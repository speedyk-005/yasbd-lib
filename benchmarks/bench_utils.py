"""Unified wrapper for all Sentence Boundary Detection (SBD) libraries."""

from __future__ import annotations

import timeit
import warnings
from typing import Any, Type, TypeVar

from loguru import logger as _loguru
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

_loguru.disable("sentsplit")
_console = Console()

warnings.filterwarnings("ignore", category=UserWarning, module="sentsplit")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")

T = TypeVar("T", bound="BaseSegmenter")
_REGISTRY: dict[str, BaseSegmenter] = {}


def register_with_lang(lang: str):
    """Decorator factory to instantiate a segmenter with a specific language."""

    def decorator(cls: Type[T]) -> Type[T]:
        instance = cls(lang=lang)
        _REGISTRY[instance.name] = instance
        return cls

    return decorator


class BaseSegmenter:
    name: str
    langs: list[str] = []

    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.last_run_stats: dict[str, Any] | None = None

    def segment(self, text: str, verbose: bool = False) -> list[str]:
        try:
            result = self._segment(text)
        except Exception as e:
            print(f"  {self.name} [{self.lang}]... ERROR")
            raise e
        if verbose:
            print(f"  {self.name} [{self.lang}]: {len(result)} sents")
        return result

    def _segment(self, text: str) -> list[str]:
        raise NotImplementedError


# ── yasbd ───


@register_with_lang(lang="en")
class YasbdWrapper(BaseSegmenter):
    name = "yasbd"
    langs = ["en", "fr", "ht", "es", "ja"]

    def __init__(self, lang: str) -> None:
        super().__init__(lang)
        from yasbd.boundary_detector import BoundaryDetector

        self._detector = BoundaryDetector(lang=self.lang)

    def _segment(self, text: str) -> list[str]:
        if self._detector.lang != self.lang:
            self._detector.lang = self.lang
        return list(self._detector.segment(text))


# ── pysbd ───


@register_with_lang(lang="en")
class PysbdWrapper(BaseSegmenter):
    name = "pysbd"
    langs = [
        "en",
        "es",
        "fr",
        "de",
        "it",
        "nl",
        "pt",
        "da",
        "no",
        "sv",
        "ar",
        "ja",
        "zh",
        "ko",
        "ru",
        "pl",
        "tr",
        "vi",
        "th",
        "el",
        "hi",
        "ur",
    ]

    def __init__(self, lang: str) -> None:
        super().__init__(lang)
        import pysbd

        self._segmenter = pysbd.Segmenter(language=self.lang, clean=False)

    def _segment(self, text: str) -> list[str]:
        return self._segmenter.segment(text)


# ── sentencex ──


@register_with_lang(lang="en")
class SentencexWrapper(BaseSegmenter):
    name = "sentencex"
    langs = []

    # Note: sentencex doesn't use stateful initialization, it accepts lang during execution,
    # but we still track lang in __init__ for structural consistency across the wrappers.
    def __init__(self, lang: str) -> None:
        super().__init__(lang)

    def _segment(self, text: str) -> list[str]:
        import sentencex

        return sentencex.segment(self.lang, text)


# ── sentsplit ──


@register_with_lang(lang="en")
class SentsplitWrapper(BaseSegmenter):
    name = "sentsplit"
    langs = ["en", "fr", "de", "it", "ja", "ko", "lt", "pl", "pt", "ru", "zh", "tr"]

    def __init__(self, lang: str) -> None:
        super().__init__(lang)
        from sentsplit.segment import SentSplit

        self._splitter = SentSplit(self.lang)

    def _segment(self, text: str) -> list[str]:
        return self._splitter.segment(text)


# ── nupunkt ─


@register_with_lang(lang="en")
class NupunktWrapper(BaseSegmenter):
    name = "nupunkt"
    langs = ["en", "es", "fr", "de", "it", "nl", "pt", "ru", "pl", "sv", "da", "no"]

    def __init__(self, lang: str) -> None:
        super().__init__(lang)

    def _segment(self, text: str) -> list[str]:
        from nupunkt import sent_tokenize

        return sent_tokenize(text)


# ── blingfire ───


@register_with_lang(lang="en")
class BlingfireWrapper(BaseSegmenter):
    name = "blingfire"
    langs = []

    def __init__(self, lang: str) -> None:
        super().__init__(lang)

    def _segment(self, text: str) -> list[str]:
        from blingfire import text_to_sentences

        raw = text_to_sentences(text)
        return raw.split("\n")


# ── sentence-splitter ───


@register_with_lang(lang="en")
class SentenceSplitterWrapper(BaseSegmenter):
    name = "sentence-splitter"
    langs = [
        "en",
        "da",
        "de",
        "es",
        "fi",
        "fr",
        "it",
        "lt",
        "nb",
        "nl",
        "pl",
        "pt",
        "ro",
        "sv",
        "tr",
    ]

    def __init__(self, lang: str) -> None:
        super().__init__(lang)
        from sentence_splitter import SentenceSplitter

        self._splitter = SentenceSplitter(language=self.lang)

    def _segment(self, text: str) -> list[str]:
        return self._splitter.split(text)


# ── Public API ───


def get_segmenter(name: str, lang: str = "en") -> BaseSegmenter:
    """Return a specific segmenter, setting the requested language."""
    if name not in _REGISTRY:
        raise ValueError(f"Segmenter '{name}' is not registered.")
    _REGISTRY[name].lang = lang
    return _REGISTRY[name]


def all_segmenters(lang: str = "en") -> dict[str, BaseSegmenter]:
    """Return all registered segmenters, setting the requested language on each."""
    for seg in _REGISTRY.values():
        seg.lang = lang
    return dict(_REGISTRY)


def warm_time_segmenters(text: str, lang: str = "en", number: int = 10):
    """Run warm timing on all segmenters via the registry.

    Returns {name: {"ms": float, "sents": int}}.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=_console,
    ) as progress:
        task = progress.add_task("Warming up...", total=len(_REGISTRY) * 2)
        for name, seg in _REGISTRY.items():
            seg.lang = lang
            progress.update(task, description=f"Warming {name}...")
            sents = seg.segment(text)  # warm-up
            progress.advance(task)
            progress.update(task, description=f"Timing {name}...")
            t = timeit.timeit(lambda s=seg, t=text: s.segment(t), number=number)
            progress.advance(task)
            ms = t / number * 1000
            _console.print(f"[bold]{name:20s}[/] {ms:.2f}ms  ({len(sents)} sents)")


def segment_and_print(text: str, lang: str = "en") -> dict[str, list[str]]:
    """Segments text across all wrappers initialized dynamically to the requested language."""
    results = {}

    # We pass the dynamic language to all_segmenters to get clean, fresh object configurations
    for name, seg in all_segmenters(lang=lang).items():
        try:
            sents = seg.segment(text)
            results[name] = sents
            print(f"  {name} [{lang}]:")
            for i, s in enumerate(sents, 1):
                print(f"    {i}: {s!r}")
            print()
        except Exception as e:
            print(f"  {name} [{lang}]... ERROR: {e}\n")

    return results
