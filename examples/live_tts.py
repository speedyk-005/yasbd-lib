"""
Generates and plays Edge TTS audio sentence-by-sentence with parallel generation.

It can be paired with examples/incremental_segmentation.py to directly produce sentences.

Prerequisites:
    pip install miniaudio edge_tts aiofiles
"""

import asyncio
import tempfile
import time
from collections.abc import Iterable, Iterator
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from queue import Queue
from threading import Thread

import aiofiles
import edge_tts
import miniaudio

from yasbd import BoundaryDetector


class LiveTTS:
    def __init__(
        self,
        voice: str = "en-US-AriaNeural",
        n_jobs: int = 2,
    ) -> None:
        """
        Initialize the streaming client.

        Args:
            voice: Edge TTS voice model name.
            n_jobs: Number of parallel TTS generation jobs.
        """
        if n_jobs < 1:
            raise ValueError("n_jobs must be at least 1")

        self.voice = voice
        self.n_jobs = n_jobs

    def _handle_async_exception(self, loop, context) -> None:
        """Custom exception handler for the async event loop."""
        exception = context.get("exception")
        message = context.get("message", "")

        if exception:
            error_msg = str(exception)

            if "Connection lost" in error_msg and "Connection reset by peer" in error_msg:
                return

        if "SSL handshake failed" in message or "SSLWantReadError" in message:
            return

        loop.default_exception_handler(context)

    def _generate_tts_sync(self, text: str) -> str:
        """Generate TTS for a single sentence and save it to a temp file."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file_path = tmp_file.name

        async def generate() -> None:
            communicate = edge_tts.Communicate(
                text,
                self.voice,
                rate="+15%",
            )

            async with aiofiles.open(tmp_file_path, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        await file.write(chunk["data"])

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(self._handle_async_exception)

        try:
            loop.run_until_complete(generate())
            return tmp_file_path
        except Exception:
            Path(tmp_file_path).unlink(missing_ok=True)
            raise
        finally:
            asyncio.set_event_loop(None)
            loop.close()

    def _play_audio(self, file_path: str) -> None:
        """Play an audio file using miniaudio."""
        stream = miniaudio.stream_file(file_path)
        device = miniaudio.PlaybackDevice()

        try:
            device.start(stream)

            info = miniaudio.get_file_info(file_path)
            time.sleep(info.duration)
        finally:
            device.close()

    def _playback_worker(self, queue: Queue[str | None]) -> None:
        """Play generated audio files sequentially."""
        while True:
            audio_file = queue.get()

            try:
                if audio_file is None:
                    return

                self._play_audio(audio_file)
            finally:
                if audio_file is not None:
                    Path(audio_file).unlink(missing_ok=True)

                queue.task_done()

    def _generate_stream(
        self,
        chunks: Iterable[str],
        executor: ThreadPoolExecutor,
    ) -> Iterator[str]:
        """
        Generate TTS concurrently while preserving input order.

        At most ``n_jobs`` futures are kept in flight. Completed futures
        are detected with ``as_completed()``, but results are buffered
        until all preceding sentences are ready.
        """
        chunk_iter = iter(chunks)
        futures: dict[Future[str], int] = {}
        completed: dict[int, str] = {}

        next_submit = 0
        next_yield = 0

        def submit_next() -> bool:
            nonlocal next_submit

            try:
                chunk = next(chunk_iter)
            except StopIteration:
                return False

            future = executor.submit(
                self._generate_tts_sync,
                chunk,
            )
            futures[future] = next_submit
            next_submit += 1
            return True

        # Keep the executor filled initially.
        while len(futures) < self.n_jobs:
            if not submit_next():
                break

        while futures:
            # Wait for the first future that completes.
            for future in as_completed(futures):
                index = futures.pop(future)
                completed[index] = future.result()

                # Immediately replace the completed job with new input.
                submit_next()

                break

            # Release completed sentences in their original order.
            while next_yield in completed:
                yield completed.pop(next_yield)
                next_yield += 1

    def play_live(self, text_or_gen: str | Iterable[str]) -> None:
        """
        Generate and play text live, sentence-by-sentence.

        Args:
            text_or_gen: Raw text or an iterable of text to synthesize.
        """
        if isinstance(text_or_gen, str):
            splitter = BoundaryDetector(
                lang=self.voice.split("-")[0],
            )
            chunks = splitter.segment(text_or_gen)
        else:
            chunks = text_or_gen

        playback_queue: Queue[str | None] = Queue()

        playback_thread = Thread(
            target=self._playback_worker,
            args=(playback_queue,),
            daemon=True,
        )
        playback_thread.start()

        with ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            for audio_file in self._generate_stream(chunks, executor):
                if audio_file:
                    playback_queue.put(audio_file)

        # No more audio files will arrive.
        playback_queue.put(None)

        # Wait until every queued file has finished playing.
        playback_queue.join()
        playback_thread.join()


# Example usage
if __name__ == "__main__":
    text = [
        "Got it. I updated my memory:",
        "PLASMA is no longer an active project for you.",
        "Ruff is your preferred Python tooling instead of Black, Pylint, and Flake8.",
        "You mainly use PocketPal and MNN Chat for AI/local model usage.",
        "Layla AI Lite is no longer considered one of your main tools.",
        "I'll use these preferences going forward.",
    ]

    client = LiveTTS(
        voice="en-US-AriaNeural",
        n_jobs=3,
    )

    print(text)
    client.play_live(text)
    print("Playback finished!")
