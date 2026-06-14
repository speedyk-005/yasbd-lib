<div align="center">
  <img src="https://github.com/speedyk-005/yasbd-lib/blob/main/yasbd_logo.png?raw=true" alt="Yasbd-lib Logo" width="500"/>
  <p><i>"Even a pair of scissors deserves to be smart. Welcome to cybernetic boundary shearing."</i></p>
</div>

[![Python Version](https://img.shields.io/badge/Python-3.11%20--%203.14-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/yasbd-lib?kill_cache=1)](https://pypi.org/project/yasbd-lib)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/yasbd-lib?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/yasbd-lib)
[![Coverage Status](https://coveralls.io/repos/github/speedyk-005/yasbd-lib/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/speedyk-005/yasbd-lib?branch=main)
[![Stability](https://img.shields.io/badge/stability-alpha-red)](https://github.com/speedyk-005/yasbd-lib)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/speedyk-005/yasbd-lib/actions)
[![CodeFactor](https://www.codefactor.io/repository/github/speedyk-005/yasbd-lib/badge)](https://www.codefactor.io/repository/github/speedyk-005/yasbd-lib)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/speedyk-005/yasbd-lib)

> [!WARNING]
> This project is currently in alpha.

---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [🎬 Manifesto](#-manifesto)
  - [✂ Why do I need a pair of "smart scissors" for text?](#-why-do-i-need-a-pair-of-smart-scissors-for-text)
  - [🔪 Are these shears just a rusty regex loop spray-painted in carbon fiber?](#-are-these-shears-just-a-rusty-regex-loop-spray-painted-in-carbon-fiber)
- [🌐 Supported Languages](#-supported-languages)
- [🏁 Benchmarks](#-benchmarks)
- [📦 Installation](#-installation)
  - [The Quick & Easy Way](#the-quick--easy-way)
  - [The From-Source Way](#the-from-source-way)
  - [Want to Help Make yasbd Even Better?](#want-to-help-make-yasbd-even-better)
- [📟 Usage](#-usage)
  - [Initialization](#initialization)
  - [Core Methods](#core-methods)
    - [Boundary detection](#boundary-detection)
    - [Segmentation](#segmentation)
  - [Cleaner](#cleaner)
  - [CLI](#cli)
    - [About JSONL](#about-jsonl)
  - [Adapter](#adapter)
  - [spaCy component](#spacy-component)
- [🗺 Features & Roadmap](#-features--roadmap)
- [🤝 Contributors](#-contributors)
- [📜 Last note](#-last-note)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

## 🎬 Manifesto

**Y**et **A**nother **S**entence **B**oundary **D**etector is a pair of smart scissors for text. Pointer-based, from-scratch [SBD](https://en.wikipedia.org/wiki/Sentence_boundary_disambiguation) for production NLP pipelines. Features a drop-in adapter for pysbd to fix edge cases without heavy refactoring.

###  ✂ Why do I need a pair of "smart scissors" for text?

Running `re.split(r'\.\s+[A-Z]')` and praying. This blunt tool instantly shears titles like `Mr. Smith` or French corporate markers like `Sté. Générale` in half, scattering semantic fragments across the pipeline.

Punctuation is the most overloaded glyph set in text. A period alone does six jobs and only one is "sentence end." Generic split-on-punctuation fails on:

- `Dr.` `Inc.` `U.S.A.` (abbreviation markers, not boundaries. ~47% of periods in news text are these)
- `3.5M` `3.14` (decimal points, not sentence ends)
- `D. H. Lawrence` (initials. Two periods, zero boundaries)
- `...` (ellipsis. Trailing off or sentence end? ambiguous)
- `1.` `a.` at line start (inline list markers impersonating sentence ends)
- `?!` inside quotes (punctuation nesting across boundaries)

And multilingual quirks a naive splitter never saw coming.

### 🔪 Are these shears just a rusty regex loop spray-painted in carbon fiber?

Regex is how I cut. Not what I am. My brain is a two-pass pipeline:

**Pass 1** - Naive boundary finder. Finds every position that could plausibly end a sentence: periods, question marks, exclamation points - anything followed by whitespace, uppercase, or a newline. Deliberately over-inclusive. Better to catch a false positive than miss a real boundary.

**Pass 2** - Cross-references 9+ mid-sentence patterns to surgically excise false positives:

- Newline inside sentence
- Title/initialism protection
- Abbreviation lists
- Geopolitical + case markers
- Quote/parenthesis span filtering
- TOC leader suppression
- List marker re-alignmen
- Contiguous terminator collapsing
- Language specifical final fixups

---

## 🌐 Supported Languages

11 languages supported today. Target is 22+.

|  | Code | Language |
|--|------|----------|
| 🇪🇹 | am   | Amharic |
| 🇸🇦 | ar   | Arabic |
| 🇩🇪 | de   | German |
| 🇬🇧 | en   | English |
| 🇪🇸 | es   | Spanish |
| 🇫🇷 | fr   | French |
| 🇭🇹 | ht   | Haitian Creole |
| 🇯🇵 | ja   | Japanese |
| 🇵🇹 | pt   | Portuguese |
| 🇷🇺 | ru   | Russian |
| 🇨🇳 | zh   | Chinese |

You can also get a list from `yasbd.get_supported_langs`.

---

## 🏁 Benchmarks

Tested against 6 competitors (pysbd, sentencex, sentsplit, nupunkt, blingfire, sentence-splitter) across 5 languages and 7 edge cases: compound abbreviations, CJK quotes, newline wrapping, chat logs, URLs, decimals, and nested punctuation.

**TL;DR:** yasbd ranked #1 in accuracy across almost every test, while staying competitive on speed as pure Python. blingfire is faster but brittle. pysbd and sentencex shred French abbreviations.

On our [golden benchmark](https://github.com/speedyk-005/yasbd-lib/tree/main/benchmarks#en-golden-benchmark) (92 English edge cases adapted from pysbd's official golden rule set with fixes and additions): yasbd scores **98.9%**, pysbd **83.7%**.

Full results, terminal output, and a performance graph can be found in **[benchmarks/](https://github.com/speedyk-005/yasbd-lib/tree/main/benchmarks)**

**SPOILER**: Yasbd aced 'em all in accuracy while offering balanced speed.

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
> Not a Pythonista? Jump straight to the [CLI](#cli) section.
>
> Looking for the pysbd drop-in replacement? Jump straight to the [Adapter](#adapter) section.

### Initialization

```python
from yasbd.boundary_detector import BoundaryDetector
# Or from yasbd import BoundaryDetector

# Basic setup
detector = BoundaryDetector(lang="en")

# With all options (so far.)
detector = BoundaryDetector(
	# ISO 639 code (e.g., en, fr, es, ...). Required.
	# Use "auto" for automatic detection.
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

> [!TIP]
> **Auto-detect**
>
> Pass `lang="auto"` if you want the system to figure out the language for you.
> I wouldn't lean on it too hard tho — it's a bit slower, and short phrases can throw it off sometimes.

### Core Methods
The two primary APIs are detect() and segment().

Both methods accept plain strings, open text streams (TextIOBase), or a StreamCleaner instance. Inputs are processed lazily as a stream of paragraphs, allowing large documents to be handled without loading everything into memory at once.

- `detect()` yields sentence boundary offsets.
- `segment()` yields sentence strings.

#### Boundary detection

[`detect()`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd.boundary_detector.BoundaryDetector.detect) tells you where each sentence stops. Integer offsets into the original input stream.

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

#### Segmentation

If you do not want to manage boundary offsets yourself (and who would?), [`segment()`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd.boundary_detector.BoundaryDetector.segment) slices text for you.

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
> **ParagraphStream** - yasbd uses [`ParagraphStream`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd.utils.paragraph_stream.ParagraphStream) internally to split text into paragraph blocks. You can import it directly if you need paragraph-level processing in your own code:
> ```python
> from yasbd.utils.paragraph_stream import ParagraphStream  # or yasbd.paragraph_stream
>
> for para in ParagraphStream(text):  # or an opened file
>     print(para)  # each paragraph block
> ```
> You can also skip empty lines with `skip_empty_lines=True`

### Cleaner

OCR'd a PDF, parsed a DOCX, or scraped noisy HTML? "StreamCleaner" normalizes text before it reaches the language detector or sentence segmenter.
StreamCleaner accepts either a string or an open text stream and yields cleaned paragraphs lazily.
You can pass a "StreamCleaner" instance directly to "detect()" or "segment()" to clean text as it is processed.

```python
from yasbd.utils.cleaner import StreamCleaner  # or yasbd.cleaner

cleaner = StreamCleaner(
    "Hello  world.   This is  messy.",
    verbose=True,  # Default to False
)
list(cleaner)
# ['Hello world. This is messy.']
```

"StreamCleaner" implements the iterator protocol and yields cleaned paragraphs one at a time. It can consume plain strings, open text files, and other text streams.

```python
from yasbd.utils.cleaner import StreamCleaner  # or yasbd.cleaner

with open("document.txt", encoding="utf-8") as f:
    for paragraph in StreamCleaner(f):
        print(paragraph)
```

Common cleanup operations include:

- Fixing mojibake and OCR artifacts
- Removing HTML tags
- Normalizing whitespace and repeated slashes
- Rejoining hyphenated words split across lines
- Merging vertically stacked characters

**Skip** built-in steps you don't want:

```python
cleaner = StreamCleaner(
    text,
    steps_to_skip=[
        "fix_ocr_text",
        "normalize_spaces",
    ],
)
```

**Add** custom cleaning steps:

```python
cleaner = StreamCleaner(
    text,
    extra_steps=[
        lambda t: t.replace("TM", ""),
        lambda t: t.upper(),
    ],
)
```

Each extra step must accept and return a `str`. If a step raises or returns a non-string, a `CleanStepError` is raised with the original exception chained.

Available built-in steps:

| Step | What it does |
|------|-------------|
| `fix_mojibake` | Fixes Unicode mojibake via ftfy |
| `fix_ocr_text` | Repairs OCR artifacts, rejoins hyphenated words, removes page markers |
| `unwrap_htmls` | Strips HTML tags (including `<script>`, `<style>` and their content) |
| `normalize_slashes` | Collapses `///` triple slashes |
| `normalize_spaces` | Collapses multiple spaces into one |

### CLI

Do you just want to split text into sentences without writing Python?
The `yasbd` command works right from your terminal. Install once, pipe
anything into it, get sentences back.

```bash
# List supported language codes
yasbd langs
# am, ar, de, en, es, fr, ht, ja, pt, ru, zh

# Split text into sentences
yasbd segment "Dr. Smith works here. Is he there?"
# [1] 'Dr. Smith works here.'
# [2] 'Is he there?'

# Detect boundary offsets
yasbd detect "Hello world. How are you?"
# [1] 12
# [2] 24

# Read from file
yasbd segment --file document.txt
yasbd segment --file input.txt --destination output.txt  # JSONL output

# Pipe support - auto-detects, skips [N] enumeration
echo "Hello. World." | yasbd segment | cat
# Hello.
# World.

# Clean noisy text (HTML, mojibake, OCR artifacts)
yasbd clean "<script>x</script>Hello <b>world</b>."
# [1] 'Hello <b>world</b>.'

# Clean with extra shell command step (e.g., transliterate via external tool)
yasbd clean "naïve café" --extra-step "sed 's/é/e/g; s/ï/i/g'"
# [1] 'naive cafe'

# Repeatable --extra-step for multiple shell commands
yasbd clean "HELLO." -e "tr 'A-Z' 'a-z'" -e "sed 's/\./!/g'"
# [1] 'hello!'

# Chaining: Skip HTML unwrap then segment in Spanish with verbosity
yasbd clean --file dirty.html --skip unwrap_htmls | yasbd segment --lang es -v

# Version
yasbd --version

# Full help
yasbd --help         # top-level commands
yasbd segment --help # per-command options
yasbd detect --help
yasbd clean --help
```

CLI API reference at [`API_REFERENCES.md#yasbd.cli`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd.cli).

#### About JSONL

When writing to a file with `--destination`, output is JSONL (one JSON object per line):

- **segment / clean**: `{"no": 1, "text": "Hello."}`
- **detect**: `{"no": 1, "offset": 6}` or `{"no": 2, "offset": 13}`
- **detect --relative**: `{"no": 3, "eof": true}` on paragraph boundaries

### Adapter

Migrating from pysbd? Swap the import and keep your pipeline:

```python
# Before: from pysbd import Segmenter
from yasbd.utils.pysbd_adapter import Segmenter  # or yasbd.pysbd_adapter

seg = Segmenter(language="ja")
res = seg.segment('田中さんは「準備は完了しました」そう言って部屋を出た。U.S.A.の経済政策は非常に複雑です。')
print(res)
# ['田中さんは「準備は完了しました」そう言って部屋を出た。', 'U.S.A.の経済政策は非常に複雑です。']
```

Same API surface. Same [`Segmenter`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd.utils.pysbd_adapter.Segmenter) class. Same [`segment()`](https://github.com/speedyk-005/yasbd-lib/blob/main/API_REFERENCES.md#yasbd.utils.pysbd_adapter.Segmenter.segment) method signature. Even the lovely `TextSpan` with `.sent`, `.start`, `.end` is included.

---

### spaCy component

Even your spaCy pipeline deserves smart scissors. Call `register_spacy_component()` once, then add `yasbd` to any pipeline:

```python
import spacy
from yasbd import register_spacy_component

register_spacy_component()  # requires spaCy v3+
nlp = spacy.blank("en")
nlp.add_pipe("yasbd", first=True, config={"lang": "en"})

doc = nlp("Dr. Smith arrived. He was late.")
for sent in doc.sents:
    print(sent.text)
# Dr. Smith arrived.
# He was late.
```

Tweak the detector at runtime:

```python
pipe = nlp.get_pipe("yasbd")
pipe.detector.lang = "fr"
pipe.detector.verbose = True
```

---

## 🗺 Features & Roadmap

- [x] Base segmenter
- [x] Regex caching (compile once per language class)
- [x] Drop-in pysbd adapter (same API, no pipeline changes)
- [x] StreamCleaner for OCR'd and noisy text
- [x] CLI tool
- [x] Automatic language detection with caching (#74)
- [x] spaCy v3 pipeline component factory (#28)
- [ ] 22+ language targets (#20)

---

## 🤝 Contributors

A massive thank you to the open source community helping make `yasbd` more accurate and scalable:

| Name | Role |
|------|------|
| **[@speedyk-005](https://github.com/speedyk-005)** | Maintainer & Creator |
| **[@JheanLL](https://github.com/JheanLL)** | Trie prototype design & Spanish rule contributions |
| **[@Jah-yee](https://github.com/Jah-yee)** | Community contributor |
| **[@Rajesh270712](https://github.com/Rajesh270712)** | Base + English rule contributions |

Interested in contributing? See the [**Contributing Guide**](https://github.com/speedyk-005/yasbd-lib/blob/main/CONTRIBUTING.md) to get started!

---

## 📜 Last note

**yasbd** is maintained by [speedyk-005](https://github.com/speedyk-005). Licensed under [Mozilla Public License 2.0](https://github.com/speedyk-005/yasbd-lib/blob/main/LICENSE) - you can use it freely in commercial and private work.

Star us on GitHub if you dig it. Tell your NLP pipeline we said hi. 🚀
