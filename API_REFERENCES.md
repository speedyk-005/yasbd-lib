# `yasbd`

## Table of Contents

- 🅼 [yasbd](#yasbd)
- 🅼 [yasbd\.boundary\_detector](#yasbd-boundary_detector)
- 🅼 [yasbd\.cli](#yasbd-cli)
- 🅼 [yasbd\.exceptions](#yasbd-exceptions)
- 🅼 [yasbd\.rules](#yasbd-rules)
- 🅼 [yasbd\.rules\.ar](#yasbd-rules-ar)
- 🅼 [yasbd\.rules\.base](#yasbd-rules-base)
- 🅼 [yasbd\.rules\.de](#yasbd-rules-de)
- 🅼 [yasbd\.rules\.en](#yasbd-rules-en)
- 🅼 [yasbd\.rules\.es](#yasbd-rules-es)
- 🅼 [yasbd\.rules\.fr](#yasbd-rules-fr)
- 🅼 [yasbd\.rules\.ht](#yasbd-rules-ht)
- 🅼 [yasbd\.rules\.ja](#yasbd-rules-ja)
- 🅼 [yasbd\.rules\.pt](#yasbd-rules-pt)
- 🅼 [yasbd\.rules\.ru](#yasbd-rules-ru)
- 🅼 [yasbd\.rules\.zh](#yasbd-rules-zh)
- 🅼 [yasbd\.utils](#yasbd-utils)
- 🅼 [yasbd\.utils\.cleaner](#yasbd-utils-cleaner)
- 🅼 [yasbd\.utils\.cleaner\_stub](#yasbd-utils-cleaner_stub)
- 🅼 [yasbd\.utils\.input\_validator](#yasbd-utils-input_validator)
- 🅼 [yasbd\.utils\.paragraph\_stream](#yasbd-utils-paragraph_stream)
- 🅼 [yasbd\.utils\.pysbd\_adapter](#yasbd-utils-pysbd_adapter)

<a name="yasbd"></a>
## 🅼 yasbd

- **[Exports](#yasbd-exports)**

<a name="yasbd-exports"></a>
### Exports

- 🅼 [`BoundaryDetector`](#yasbd-BoundaryDetector)
- 🅼 [`ParagraphEOF`](#yasbd-ParagraphEOF)
- 🅼 [`InvalidInputError`](#yasbd-InvalidInputError)
- 🅼 [`UnsupportedLanguageError`](#yasbd-UnsupportedLanguageError)
- 🅼 [`YasbdError`](#yasbd-YasbdError)
- 🅼 [`get_supported_langs`](#yasbd-get_supported_langs)
- 🅼 [`__version__`](#yasbd-__version__)
<a name="yasbd-boundary_detector"></a>
## 🅼 yasbd\.boundary\_detector

- **Classes:**
  - 🅲 [BoundaryDetector](#yasbd-boundary_detector-BoundaryDetector)

### Classes

<a name="yasbd-boundary_detector-BoundaryDetector"></a>
### 🅲 yasbd\.boundary\_detector\.BoundaryDetector

```python
class BoundaryDetector:
```

**Functions:**

<a name="yasbd-boundary_detector-BoundaryDetector-__init__"></a>
#### 🅵 yasbd\.boundary\_detector\.BoundaryDetector\.\_\_init\_\_

```python
def __init__(self, lang: str = 'en', preserve_quote_and_paren: bool = True, verbose: bool = False):
```

Initialize the segmenter\.

**Parameters:**

- **lang**: Two chars ISO language code \(e\.g\. en, fr, \.\.\.\)\.
- **preserve_quote_and_paren**: Do not split on terminators inside
quoted or parenthesised text\.
- **verbose**: Enable verbose logging\.
<a name="yasbd-boundary_detector-BoundaryDetector-lang"></a>
#### 🅵 yasbd\.boundary\_detector\.BoundaryDetector\.lang

```python
def lang(self) -> str:
```

ISO language code of the active rule set\.
<a name="yasbd-boundary_detector-BoundaryDetector-lang"></a>
#### 🅵 yasbd\.boundary\_detector\.BoundaryDetector\.lang

```python
def lang(self, lang: str) -> None:
```
<a name="yasbd-boundary_detector-BoundaryDetector-detect"></a>
#### 🅵 yasbd\.boundary\_detector\.BoundaryDetector\.detect

```python
def detect(self, source: str | TextIOBase | StreamCleanerStub, relative: bool = False) -> Generator[int, None, None]:
```

Detect sentence boundaries in the source text\.

**Parameters:**

- **source**: Plain text string, an open text stream \(e\.g\., \`\`StringIO\`\`\),
or a \`\`StreamCleaner\`\` instance\.
- **relative**: If \`\`False\`\` \(default\), yields absolute character
offsets from the beginning of the entire stream\. If \`\`True\`\`,
offsets reset at each paragraph break, yielding indices relative
to the start of the current paragraph\.
<a name="yasbd-boundary_detector-BoundaryDetector-segment"></a>
#### 🅵 yasbd\.boundary\_detector\.BoundaryDetector\.segment

```python
def segment(self, source: str | TextIOBase | StreamCleanerStub, preserve_whitespace: bool = False) -> Generator[str, None, None]:
```

Split text into sentences\.

**Parameters:**

- **source**: Plain text string or \`\`TextIOBase\`\` stream
\(e\.g\., \`\`StringIO\`\`, opened file\)\.
- **preserve_whitespace**: If \`\`False\`\` \(default\), strip leading and
trailing whitespace from each sentence\.
<a name="yasbd-cli"></a>
## 🅼 yasbd\.cli

- **Functions:**
  - 🅵 [segment](#yasbd-cli-segment)
  - 🅵 [detect](#yasbd-cli-detect)
  - 🅵 [clean](#yasbd-cli-clean)
  - 🅵 [langs](#yasbd-cli-langs)
  - 🅵 [main](#yasbd-cli-main)

### Functions

<a name="yasbd-cli-segment"></a>
### 🅵 yasbd\.cli\.segment

```python
def segment(text: Optional[str] = None, file: Optional[str] = None, destination: Optional[str] = None, lang: str = 'en', preserve_whitespace: bool = False, verbose: bool = False):
```

Split text into sentences\.
<a name="yasbd-cli-detect"></a>
### 🅵 yasbd\.cli\.detect

```python
def detect(text: Optional[str] = None, file: Optional[str] = None, destination: Optional[str] = None, lang: str = 'en', relative: bool = False, verbose: bool = False):
```

Detect sentence boundary offsets \(character positions\)\.
<a name="yasbd-cli-clean"></a>
### 🅵 yasbd\.cli\.clean

```python
def clean(text: Optional[str] = None, file: Optional[str] = None, destination: Optional[str] = None, steps_to_skip: Optional[str] = None, verbose: bool = False):
```

Clean and normalize noisy text paragraphs\.
<a name="yasbd-cli-langs"></a>
### 🅵 yasbd\.cli\.langs

```python
def langs():
```

List supported language codes\.
<a name="yasbd-cli-main"></a>
### 🅵 yasbd\.cli\.main

```python
def main():
```
<a name="yasbd-exceptions"></a>
## 🅼 yasbd\.exceptions

- **Classes:**
  - 🅲 [YasbdError](#yasbd-exceptions-YasbdError)
  - 🅲 [UnsupportedLanguageError](#yasbd-exceptions-UnsupportedLanguageError)
  - 🅲 [InvalidInputError](#yasbd-exceptions-InvalidInputError)

### Classes

<a name="yasbd-exceptions-YasbdError"></a>
### 🅲 yasbd\.exceptions\.YasbdError

```python
class YasbdError(Exception):
```

Base exception for all yasbd errors\.
<a name="yasbd-exceptions-UnsupportedLanguageError"></a>
### 🅲 yasbd\.exceptions\.UnsupportedLanguageError

```python
class UnsupportedLanguageError(YasbdError, ValueError):
```

Raised when an unsupported language code is provided\.
<a name="yasbd-exceptions-InvalidInputError"></a>
### 🅲 yasbd\.exceptions\.InvalidInputError

```python
class InvalidInputError(YasbdError, TypeError):
```

Raised when invalid input\(s\) are encountered\.
<a name="yasbd-rules"></a>
## 🅼 yasbd\.rules

- **Functions:**
  - 🅵 [get\_supported\_langs](#yasbd-rules-get_supported_langs)

### Functions

<a name="yasbd-rules-get_supported_langs"></a>
### 🅵 yasbd\.rules\.get\_supported\_langs

```python
def get_supported_langs() -> list[str]:
```

Discover and cache supported language codes from the rules directory\.
<a name="yasbd-rules-ar"></a>
## 🅼 yasbd\.rules\.ar

- **Classes:**
  - 🅲 [ArRules](#yasbd-rules-ar-ArRules)

### Classes

<a name="yasbd-rules-ar-ArRules"></a>
### 🅲 yasbd\.rules\.ar\.ArRules

```python
class ArRules(Rules):
```
<a name="yasbd-rules-base"></a>
## 🅼 yasbd\.rules\.base

- **Classes:**
  - 🅲 [Rules](#yasbd-rules-base-Rules)

### Classes

<a name="yasbd-rules-base-Rules"></a>
### 🅲 yasbd\.rules\.base\.Rules

```python
class Rules:
```

**Functions:**

<a name="yasbd-rules-base-Rules-__init__"></a>
#### 🅵 yasbd\.rules\.base\.Rules\.\_\_init\_\_

```python
def __init__(self):
```

Initialize rule instance with lazy-compiled regex patterns\.

Patterns are compiled once per class and cached via \`\`\_REGEX\_CACHED\`\`\.
Subclasses can override data constants \(abbreviation sets, terminators, etc\.\)
and the classmethod \`\`\_compile\_regex\_dynamically\`\` will pick them up\.
<a name="yasbd-rules-base-Rules-apply"></a>
#### 🅵 yasbd\.rules\.base\.Rules\.apply

```python
def apply(self, text: str, preserve_quote_and_paren: bool) -> list[int]:
```

Detect sentence boundaries in \*text\*\.

Two-pass algorithm:
1\. Collect boundary candidates from punctuation positions\.
2\. Remove false alarms \(mid-sentence abbreviations, ellipsis,
   quote/paren spans, list markers\)\.

**Parameters:**

- **text**: A string to find sentence boundaries in\.
- **preserve_quote_and_paren**: If \`\`True\`\`, suppress boundaries
inside quote and parenthesis spans\.

**Returns:**

- Sorted list of character offsets at which sentences end\.
<a name="yasbd-rules-de"></a>
## 🅼 yasbd\.rules\.de

- **Classes:**
  - 🅲 [DeRules](#yasbd-rules-de-DeRules)

### Classes

<a name="yasbd-rules-de-DeRules"></a>
### 🅲 yasbd\.rules\.de\.DeRules

```python
class DeRules(Rules):
```
<a name="yasbd-rules-en"></a>
## 🅼 yasbd\.rules\.en

- **Classes:**
  - 🅲 [EnRules](#yasbd-rules-en-EnRules)

### Classes

<a name="yasbd-rules-en-EnRules"></a>
### 🅲 yasbd\.rules\.en\.EnRules

```python
class EnRules(Rules):
```
<a name="yasbd-rules-es"></a>
## 🅼 yasbd\.rules\.es

- **Classes:**
  - 🅲 [EsRules](#yasbd-rules-es-EsRules)

### Classes

<a name="yasbd-rules-es-EsRules"></a>
### 🅲 yasbd\.rules\.es\.EsRules

```python
class EsRules(Rules):
```
<a name="yasbd-rules-fr"></a>
## 🅼 yasbd\.rules\.fr

- **Classes:**
  - 🅲 [FrRules](#yasbd-rules-fr-FrRules)

### Classes

<a name="yasbd-rules-fr-FrRules"></a>
### 🅲 yasbd\.rules\.fr\.FrRules

```python
class FrRules(Rules):
```
<a name="yasbd-rules-ht"></a>
## 🅼 yasbd\.rules\.ht

- **Classes:**
  - 🅲 [HtRules](#yasbd-rules-ht-HtRules)

### Classes

<a name="yasbd-rules-ht-HtRules"></a>
### 🅲 yasbd\.rules\.ht\.HtRules

```python
class HtRules(Rules):
```
<a name="yasbd-rules-ja"></a>
## 🅼 yasbd\.rules\.ja

- **Classes:**
  - 🅲 [JaRules](#yasbd-rules-ja-JaRules)

### Classes

<a name="yasbd-rules-ja-JaRules"></a>
### 🅲 yasbd\.rules\.ja\.JaRules

```python
class JaRules(Rules):
```
<a name="yasbd-rules-pt"></a>
## 🅼 yasbd\.rules\.pt

- **Classes:**
  - 🅲 [PtRules](#yasbd-rules-pt-PtRules)

### Classes

<a name="yasbd-rules-pt-PtRules"></a>
### 🅲 yasbd\.rules\.pt\.PtRules

```python
class PtRules(Rules):
```
<a name="yasbd-rules-ru"></a>
## 🅼 yasbd\.rules\.ru

- **Classes:**
  - 🅲 [RuRules](#yasbd-rules-ru-RuRules)

### Classes

<a name="yasbd-rules-ru-RuRules"></a>
### 🅲 yasbd\.rules\.ru\.RuRules

```python
class RuRules(Rules):
```
<a name="yasbd-rules-zh"></a>
## 🅼 yasbd\.rules\.zh

- **Classes:**
  - 🅲 [ZhRules](#yasbd-rules-zh-ZhRules)

### Classes

<a name="yasbd-rules-zh-ZhRules"></a>
### 🅲 yasbd\.rules\.zh\.ZhRules

```python
class ZhRules(Rules):
```
<a name="yasbd-utils"></a>
## 🅼 yasbd\.utils
<a name="yasbd-utils-cleaner"></a>
## 🅼 yasbd\.utils\.cleaner

- **Constants:**
  - 🆅 [PREFIXES](#yasbd-utils-cleaner-PREFIXES)
  - 🆅 [HYPHENATED\_WORD\_FINDER](#yasbd-utils-cleaner-HYPHENATED_WORD_FINDER)
  - 🆅 [HEADING\_OR\_LIST\_FINDER](#yasbd-utils-cleaner-HEADING_OR_LIST_FINDER)
  - 🆅 [ARTIFACT\_FINDER](#yasbd-utils-cleaner-ARTIFACT_FINDER)
  - 🆅 [MULTIPLE\_SPACES\_FINDER](#yasbd-utils-cleaner-MULTIPLE_SPACES_FINDER)
  - 🆅 [PAGE\_FINDER](#yasbd-utils-cleaner-PAGE_FINDER)
  - 🆅 [HTML\_TAGS\_FINDER](#yasbd-utils-cleaner-HTML_TAGS_FINDER)
  - 🆅 [NEWLINE\_IN\_MIDDLE\_OF\_WORD\_FINDER](#yasbd-utils-cleaner-NEWLINE_IN_MIDDLE_OF_WORD_FINDER)
  - 🆅 [NEWLINE\_FOLLOWED\_BY\_PERIOD\_FINDER](#yasbd-utils-cleaner-NEWLINE_FOLLOWED_BY_PERIOD_FINDER)
  - 🆅 [NO\_SPACE\_BETWEEN\_SENTENCES\_FINDER](#yasbd-utils-cleaner-NO_SPACE_BETWEEN_SENTENCES_FINDER)
  - 🆅 [CONSECUTIVE\_FORWARD\_SLASH\_FINDER](#yasbd-utils-cleaner-CONSECUTIVE_FORWARD_SLASH_FINDER)
  - 🆅 [CLEANING\_PIPELINE](#yasbd-utils-cleaner-CLEANING_PIPELINE)
- **Classes:**
  - 🅲 [StreamCleaner](#yasbd-utils-cleaner-StreamCleaner)

### Constants

<a name="yasbd-utils-cleaner-PREFIXES"></a>
### 🆅 yasbd\.utils\.cleaner\.PREFIXES

```python
PREFIXES = {'hyper', 'ultra', 'super', 'extra', 'semi', 'multi', 'pre', 'post', 'ex', 'cross', 'inter', 'trans', 'anti', 'counter', 'non', 'quasi', 'self', 'auto', 'cyber', 'techno', 'electro', 'high', 'low', 'open', 'closed', 'up', 'down', 'off', 'mid', 'vice'}
```
<a name="yasbd-utils-cleaner-HYPHENATED_WORD_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.HYPHENATED\_WORD\_FINDER

```python
HYPHENATED_WORD_FINDER = re2.compile(f'\n    (?<=[{_vowels_pattern}]\\p{{M}}?-)\\s+(?=[{_vowels_pattern}])|\n    (?<=(?:{_suffix_pattern})-)\\s|\n    (?<!(?:{_suffix_pattern}))-\\s|\n', re2.X)
```
<a name="yasbd-utils-cleaner-HEADING_OR_LIST_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.HEADING\_OR\_LIST\_FINDER

```python
HEADING_OR_LIST_FINDER = re2.compile('(?<=^\\s?(?:[-•*+]|[\\w\\d][.)]))\\s*\\n', re2.M)
```
<a name="yasbd-utils-cleaner-ARTIFACT_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.ARTIFACT\_FINDER

```python
ARTIFACT_FINDER = re.compile('^\\s*[-•*+=#\\/\\\\_⯀∎]\\s*$', re.M)
```
<a name="yasbd-utils-cleaner-MULTIPLE_SPACES_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.MULTIPLE\_SPACES\_FINDER

```python
MULTIPLE_SPACES_FINDER = re.compile('\\s{2,}')
```
<a name="yasbd-utils-cleaner-PAGE_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.PAGE\_FINDER

```python
PAGE_FINDER = re.compile('\n    ^\\s*(?:\n        Page\\ \\d+\\ of\\ \\d+|  # Match "Page X of Y"\n        -\\s*\\d+\\s*-|          # Match "- X -"\n        \\|\\s*Page\\ \\d+\\s*\\|   # Match "| Page X |"\n    )\\s*$\n    ', re.X | re.M)
```
<a name="yasbd-utils-cleaner-HTML_TAGS_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.HTML\_TAGS\_FINDER

```python
HTML_TAGS_FINDER = re.compile('\n    # Branch 1: Strip the tag AND its content\n    <(script|img|iframe|object|embed|style|code)[^>]*?>.*?</\\1>|\n\n    # Branch 2: Just strip the brackets except quick formatting\n    </?\\b[^libu][^>]*?>\n    ', re.X | re.I | re.S)
```
<a name="yasbd-utils-cleaner-NEWLINE_IN_MIDDLE_OF_WORD_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.NEWLINE\_IN\_MIDDLE\_OF\_WORD\_FINDER

```python
NEWLINE_IN_MIDDLE_OF_WORD_FINDER = re2.compile('(?<=\\b[a-zA-Z]{1,2})\\n')
```
<a name="yasbd-utils-cleaner-NEWLINE_FOLLOWED_BY_PERIOD_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.NEWLINE\_FOLLOWED\_BY\_PERIOD\_FINDER

```python
NEWLINE_FOLLOWED_BY_PERIOD_FINDER = re.compile('\\n(?=\\.(?=\\s))')
```
<a name="yasbd-utils-cleaner-NO_SPACE_BETWEEN_SENTENCES_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.NO\_SPACE\_BETWEEN\_SENTENCES\_FINDER

```python
NO_SPACE_BETWEEN_SENTENCES_FINDER = re.compile('(?<=\\w\\.)(?=[A-Z][a-z])')
```
<a name="yasbd-utils-cleaner-CONSECUTIVE_FORWARD_SLASH_FINDER"></a>
### 🆅 yasbd\.utils\.cleaner\.CONSECUTIVE\_FORWARD\_SLASH\_FINDER

```python
CONSECUTIVE_FORWARD_SLASH_FINDER = re.compile('\\/{3}')
```
<a name="yasbd-utils-cleaner-CLEANING_PIPELINE"></a>
### 🆅 yasbd\.utils\.cleaner\.CLEANING\_PIPELINE

```python
CLEANING_PIPELINE = {'fix_mojibake': ftfy.fix_text, 'fix_ocr_text': _clean_ocr_text, 'unwrap_htmls': lambda t: t if '<' not in t else HTML_TAGS_FINDER.sub('', t), 'normalize_slashes': lambda t: t if '///' not in t else CONSECUTIVE_FORWARD_SLASH_FINDER.sub('', t), 'normalize_spaces': lambda t: t if ' ' not in t else MULTIPLE_SPACES_FINDER.sub(' ', t)}
```

### Classes

<a name="yasbd-utils-cleaner-StreamCleaner"></a>
### 🅲 yasbd\.utils\.cleaner\.StreamCleaner

```python
class StreamCleaner(StreamCleanerStub):
```

Normalize and clean noisy text by applying \`\`ftfy\`\`, HTML sanitization,

and various regex cleanup rules across paragraphs\.

**Functions:**

<a name="yasbd-utils-cleaner-StreamCleaner-__init__"></a>
#### 🅵 yasbd\.utils\.cleaner\.StreamCleaner\.\_\_init\_\_

```python
def __init__(self, source: str | TextIOBase, steps_to_skip: Collection[str] | None = None) -> None:
```

Implements the iterator protocol\. Yields cleaned paragraph strings\.

**Parameters:**

- **source**: Plain text string or open text stream \(e\.g\., \`\`StringIO\`\`\)\.
- **steps_to_skip**: A collection of steps to ignore\. All steps will run if not provided\.
choices are:
- fix\_mojibake
- fix\_ocr\_text
- unwrap\_htmls
- normalize\_slashes
- normalize\_spaces
<a name="yasbd-utils-cleaner-StreamCleaner-__iter__"></a>
#### 🅵 yasbd\.utils\.cleaner\.StreamCleaner\.\_\_iter\_\_

```python
def __iter__(self) -> Iterator[str]:
```
<a name="yasbd-utils-cleaner-StreamCleaner-__next__"></a>
#### 🅵 yasbd\.utils\.cleaner\.StreamCleaner\.\_\_next\_\_

```python
def __next__(self) -> str:
```
<a name="yasbd-utils-cleaner_stub"></a>
## 🅼 yasbd\.utils\.cleaner\_stub

- **Classes:**
  - 🅲 [StreamCleanerStub](#yasbd-utils-cleaner_stub-StreamCleanerStub)

### Classes

<a name="yasbd-utils-cleaner_stub-StreamCleanerStub"></a>
### 🅲 yasbd\.utils\.cleaner\_stub\.StreamCleanerStub

```python
class StreamCleanerStub:
```

Runtime validation and type marker for StreamCleaner-like inputs\.

Used as a lightweight contract anchor for runtime checks and type hints
where Protocols are not supported by the validation system\.

This class provides no functionality\.
<a name="yasbd-utils-input_validator"></a>
## 🅼 yasbd\.utils\.input\_validator

- **Functions:**
  - 🅵 [validate\_input](#yasbd-utils-input_validator-validate_input)

### Functions

<a name="yasbd-utils-input_validator-validate_input"></a>
### 🅵 yasbd\.utils\.input\_validator\.validate\_input

```python
def validate_input(fn):
```

A decorator that validates function inputs and outputs

A wrapper around Pydantic's \`validate\_call\` that catches \`ValidationError\`
and re-raises it as a more user-friendly \`InvalidInputError\`\.
<a name="yasbd-utils-paragraph_stream"></a>
## 🅼 yasbd\.utils\.paragraph\_stream

- **Classes:**
  - 🅲 [ParagraphStream](#yasbd-utils-paragraph_stream-ParagraphStream)

### Classes

<a name="yasbd-utils-paragraph_stream-ParagraphStream"></a>
### 🅲 yasbd\.utils\.paragraph\_stream\.ParagraphStream

```python
class ParagraphStream:
```

An iterator that groups lines of text into paragraph blocks\.

This class implements Python's Iterator Protocol \(\_\_iter\_\_ and \_\_next\_\_\),
retaining state across calls and yielding reconstructed paragraph blocks\.

**Functions:**

<a name="yasbd-utils-paragraph_stream-ParagraphStream-__init__"></a>
#### 🅵 yasbd\.utils\.paragraph\_stream\.ParagraphStream\.\_\_init\_\_

```python
def __init__(self, source: 'str | TextIOBase | StreamCleaner', skip_empty_lines: bool = False) -> None:
```

Initialize ParagraphStream\.

**Parameters:**

- **source**: Input text as a string, \`\`TextIOBase\`\` stream, or \`\`StreamCleaner\`\`\.
- **skip_empty_lines**: If True, blank separator lines are omitted from paragraph blocks\.
<a name="yasbd-utils-paragraph_stream-ParagraphStream-__iter__"></a>
#### 🅵 yasbd\.utils\.paragraph\_stream\.ParagraphStream\.\_\_iter\_\_

```python
def __iter__(self) -> Iterator[str]:
```
<a name="yasbd-utils-paragraph_stream-ParagraphStream-__next__"></a>
#### 🅵 yasbd\.utils\.paragraph\_stream\.ParagraphStream\.\_\_next\_\_

```python
def __next__(self) -> str:
```

Advance the stream and return the next paragraph\.

Yields paragraphs reconstructed as strings, preserving original line endings\.

**Returns:**

- The next complete paragraph string\.

**Raises:**

- **StopIteration**: When there are no more paragraphs to return\.
<a name="yasbd-utils-pysbd_adapter"></a>
## 🅼 yasbd\.utils\.pysbd\_adapter

- **Classes:**
  - 🅲 [TextSpan](#yasbd-utils-pysbd_adapter-TextSpan)
  - 🅲 [Segmenter](#yasbd-utils-pysbd_adapter-Segmenter)

### Classes

<a name="yasbd-utils-pysbd_adapter-TextSpan"></a>
### 🅲 yasbd\.utils\.pysbd\_adapter\.TextSpan

```python
class TextSpan:
```

A sentence with its character-offset span in the original text\.

**Parameters:**

- **sent**: Sentence text\.
- **start**: Start character offset of a sentence in original text\.
- **end**: End character offset of a sentence in original text\.

**Functions:**

<a name="yasbd-utils-pysbd_adapter-TextSpan-__init__"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.TextSpan\.\_\_init\_\_

```python
def __init__(self, sent, start, end):
```
<a name="yasbd-utils-pysbd_adapter-TextSpan-__str__"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.TextSpan\.\_\_str\_\_

```python
def __str__(self) -> str:
```
<a name="yasbd-utils-pysbd_adapter-TextSpan-__eq__"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.TextSpan\.\_\_eq\_\_

```python
def __eq__(self, other) -> bool:
```
<a name="yasbd-utils-pysbd_adapter-Segmenter"></a>
### 🅲 yasbd\.utils\.pysbd\_adapter\.Segmenter

```python
class Segmenter:
```

**Functions:**

<a name="yasbd-utils-pysbd_adapter-Segmenter-__init__"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.Segmenter\.\_\_init\_\_

```python
def __init__(self, language: str = 'en', clean: bool = False, doc_type: str | None = None, char_span: bool = False):
```

Initializes the Segmenter\.

**Parameters:**

- **language** (default: `"en"`): Two-character ISO 639-1 language code\. Defaults to "en"\.
- **clean** (default: `False`): Whether to clean the original text\. Defaults to False\.
- **doc_type** (default: `None`): Normal text or OCRed text \(e\.g\. "pdf"\)\. Defaults to None\.
- **char_span** (default: `False`): Whether to return character offset spans\. Defaults to False\.
<a name="yasbd-utils-pysbd_adapter-Segmenter-language"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.Segmenter\.language

```python
def language(self) -> str:
```
<a name="yasbd-utils-pysbd_adapter-Segmenter-language"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.Segmenter\.language

```python
def language(self, value: str):
```
<a name="yasbd-utils-pysbd_adapter-Segmenter-sentences_with_char_spans"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.Segmenter\.sentences\_with\_char\_spans

```python
def sentences_with_char_spans(self, sentences: list[str]) -> list[TextSpan]:
```

Map sentences to their char offsets using cumulative lengths\.

Pysbd compatibility method
<a name="yasbd-utils-pysbd_adapter-Segmenter-segment"></a>
#### 🅵 yasbd\.utils\.pysbd\_adapter\.Segmenter\.segment

```python
def segment(self, text: str) -> list[str | TextSpan]:
```

Segments \*text\* into sentences\.

**Parameters:**

- **text**: Raw text to be segmented into sentences\.

**Returns:**

- A list of sentences \(strings\) by default, or a list of TextSpan
objects if \`\`char\_span\`\` was set to \`\`True\`\`\.
