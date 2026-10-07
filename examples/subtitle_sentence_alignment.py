"""Join SRT subtitle cues into sentences while retaining their source time ranges.

Subtitle cues often split a sentence over several display intervals, or contain
the end of one sentence and the start of another. Use detect() character offsets
to associate each sentence with the cues containing its text.

Times are the envelope of the source cues, not word-level timestamps. Two output
sentences can therefore overlap when they share an input cue. Input text should
already contain punctuation; this example does not restore missing punctuation.

Setup:
    pip install yasbd-lib "srt>=3.5.3,<4"

Run the built-in sample or read a UTF-8 subtitle file:
    python examples/subtitle_sentence_alignment.py
    python examples/subtitle_sentence_alignment.py input.srt --lang en > sentences.srt
"""

import argparse
from itertools import pairwise
from pathlib import Path

import srt

from yasbd import BoundaryDetector

SAMPLE_SUBTITLES = """1
00:00:00,000 --> 00:00:01,800
Dr. Patel reviewed the

2
00:00:01,800 --> 00:00:04,200
U.S. launch. We agreed

3
00:00:04,200 --> 00:00:06,500
to proceed.
"""


def sentence_cues(source: str, lang: str = "en") -> list[srt.Subtitle]:
    """Return sentence-sized cues with the time envelope of their source cues.

    >>> cues = sentence_cues(SAMPLE_SUBTITLES)
    >>> [cue.content for cue in cues]
    ['Dr. Patel reviewed the U.S. launch.', 'We agreed to proceed.']
    >>> [(cue.start.total_seconds(), cue.end.total_seconds()) for cue in cues]
    [(0.0, 4.2), (1.8, 6.5)]
    >>> source = srt.Subtitle(1, cues[0].start, cues[0].end, "First. Second.")
    >>> shared = sentence_cues(source.to_srt())
    >>> [cue.content for cue in shared]
    ['First.', 'Second.']
    >>> all(cue.start == source.start and cue.end == source.end for cue in shared)
    True
    >>> sentence_cues("")
    []
    """
    pieces = []
    ranges = []
    offset = 0
    for cue in srt.parse(source):
        content = " ".join(cue.content.split())
        if not content:
            continue
        pieces.append(content)
        ranges.append((offset, offset + len(content), cue))
        offset += len(content) + 1

    if not ranges:
        return []

    text = " ".join(pieces)
    detector = BoundaryDetector(lang=lang)
    result = []
    cursor = 0
    for start, end in pairwise((0, *detector.detect(text))):
        sentence = text[start:end]
        left = start + len(sentence) - len(sentence.lstrip())
        right = start + len(sentence.rstrip())
        if left >= right:
            continue

        while ranges[cursor][1] <= left:
            cursor += 1
        last = cursor
        while last + 1 < len(ranges) and ranges[last + 1][0] < right:
            last += 1
        covered = [item[2] for item in ranges[cursor : last + 1]]
        result.append(
            srt.Subtitle(
                index=len(result) + 1,
                start=min(cue.start for cue in covered),
                end=max(cue.end for cue in covered),
                content=text[left:right],
            )
        )
        cursor = last

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", nargs="?", type=Path, help="UTF-8 SRT file")
    parser.add_argument("--lang", default="en", help="YASBD language code (default: en)")
    args = parser.parse_args()
    source = (
        args.input.read_text(encoding="utf-8-sig")
        if args.input is not None
        else SAMPLE_SUBTITLES
    )
    print(srt.compose(sentence_cues(source, args.lang)), end="")


if __name__ == "__main__":
    main()
