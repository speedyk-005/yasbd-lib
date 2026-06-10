# Table of Contents

* [yasbd](#yasbd)
* [yasbd.boundary\_detector](#yasbd.boundary_detector)
  * [BoundaryDetector](#yasbd.boundary_detector.BoundaryDetector)
    * [\_\_init\_\_](#yasbd.boundary_detector.BoundaryDetector.__init__)
    * [lang](#yasbd.boundary_detector.BoundaryDetector.lang)
    * [detect](#yasbd.boundary_detector.BoundaryDetector.detect)
    * [segment](#yasbd.boundary_detector.BoundaryDetector.segment)
* [yasbd.cli](#yasbd.cli)
  * [segment](#yasbd.cli.segment)
  * [detect](#yasbd.cli.detect)
  * [clean](#yasbd.cli.clean)
  * [langs](#yasbd.cli.langs)
  * [main](#yasbd.cli.main)
* [yasbd.exceptions](#yasbd.exceptions)
  * [YasbdError](#yasbd.exceptions.YasbdError)
  * [UnsupportedLanguageError](#yasbd.exceptions.UnsupportedLanguageError)
  * [InvalidInputError](#yasbd.exceptions.InvalidInputError)
  * [CleanStepError](#yasbd.exceptions.CleanStepError)
* [yasbd.rules](#yasbd.rules)
  * [get\_supported\_langs](#yasbd.rules.get_supported_langs)
* [yasbd.rules.ar](#yasbd.rules.ar)
* [yasbd.rules.base](#yasbd.rules.base)
  * [Rules](#yasbd.rules.base.Rules)
    * [\_\_init\_\_](#yasbd.rules.base.Rules.__init__)
    * [apply](#yasbd.rules.base.Rules.apply)
* [yasbd.rules.de](#yasbd.rules.de)
* [yasbd.rules.en](#yasbd.rules.en)
* [yasbd.rules.es](#yasbd.rules.es)
* [yasbd.rules.fr](#yasbd.rules.fr)
* [yasbd.rules.ht](#yasbd.rules.ht)
* [yasbd.rules.ja](#yasbd.rules.ja)
* [yasbd.rules.pt](#yasbd.rules.pt)
* [yasbd.rules.ru](#yasbd.rules.ru)
* [yasbd.rules.zh](#yasbd.rules.zh)
* [yasbd.utils](#yasbd.utils)
* [yasbd.utils.cleaner](#yasbd.utils.cleaner)
  * [StreamCleaner](#yasbd.utils.cleaner.StreamCleaner)
    * [\_\_init\_\_](#yasbd.utils.cleaner.StreamCleaner.__init__)
* [yasbd.utils.input\_validator](#yasbd.utils.input_validator)
  * [validate\_input](#yasbd.utils.input_validator.validate_input)
* [yasbd.utils.logger](#yasbd.utils.logger)
  * [log\_info](#yasbd.utils.logger.log_info)
* [yasbd.utils.paragraph\_stream](#yasbd.utils.paragraph_stream)
  * [ParagraphStream](#yasbd.utils.paragraph_stream.ParagraphStream)
    * [\_\_init\_\_](#yasbd.utils.paragraph_stream.ParagraphStream.__init__)
    * [\_\_next\_\_](#yasbd.utils.paragraph_stream.ParagraphStream.__next__)
* [yasbd.utils.pysbd\_adapter](#yasbd.utils.pysbd_adapter)
  * [TextSpan](#yasbd.utils.pysbd_adapter.TextSpan)
  * [Segmenter](#yasbd.utils.pysbd_adapter.Segmenter)
    * [\_\_init\_\_](#yasbd.utils.pysbd_adapter.Segmenter.__init__)
    * [sentences\_with\_char\_spans](#yasbd.utils.pysbd_adapter.Segmenter.sentences_with_char_spans)
    * [segment](#yasbd.utils.pysbd_adapter.Segmenter.segment)

<a id="yasbd"></a>

# yasbd

<a id="yasbd.boundary_detector"></a>

# yasbd.boundary\_detector

<a id="yasbd.boundary_detector.BoundaryDetector"></a>

## BoundaryDetector Objects

```python
class BoundaryDetector()
```

<a id="yasbd.boundary_detector.BoundaryDetector.__init__"></a>

#### \_\_init\_\_

```python
@validate_input
def __init__(lang: str = "en",
             *,
             preserve_quote_and_paren: bool = True,
             verbose: bool = False)
```

Initialize the segmenter.

**Arguments**:

- `lang` - Two chars ISO language code (e.g. en, fr, ...).
- `preserve_quote_and_paren` - Do not split on terminators inside
  quoted or parenthesised text.
- `verbose` - Enable verbose logging.

<a id="yasbd.boundary_detector.BoundaryDetector.lang"></a>

#### lang

```python
@property
def lang() -> str
```

ISO language code of the active rule set.

<a id="yasbd.boundary_detector.BoundaryDetector.detect"></a>

#### detect

```python
@validate_input
def detect(source: str | TextIOBase | StreamCleanerStub,
           *,
           relative: bool = False) -> Generator[int, None, None]
```

Detect sentence boundaries in the source text.

**Arguments**:

- `source` - Plain text string, an open text stream (e.g., ``StringIO``),
  or a ``StreamCleaner`` instance.
- `relative` - If ``False`` (default), yields absolute character
  offsets from the beginning of the entire stream. If ``True``,
  offsets reset at each paragraph break, yielding indices relative
  to the start of the current paragraph.
  

**Notes**:

  When ``relative=True``, a ``ParagraphEOF`` sentinel is yielded
  between distinct paragraphs to signal the boundary of the local
  coordinate system. Import via: ``from yasbd import ParagraphEOF``.
  

**Yields**:

  Integer boundary offsets or ``ParagraphEOF`` sentinels.

<a id="yasbd.boundary_detector.BoundaryDetector.segment"></a>

#### segment

```python
@validate_input
def segment(source: str | TextIOBase | StreamCleanerStub,
            *,
            preserve_whitespace: bool = False) -> Generator[str, None, None]
```

Split text into sentences.

**Arguments**:

- `source` - Plain text string or ``TextIOBase`` stream
  (e.g., ``StringIO``, opened file).
- `preserve_whitespace` - If ``False`` (default), strip leading and
  trailing whitespace from each sentence.
  

**Yields**:

  Individual sentences as strings.

<a id="yasbd.cli"></a>

# yasbd.cli

<a id="yasbd.cli.segment"></a>

#### segment

```python
@cli.command(
    "segment",
    text=Arg(help="Text to split. Use --file to read from a file instead."),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination", "-d", help="Write output to a file."),
    lang=Arg("--lang", "-l", help="Language code (e.g., 'en', 'fr', 'de')."),
    preserve_whitespace=Arg("--preserve-whitespace",
                            "-w",
                            help="Preserve original whitespace in output."),
    verbose=Arg("--verbose", "-v", help="Enable verbose logging."),
)
def segment(text: Optional[str] = None,
            file: Optional[str] = None,
            destination: Optional[str] = None,
            lang: str = "en",
            preserve_whitespace: bool = False,
            verbose: bool = False)
```

Split text into sentences.

Reads from a positional string, --file, or stdin pipe.
Writes enumerated sentences to stdout or JSONL to --destination.

<a id="yasbd.cli.detect"></a>

#### detect

```python
@cli.command(
    "detect",
    text=Arg(
        help=
        "Text to detect boundaries in. Use --file to read from a file instead."
    ),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination",
                    "-d",
                    help="Write boundary offsets to a file."),
    lang=Arg("--lang", "-l", help="Language code (e.g., 'en', 'fr', 'de')."),
    relative=Arg("--relative", "-r", help="Yield paragraph-relative offsets."),
    verbose=Arg("--verbose", "-v", help="Enable verbose logging."),
)
def detect(text: Optional[str] = None,
           file: Optional[str] = None,
           destination: Optional[str] = None,
           lang: str = "en",
           relative: bool = False,
           verbose: bool = False)
```

Detect sentence boundary offsets (character positions).

Reads from a positional string, --file, or stdin pipe.
Writes boundary offsets to stdout or JSONL to --destination.
Use --relative for per-paragraph offsets (ParagraphEOF marks gaps).

<a id="yasbd.cli.clean"></a>

#### clean

```python
@cli.command(
    "clean",
    text=Arg(help="Text to clean. Use --file to read from a file instead."),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination",
                    "-d",
                    help="Write cleaned text to a file."),
    steps_to_skip=Arg("--steps-to-skip",
                      "--skip",
                      help="Comma-separated cleaning steps to skip."),
    extra_step=Arg(
        "--extra-step",
        "-e",
        help=
        "External shell command to run as an extra cleaning step (repeatable).",
    ),
    verbose=Arg("--verbose", "-v", help="Enable verbose logging."),
)
def clean(text: Optional[str] = None,
          file: Optional[str] = None,
          destination: Optional[str] = None,
          steps_to_skip: Optional[str] = None,
          extra_step: Optional[list[str]] = None,
          verbose: bool = False)
```

Clean and normalize noisy text paragraphs.

Applies ftfy mojibake fixing, OCR cleanup, HTML tag stripping,
slash normalization, and whitespace normalization.
Use --skip to omit specific steps (comma-separated).
Use --extra-step to run external shell commands as extra cleaning steps.

<a id="yasbd.cli.langs"></a>

#### langs

```python
@cli.command("langs")
def langs()
```

List supported language codes.

<a id="yasbd.cli.main"></a>

#### main

```python
def main()
```

CLI entry point. Handles --version, --help, and dispatches to radicli.

<a id="yasbd.exceptions"></a>

# yasbd.exceptions

<a id="yasbd.exceptions.YasbdError"></a>

## YasbdError Objects

```python
class YasbdError(Exception)
```

Base exception for all yasbd errors.

<a id="yasbd.exceptions.UnsupportedLanguageError"></a>

## UnsupportedLanguageError Objects

```python
class UnsupportedLanguageError(YasbdError, ValueError)
```

Raised when an unsupported language code is provided.

<a id="yasbd.exceptions.InvalidInputError"></a>

## InvalidInputError Objects

```python
class InvalidInputError(YasbdError, TypeError)
```

Raised when invalid input(s) are encountered.

<a id="yasbd.exceptions.CleanStepError"></a>

## CleanStepError Objects

```python
class CleanStepError(YasbdError, TypeError)
```

Raised when a StreamCleaner extra step fails (non-callable or non-str return).

<a id="yasbd.rules"></a>

# yasbd.rules

<a id="yasbd.rules.get_supported_langs"></a>

#### get\_supported\_langs

```python
@cache
def get_supported_langs() -> list[str]
```

Discover and cache supported language codes from the rules directory.

<a id="yasbd.rules.ar"></a>

# yasbd.rules.ar

<a id="yasbd.rules.base"></a>

# yasbd.rules.base

<a id="yasbd.rules.base.Rules"></a>

## Rules Objects

```python
class Rules()
```

<a id="yasbd.rules.base.Rules.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Initialize rule instance with lazy-compiled regex patterns.

Patterns are compiled once per class and cached via ``_REGEX_CACHED``.
Subclasses can override data constants (abbreviation sets, terminators, etc.)
and the classmethod ``_compile_regex_dynamically`` will pick them up.

<a id="yasbd.rules.base.Rules.apply"></a>

#### apply

```python
def apply(text: str, preserve_quote_and_paren: bool) -> list[int]
```

Detect sentence boundaries in *text*.

Two-pass algorithm:
1. Collect boundary candidates from punctuation positions.
2. Remove false alarms (mid-sentence abbreviations, ellipsis,
quote/paren spans, list markers).

**Arguments**:

- `text` - A string to find sentence boundaries in.
- `preserve_quote_and_paren` - If ``True``, suppress boundaries
  inside quote and parenthesis spans.
  

**Returns**:

  Sorted list of character offsets at which sentences end.

<a id="yasbd.rules.de"></a>

# yasbd.rules.de

<a id="yasbd.rules.en"></a>

# yasbd.rules.en

<a id="yasbd.rules.es"></a>

# yasbd.rules.es

<a id="yasbd.rules.fr"></a>

# yasbd.rules.fr

<a id="yasbd.rules.ht"></a>

# yasbd.rules.ht

<a id="yasbd.rules.ja"></a>

# yasbd.rules.ja

<a id="yasbd.rules.pt"></a>

# yasbd.rules.pt

<a id="yasbd.rules.ru"></a>

# yasbd.rules.ru

<a id="yasbd.rules.zh"></a>

# yasbd.rules.zh

<a id="yasbd.utils"></a>

# yasbd.utils

<a id="yasbd.utils.cleaner"></a>

# yasbd.utils.cleaner

<a id="yasbd.utils.cleaner.StreamCleaner"></a>

## StreamCleaner Objects

```python
class StreamCleaner(StreamCleanerStub)
```

Normalize and clean noisy text by applying ``ftfy``, HTML sanitization,
and various regex cleanup rules across paragraphs.

**Examples**:

  >>> list(StreamCleaner("Hello <b>world</b>. How are you?"))
  ['Hello <b>world</b>. How are you?']
  >>> list(StreamCleaner("<script>alert('xss')</script>clean text"))
  ['clean text']
  >>> list(StreamCleaner("<b>Hello</b> world", steps_to_skip=["unwrap_htmls"]))
  ['<b>Hello</b> world']
  >>> list(StreamCleaner("Text with ///slashes"))
  ['Text with slashes']
  >>> list(StreamCleaner("W\nO\nR\nD"))
  ['WORD']
  >>> list(StreamCleaner("An hyphe-\nnated sentence"))
  ['An hyphenated sentence']
  >>> list(StreamCleaner("Don't be naï-\nve"))
  ["Don't be naïve"]
  >>> list(StreamCleaner(""))
  []
  >>> StreamCleaner("Hello world", steps_to_skip=["nothing"])
  Traceback (most recent call last):
  ...
- `ValueError` - Invalid step(s) to skip: ...
  >>> list(StreamCleaner("Hello™ world", extra_steps=[lambda t: t.replace("™", "")]))
  ['Hello world']
  >>> list(StreamCleaner("hello", extra_steps=[lambda t: 1/0]))
  Traceback (most recent call last):
  ...
- `yasbd.exceptions.CleanStepError` - extra step '<lambda>' raised ZeroDivisionError (see above for details)

<a id="yasbd.utils.cleaner.StreamCleaner.__init__"></a>

#### \_\_init\_\_

```python
@validate_input
def __init__(source: str | TextIOBase,
             steps_to_skip: Collection[str] | None = None,
             extra_steps: Collection[Callable[[str], str]] | None = None,
             *,
             verbose: bool = False) -> None
```

Implements the iterator protocol. Yields cleaned paragraph strings.

**Arguments**:

- `source` - Plain text string or open text stream (e.g., ``StringIO``).
- `steps_to_skip` - A collection of steps to ignore. All steps will run if not provided.
  choices are:
  - fix_mojibake
  - fix_ocr_text
  - unwrap_htmls
  - normalize_slashes
  - normalize_spaces
- `extra_steps` - Optional user-defined cleaning functions, run after built-in steps.
  Each function must accept and return ``str``.
- `verbose` - Enable verbose logging.

<a id="yasbd.utils.input_validator"></a>

# yasbd.utils.input\_validator

<a id="yasbd.utils.input_validator.validate_input"></a>

#### validate\_input

```python
def validate_input(fn)
```

A decorator that validates function inputs and outputs

A wrapper around Pydantic's `validate_call` that catches `ValidationError`
and re-raises it as a more user-friendly `InvalidInputError`.

<a id="yasbd.utils.logger"></a>

# yasbd.utils.logger

<a id="yasbd.utils.logger.log_info"></a>

#### log\_info

```python
def log_info(verbose: bool, *args, **kwargs) -> None
```

Log an info message if verbose is enabled.

This is a convenience function that only logs when verbose mode is enabled,
avoiding unnecessary log output in production.

**Arguments**:

- `verbose` - If True, logs the message; if False, does nothing.
- `*args` - Positional arguments passed to logger.info().
- `**kwargs` - Keyword arguments passed to logger.info().
  

**Example**:

  >>> log_info(True, "hello {}", "world")
  >>> log_info(False, "This will not be logged")

<a id="yasbd.utils.paragraph_stream"></a>

# yasbd.utils.paragraph\_stream

<a id="yasbd.utils.paragraph_stream.ParagraphStream"></a>

## ParagraphStream Objects

```python
class ParagraphStream()
```

An iterator that groups lines of text into paragraph blocks.

This class implements Python's Iterator Protocol (__iter__ and __next__),
retaining state across calls and yielding reconstructed paragraph blocks.

**Examples**:

  >>> streamer = ParagraphStream('Hello\n\nWorld', skip_empty_lines=False)
  >>> list(streamer)
  ['Hello\n\n', 'World']
  
  >>> streamer = ParagraphStream('Hello\n\nWorld', skip_empty_lines=True)
  >>> list(streamer)
  ['Hello\n', 'World']

<a id="yasbd.utils.paragraph_stream.ParagraphStream.__init__"></a>

#### \_\_init\_\_

```python
def __init__(source: "str | TextIOBase | StreamCleaner",
             skip_empty_lines: bool = False) -> None
```

Initialize ParagraphStream.

**Arguments**:

- `source` - Input text as a string, ``TextIOBase`` stream, or ``StreamCleaner``.
- `skip_empty_lines` - If True, blank separator lines are omitted from paragraph blocks.

<a id="yasbd.utils.paragraph_stream.ParagraphStream.__next__"></a>

#### \_\_next\_\_

```python
def __next__() -> str
```

Advance the stream and return the next paragraph.

Yields paragraphs reconstructed as strings, preserving original line endings.

**Returns**:

  The next complete paragraph string.
  

**Raises**:

- `StopIteration` - When there are no more paragraphs to return.

<a id="yasbd.utils.pysbd_adapter"></a>

# yasbd.utils.pysbd\_adapter

<a id="yasbd.utils.pysbd_adapter.TextSpan"></a>

## TextSpan Objects

```python
class TextSpan()
```

A sentence with its character-offset span in the original text.

**Arguments**:

- `sent` - Sentence text.
- `start` - Start character offset of a sentence in original text.
- `end` - End character offset of a sentence in original text.

<a id="yasbd.utils.pysbd_adapter.Segmenter"></a>

## Segmenter Objects

```python
class Segmenter()
```

<a id="yasbd.utils.pysbd_adapter.Segmenter.__init__"></a>

#### \_\_init\_\_

```python
@validate_input
def __init__(language: str = "en",
             clean: bool = False,
             doc_type: str | None = None,
             char_span: bool = False)
```

Initializes the Segmenter.

**Arguments**:

- `language` - Two-character ISO 639-1 language code. Defaults to "en".
- `clean` - Whether to clean the original text. Defaults to False.
- `doc_type` - Normal text or OCRed text (e.g. "pdf"). Defaults to None.
- `char_span` - Whether to return character offset spans. Defaults to False.

<a id="yasbd.utils.pysbd_adapter.Segmenter.sentences_with_char_spans"></a>

#### sentences\_with\_char\_spans

```python
@validate_input
def sentences_with_char_spans(sentences: list[str]) -> list[TextSpan]
```

Map sentences to their char offsets using cumulative lengths.

Pysbd compatibility method

<a id="yasbd.utils.pysbd_adapter.Segmenter.segment"></a>

#### segment

```python
@validate_input
def segment(text: str) -> list[str | TextSpan]
```

Segments *text* into sentences.

**Arguments**:

- `text` - Raw text to be segmented into sentences.
  

**Returns**:

  A list of sentences (strings) by default, or a list of TextSpan
  objects if ``char_span`` was set to ``True``.

