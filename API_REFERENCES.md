# Table of Contents

* [yasbd](#yasbd)
  * [register\_spacy\_component](#yasbd.register_spacy_component)
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
  * [LangPackError](#yasbd.exceptions.LangPackError)
  * [CleanStepError](#yasbd.exceptions.CleanStepError)
* [yasbd.rules](#yasbd.rules)
  * [register\_lang\_packs](#yasbd.rules.register_lang_packs)
  * [clear\_lang\_packs](#yasbd.rules.clear_lang_packs)
  * [get\_supported\_langs](#yasbd.rules.get_supported_langs)
  * [load\_rule](#yasbd.rules.load_rule)
* [yasbd.rules.am](#yasbd.rules.am)
* [yasbd.rules.ar](#yasbd.rules.ar)
* [yasbd.rules.base](#yasbd.rules.base)
  * [Rules](#yasbd.rules.base.Rules)
    * [\_\_init\_\_](#yasbd.rules.base.Rules.__init__)
    * [apply](#yasbd.rules.base.Rules.apply)
* [yasbd.rules.de](#yasbd.rules.de)
* [yasbd.rules.el](#yasbd.rules.el)
* [yasbd.rules.en](#yasbd.rules.en)
* [yasbd.rules.es](#yasbd.rules.es)
* [yasbd.rules.fr](#yasbd.rules.fr)
* [yasbd.rules.hi](#yasbd.rules.hi)
* [yasbd.rules.ht](#yasbd.rules.ht)
* [yasbd.rules.it](#yasbd.rules.it)
* [yasbd.rules.ja](#yasbd.rules.ja)
* [yasbd.rules.ko](#yasbd.rules.ko)
* [yasbd.rules.my](#yasbd.rules.my)
* [yasbd.rules.nl](#yasbd.rules.nl)
* [yasbd.rules.pt](#yasbd.rules.pt)
* [yasbd.rules.ru](#yasbd.rules.ru)
* [yasbd.rules.th](#yasbd.rules.th)
* [yasbd.rules.zh](#yasbd.rules.zh)
* [yasbd.utils](#yasbd.utils)
* [yasbd.utils.cleaner](#yasbd.utils.cleaner)
  * [StreamCleaner](#yasbd.utils.cleaner.StreamCleaner)
    * [\_\_init\_\_](#yasbd.utils.cleaner.StreamCleaner.__init__)
* [yasbd.utils.input\_validator](#yasbd.utils.input_validator)
  * [validate\_input](#yasbd.utils.input_validator.validate_input)
* [yasbd.utils.lang\_code\_normalizer](#yasbd.utils.lang_code_normalizer)
  * [normalize\_lang](#yasbd.utils.lang_code_normalizer.normalize_lang)
* [yasbd.utils.language\_classifier](#yasbd.utils.language_classifier)
  * [classify\_language](#yasbd.utils.language_classifier.classify_language)
* [yasbd.utils.logger](#yasbd.utils.logger)
  * [log\_info](#yasbd.utils.logger.log_info)
* [yasbd.utils.paragraph\_stream](#yasbd.utils.paragraph_stream)
  * [ParagraphStream](#yasbd.utils.paragraph_stream.ParagraphStream)
    * [\_\_init\_\_](#yasbd.utils.paragraph_stream.ParagraphStream.__init__)
    * [\_\_next\_\_](#yasbd.utils.paragraph_stream.ParagraphStream.__next__)
    * [close](#yasbd.utils.paragraph_stream.ParagraphStream.close)
* [yasbd.utils.pysbd\_adapter](#yasbd.utils.pysbd_adapter)
  * [TextSpan](#yasbd.utils.pysbd_adapter.TextSpan)
  * [Segmenter](#yasbd.utils.pysbd_adapter.Segmenter)
    * [\_\_init\_\_](#yasbd.utils.pysbd_adapter.Segmenter.__init__)
    * [sentences\_with\_char\_spans](#yasbd.utils.pysbd_adapter.Segmenter.sentences_with_char_spans)
    * [segment](#yasbd.utils.pysbd_adapter.Segmenter.segment)
* [yasbd.utils.spacy\_component](#yasbd.utils.spacy_component)
  * [YasbdComponent](#yasbd.utils.spacy_component.YasbdComponent)
    * [\_\_call\_\_](#yasbd.utils.spacy_component.YasbdComponent.__call__)
  * [create\_yasbd](#yasbd.utils.spacy_component.create_yasbd)

<a id="yasbd"></a>

# yasbd

<a id="yasbd.register_spacy_component"></a>

#### register\_spacy\_component

```python
def register_spacy_component()
```

Register the yasbd spaCy pipeline component on demand.

Call this to add the ``yasbd`` component factory to spaCy's registry.
Requires spaCy v3+ to be installed.

Examples
--------
>>> import spacy
>>> from yasbd import register_spacy_component
>>> register_spacy_component()
>>> nlp = spacy.blank("en")
>>> nlp.add_pipe("yasbd", first=True, config={"lang": "en"})

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
def __init__(lang: str | None = None,
             *,
             preserve_quote_and_paren: bool = True,
             verbose: bool = False)
```

Initialize the segmenter.

**Arguments**:

- `lang` - Two chars ISO language code (e.g., 'en', 'fr', ...).
  Use 'auto' for automatic language detection via py3langid.
  Explicit is faster and more reliable; use auto if you don't
  mind a slight decrease in both.
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

<a id="yasbd.exceptions.LangPackError"></a>

## LangPackError Objects

```python
class LangPackError(YasbdError)
```

Raised when a language pack module fails validation or handshake.

<a id="yasbd.exceptions.CleanStepError"></a>

## CleanStepError Objects

```python
class CleanStepError(YasbdError, TypeError)
```

Raised when a StreamCleaner extra step fails (non-callable or non-str return).

<a id="yasbd.rules"></a>

# yasbd.rules

<a id="yasbd.rules.register_lang_packs"></a>

#### register\_lang\_packs

```python
@validate_input
def register_lang_packs(names: list[str]) -> None
```

Import and validate external language pack modules.

Each module must expose a ``PROFILES`` list of ``Rules`` subclasses.
All validated profiles are stored in ``_LANG_PACK_REGISTRY``.

Caution:
This function imports arbitrary Python modules by name. Only load lang
packs from sources you trust — an untrusted module can execute
arbitrary code at import time.

**Arguments**:

- `names` - Module names resolvable from the Python path
  (e.g. ``["yasbd_indic", "yasbd_legal"]``).
  

**Raises**:

- `LangPackError` - If a language pack module cannot be imported.

<a id="yasbd.rules.clear_lang_packs"></a>

#### clear\_lang\_packs

```python
def clear_lang_packs() -> None
```

Remove all registered language packs and reset the supported-languages cache.

<a id="yasbd.rules.get_supported_langs"></a>

#### get\_supported\_langs

```python
@cache
def get_supported_langs() -> list[str]
```

Discover and cache supported language codes.

Returns a sorted list of ``auto`` plus all language codes from
the built-in rules directory and any registered language packs.

<a id="yasbd.rules.load_rule"></a>

#### load\_rule

```python
def load_rule(lang: str, verbose: bool = False) -> Rules
```

Import and instantiate the rule module for *lang*.

Checks the language pack registry first; falls back to the built-in rules directory.

**Returns**:

  The instantiated rule object.
  

**Raises**:

- `UnsupportedLanguageError` - If no rule module exists for *lang*.

<a id="yasbd.rules.am"></a>

# yasbd.rules.am

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

<a id="yasbd.rules.el"></a>

# yasbd.rules.el

<a id="yasbd.rules.en"></a>

# yasbd.rules.en

<a id="yasbd.rules.es"></a>

# yasbd.rules.es

<a id="yasbd.rules.fr"></a>

# yasbd.rules.fr

<a id="yasbd.rules.hi"></a>

# yasbd.rules.hi

<a id="yasbd.rules.ht"></a>

# yasbd.rules.ht

<a id="yasbd.rules.it"></a>

# yasbd.rules.it

<a id="yasbd.rules.ja"></a>

# yasbd.rules.ja

<a id="yasbd.rules.ko"></a>

# yasbd.rules.ko

<a id="yasbd.rules.my"></a>

# yasbd.rules.my

<a id="yasbd.rules.nl"></a>

# yasbd.rules.nl

<a id="yasbd.rules.pt"></a>

# yasbd.rules.pt

<a id="yasbd.rules.ru"></a>

# yasbd.rules.ru

<a id="yasbd.rules.th"></a>

# yasbd.rules.th

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
- `yasbd.exceptions.InvalidInputError` - 🧩 Oops! Unknown step(s): 'nothing'...
  >>> list(StreamCleaner("Hello™ world", extra_steps=[lambda t: t.replace("™", "")]))
  ['Hello world']
  >>> list(StreamCleaner("hello", extra_steps=[lambda t: 1/0]))
  Traceback (most recent call last):
  ...
- `yasbd.exceptions.CleanStepError` - extra step '<lambda>' raised an error.
- `Details` - division by zero

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
def validate_input(fn: F) -> F
```

Validate function arguments and return values using beartype.

<a id="yasbd.utils.lang_code_normalizer"></a>

# yasbd.utils.lang\_code\_normalizer

<a id="yasbd.utils.lang_code_normalizer.normalize_lang"></a>

#### normalize\_lang

```python
@validate_input
def normalize_lang(lang_code: str) -> str
```

Normalize a language tag to an ISO-639-1 language code.

The helper is explicit and opt-in. It does not alter the core
``BoundaryDetector`` language handling.

**Examples**:

  
  >>> normalize_lang("EN")
  'en'
  >>> normalize_lang("en-US")
  'en'
  >>> normalize_lang("en-Latn")
  'en'
  >>> normalize_lang("pt-BR")
  'pt'
  >>> normalize_lang("")
  ''
  >>> normalize_lang("   ")
  ''
  >>> normalize_lang("not-a-language-code")  # doctest: +ELLIPSIS
  Traceback (most recent call last):
  ...
- `yasbd.exceptions.InvalidInputError` - ...
  >>> normalize_lang("akk")  # doctest: +ELLIPSIS
  Traceback (most recent call last):
  ...
- `yasbd.exceptions.InvalidInputError` - ...
  

**Arguments**:

- `lang_code` - A language code or tag, such as ``"EN"``, ``"en-US"``,
  or ``"en-Latn"``.
  

**Returns**:

  A two-letter ISO-639-1 language code, or an empty string if empty input.
  

**Raises**:

- `ImportError` - If the optional ``langcodes`` dependency is missing.
- `InvalidInputError` - If the tag cannot be parsed or does not resolve to a
  two-letter ISO-639-1 language code.

<a id="yasbd.utils.language_classifier"></a>

# yasbd.utils.language\_classifier

<a id="yasbd.utils.language_classifier.classify_language"></a>

#### classify\_language

```python
@lru_cache(maxsize=12)
def classify_language(text: str) -> tuple[str, float]
```

Classify text with a preference for expected languages.

This function avoids the explicit ``py3langid.LanguageIdentifier`` initialization
and its associated cold-start cost by relying on this convenience API.

The algorithm works as follows:
1. Obtain the ranked language predictions.
2. Look for preferred languages within the top ``TOP_K`` results.
3. Only consider preferred languages whose score is within
``MAX_GAP`` of the top prediction.
4. If no suitable preferred language is found, fall back to all
ranked candidates.
5. Compute a normalized confidence score using a softmax over the
selected candidates.

**Arguments**:

- `text` - The text to classify.
  

**Returns**:

  A tuple containing:
  - The predicted ISO 639-1 language code.
  - A confidence score between 0.0 and 1.0.
  

**Examples**:

  >>> language, confidence = classify_language("kiyès ?")
  >>> language
  'ht'
  >>> 0.0 <= confidence <= 1.0
  True
  

**Raises**:

- `ValueError` - If the detector returns no language scores.

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
@validate_input
def __init__(source: str | TextIOBase | StreamCleanerStub,
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

<a id="yasbd.utils.paragraph_stream.ParagraphStream.close"></a>

#### close

```python
def close() -> None
```

Close the underlying source stream if applicable.

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

<a id="yasbd.utils.spacy_component"></a>

# yasbd.utils.spacy\_component

<a id="yasbd.utils.spacy_component.YasbdComponent"></a>

## YasbdComponent Objects

```python
class YasbdComponent()
```

A pipeline component for spaCy.

<a id="yasbd.utils.spacy_component.YasbdComponent.__call__"></a>

#### \_\_call\_\_

```python
def __call__(doc: Doc) -> Doc
```

Assign sentence sent_ends using yasbd.

<a id="yasbd.utils.spacy_component.create_yasbd"></a>

#### create\_yasbd

```python
@Language.factory(
    "yasbd",
    default_config={
        "lang": None,
        "preserve_quote_and_paren": True,
        "verbose": False,
    },
)
def create_yasbd(nlp: Language, name: str, lang: str | None,
                 preserve_quote_and_paren: bool, verbose: bool)
```

Create a spaCy component powered by yasbd.

