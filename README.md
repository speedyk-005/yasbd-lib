<div align="center">
  <img src="https://github.com/speedyk-005/yasbd-lib/blob/main/yasbd_logo.png?raw=true" alt="Yasbd-lib Logo" width="500"/>
  <p><i>“Even a pair of scissors deserves to be smart. Welcome to cybernetic boundary shearing.”</i></p>
</div>

[![Python Version](https://img.shields.io/badge/Python-3.11%20--%203.14-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/yasbd-lib)](https://pypi.org/project/yasbd-lib)
[![Coverage Status](https://coveralls.io/repos/github/speedyk-005/yasbd-lib/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/speedyk-005/yasbd-lib?branch=main)
[![Stability](https://img.shields.io/badge/stability-alpha-red)](https://github.com/speedyk-005/yasbd-lib)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/speedyk-005/yasbd-lib/actions)
[![CodeFactor](https://www.codefactor.io/repository/github/speedyk-005/yasbd-lib/badge)](https://www.codefactor.io/repository/github/speedyk-005/yasbd-lib)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/speedyk-005/yasbd-lib)

> [!WARNING]
> This project is currently in alpha.

---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Manifesto](#manifesto)
  - [✂ Why do I need a pair of "smart scissors" for text?](#-why-do-i-need-a-pair-of-smart-scissors-for-text)
  - [🔪 Are these shears just a rusty regex loop spray-painted in carbon fiber?](#-are-these-shears-just-a-rusty-regex-loop-spray-painted-in-carbon-fiber)
- [🏁 Benchmarks](#-benchmarks)
- [📦 Installation](#-installation)
  - [The Quick & Easy Way](#the-quick--easy-way)
  - [The From-Source Way](#the-from-source-way)
  - [Want to Help Make yasbd Even Better?](#want-to-help-make-yasbd-even-better)
- [📟 Usage](#-usage)
  - [Initialization](#initialization)
  - [Boundary detection](#boundary-detection)
  - [Segmentation](#segmentation)
  - [Cleaner](#cleaner)
  - [Adapter](#adapter)
- [🗺 Features & Roadmap](#-features--roadmap)
- [📜 Last note](#-last-note)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

## Manifesto

**Y**et **A**nother **S**entence **B**oundary **D**etector is a pair of smart scissors for text. Pointer-based, from-scratch [SBD](https://en.wikipedia.org/wiki/Sentence_boundary_disambiguation) for production pipelines. Features a drop-in adapter for pysbd to fix edges cases without heavy refactoring. Five languages supported today (en, fr, es, ht, ja). Target is 22+.

###  ✂ Why do I need a pair of "smart scissors" for text?

Running `re.split(r'\.\s+[A-Z]')` and praying. This blunt tool instantly shears titles like `Mr. Smith` or French corporate markers like `Sté. Générale` in half, scattering semantic fragments across your pipeline.
Punctuation is the most overloaded glyph set in text. A period alone does six jobs and only one is "sentence end." Generic split-on-punctuation fails on:

- `Dr.` `Inc.` `U.S.A.` (abbreviation markers, not boundaries. ~47% of periods in news text are these)
- `3.5M` `3.14` (decimal points, not sentence ends)
- `D. H. Lawrence` (initials. Two periods, zero boundaries)
- `...` (ellipsis. Trailing off or sentence end? ambiguous)
- `1.` `a.` at line start (inline list markers impersonating sentence ends)
- `?!` inside quotes (punctuation nesting across boundaries)

And multilingual quirks a naive splitter never saw coming.

### 🔪 Are these shears just a rusty regex loop spray-painted in carbon fiber?

Regex is how I cut. Not what I am. My brain is a two-pass pipeline. Pass one finds every possible boundary, greedy and over-inclusive. Pass two surgically removes false positives by cross-referencing 150+ curated abbreviations across 8 semantic categories, checking context before and after each candidate. Quote spans, parentheses, list markers, ellipsis, contiguous terminators -- each gets its own refiner.

---

## 🏁 Benchmarks

Tested against 6 competitors (pysbd, sentencex, sentsplit, nupunkt, blingfire, sentence-splitter) across 5 languages and 7 edge cases: compound abbreviations, CJK quotes, newline wrapping, chat logs, URLs, and more.

**TL;DR:** yasbd ranked #1 in accuracy across almost every test, while staying competitive on speed as pure Python. blingfire is faster but brittle. pysbd and sentencex shred French abbreviations. nupunkt has an 11-second cold start.
Full results, terminal output, and a performance graph can be found in **[benchmarks/](https://github.com/speedyk-005/yasbd-lib/tree/main/benchmarks)**

<img src="https://raw.githubusercontent.com/speedyk-005/yasbd-lib/main/benchmarks/bench.png" alt="SBD Benchmark Performance" width="800"/>

---

## 📦 Installation

Ready to do some cybernetic boundary shearing? Let's get you set up quickly and painlessly.

### The Quick & Easy Way

The simplest way to get started is with pip:

```bash
pip install yasbd-lib -U
```

> [!TIP]
> **Termux (Android)**
>
> No Rust toolchain? Install pydantic-core pre-built wheels first, then retry:
>
> ```bash
> pip install typing-extensions
> pip install pydantic-core --index-url https://termux-user-repository.github.io/pypi/
> pip install "pydantic>=2.12.4,<2.13"
> ```

That's it! Blade is armed.

### The From-Source Way

Prefer building from source? Clone and install manually for full control:

```bash
git clone https://github.com/speedyk-005/yasbd-lib.git
cd yasbd
pip install .
```

(But honestly, the pip way is way easier.)

### Want to Help Make yasbd Even Better?

That's awesome. See [**Contributing Guide**](https://github.com/speedyk-005/yasbd-lib/blob/main/CONTRIBUTING.md).


---

## 📟 Usage

> [!TIP]
> Looking for the pysbd drop-in replacement? Jump straight to the [Adapter](#adapter) section.

### Initialization

```python
from yasbd.boundary_detector import BoundaryDetector
# Or from yasbd import BoundaryDetector

# Basic setup
detector = BoundaryDetector(lang="en")

# With all options (so far.)
detector = BoundaryDetector(
	# ISO 639 code (e.g., en, fr, es, ...). Defaults to `en`.
	# https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
    lang="fr",

    # Don't split inside them. (It won't protect block quotes) Defaults to `True`.
    # https://en.wikipedia.org/wiki/Block_quotation
    preserve_quote_and_paren=True,

    # Enable verbose logging. Defaults to `False`.
    verbose=True,
)
```

Switching languages at runtime is a property set:

```python
detector.lang = "es"
```

The rule module loads lazily on first access. Switching mid-stream reimports the module and rebinds the pattern cache. Zero config, no restarts needed.

### Boundary detection

[`detect()`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-boundary_detector-BoundaryDetector-detect) tells you where each sentence stops. Integer offsets into the original string. No copies, no slicing, no bookkeeping. Feed them to whatever downstream logic you already have.

Two detection modes:

- **absolute**: (default) offsets count from the start of the entire input stream.
- **relative**: offsets reset at each paragraph boundary. A `ParagraphEOF` sentinel signals the gap between paragraphs.

```python
# absolute mode (default)
res= list(detector.detect('She turned to him, "This is great." She held the book out to show him.'))
print(res)
# [35, 70]

# relative mode with paragraph break
detector.lang = "es"
res = list(detector.detect(
	"El Sr. García llegó ayer. La Sra. López también.\n\nVéase la pág. 55 del libro.",
	relative=True,
))
print(res)
# [25, 48, ParagraphEOF, 27]
```

### Segmentation

If you do not want to manage boundary offsets yourself (and who would?), [`segment()`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-boundary_detector-BoundaryDetector-segment) wraps `detect()` with string slicing. It yields sentences as strings, one at a time. By default it strips leading and trailing whitespace and drops empty results. Set `preserve_whitespace=True` to keep original spacing around boundaries.

```python
detector.lang = "en"

# Basic sentence splitting
res = list(detector.segment("Hello world. How are you? I am fine."))
print(res)
# ['Hello world.', 'How are you?', 'I am fine.']

# Multi-paragraph with whitespace preserved
res = list(detector.segment(
    "First para.\nStill first.\n\nSecond para.\nFinished.",
    preserve_whitespace=True,
))
print(res)
# ['First para.', '\nStill first.', '\n\n', 'Second para.', '\nFinished.']
```

> [!TIP]
> **Inputs & streaming** — `detect()` and `segment()` accept plain strings, open file streams (`TextIOBase`), or a `StreamCleaner`. Both are generators: they yield results lazily without loading the entire source into memory. Internally, the text is split on blank lines into paragraphs, and each paragraph is processed independently with offset tracking between them.

> [!TIP]
> **ParagraphStream** — yasbd uses [`ParagraphStream`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-utils-paragraph_stream-ParagraphStream) internally to split text into paragraph blocks. You can import it directly if you need paragraph-level processing in your own code:
> ```python
> from yasbd.utils.paragraph_stream import ParagraphStream
>
> for para in ParagraphStream(text):
>     print(para)  # each paragraph block
> ```
> You can also skip empty lines with `skip_empty_lines=True`

### Cleaner

OCRd a PDF or scraping noisy text? [`StreamCleaner`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-utils-cleaner-StreamCleaner) normalizes paragraphs before they hit the detector:

```python
from yasbd.utils.cleaner import StreamCleaner

cleaner = StreamCleaner("Hello  world.   This is  messy.")
list(cleaner)
# ['Hello world. This is messy.']
```

It collapses multiple spaces, strips HTML tags, removes page numbers, re-joins hyphenated words split across lines, and more. Pass it directly to `detect()` or `segment()` instead of a string.

### Adapter

Migrating from pysbd? Swap the import and keep your pipeline:

```python
# Before: from pysbd import Segmenter
from yasbd.utils.pysbd_adapter import Segmenter

seg = Segmenter(language="ja")
res = seg.segment('田中さんは「準備は完了しました」そう言って部屋を出た。Ｕ．Ｓ．Ａ．の経済政策は非常に複雑です。')
print(res)
# ['田中さんは「準備は完了しました」そう言って部屋を出た。', 'Ｕ．Ｓ．Ａ．の経済政策は非常に複雑です。']
```

Same API surface. Same [`Segmenter`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-utils-pysbd_adapter-Segmenter) class. Same [`segment()`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-utils-pysbd_adapter-Segmenter-segment) method. Even the [`TextSpan`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd-utils-pysbd_adapter-TextSpan) class is there with `sent`, `start`, and `end` fields, hurray. It also handles leading whitespace the way pysbd expects it (trailing on the previous sentence instead of leading on the next).

---

## 🗺 Features & Roadmap

- [x] Regex caching (compile once per language class)
- [x] Drop-in pysbd adapter (same API, no pipeline changes)
- [x] StreamCleaner for OCR'd and noisy text
- [ ] spaCy integration
- [ ] 22+ language targets
- [ ] CLI tool
- [ ] REST API for remote boundary detection

---

## 📜 Last note

**yasbd** is maintained by [speedyk-005](https://github.com/speedyk-005). Licensed under [Mozilla Public License 2.0](https://github.com/speedyk-005/yasbd-lib/blob/main/LICENSE) — you can use it in proprietary software, but modifications to the source files must stay open under MPL 2.0. Contributions are welcome; see [CONTRIBUTING.md](https://github.com/speedyk-005/yasbd-lib/blob/main/CONTRIBUTING.md).
