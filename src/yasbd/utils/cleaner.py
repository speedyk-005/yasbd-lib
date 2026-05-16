import io
import re
from collections.abc import Generator, Iterable

import ftfy

# https://regex101.com/r/SSQfUY/1
# A number followed by a latin-1/Slovak uppercase letter
STICKY_NUMBER_FINDER = re.compile(r"""
    (?<=\s\d\.)(?=[A-Z\u00C0-\u00D6\u00D8-\u00DE\u0100-\u017F])
    """, re.X
)

# https://regex101.com/r/POTL2H/3
HEADING_OR_LIST_FINDER = re.compile(r"^\s*[^\W_][.\-)*]\s*$")

# https://regex101.com/r/J5Cpyk/5
STANDALONE_CHARS_FINDER = re.compile(r"^\s*(?:[^\s]|\d{1,2})\s*$")

# https://regex101.com/r/pKi6y3/1
MULTIPLE_SPACES_FINDER = re.compile(r"\s{2,}")

# https://regex101.com/r/DgnxSq/1
PAGE_FINDER = re.compile(r"""
    Page\s+\d+\s+of\s+\d+.*|  # standalone page number
    -\s*\d+\s*-|  # Page numbers with dashes
    \s*\|\s*Page\s+\d+\s*\|\s*  # Boxed page numbers
    """, re.X | re.M,
)

# https://regex101.com/r/Gl4nLk/5
HTML_TAGS_FINDER = re.compile(r"""
    # Branch 1: Strip the tag AND its content
    <(script|iframe|object|embed|style)[^>]*?>.*?</?\1\s*>|

    # Branch 2: Just strip the brackets
    </?(?:img|font|header|span|xml|del|ins|[ovbtwxp])[^>]*?>
    """, re.X | re.I
)


# -- Ported from pysbd --

# https://regex101.com/r/Nw2I67/1
CONSECUTIVE_FORWARD_SLASH_FINDER = re.compile(r"\/{3}")

# https://regex101.com/r/Zo8RlK/2
INLINE_FORMATTING_FINDER = re.compile(r"{b\^>[^<]*<b\^}")

# If a line ends with one of these, the next line belongs to the same sentence.
# OCR often breaks lines mid-sentence, so this merges them back before
# the SBD engine sees the text.
CONTINUATION_CHARS = {"，", "：", "；", ",", "-", "*", ")", ":", ";"}


def _clean_text(text: str) -> str:
    if "<" in text:
        text = HTML_TAGS_FINDER.sub("", text)
    if "{" in text:
        text = INLINE_FORMATTING_FINDER.sub("", text)
    if "///" in text:
        text = CONSECUTIVE_FORWARD_SLASH_FINDER.sub("", text)

    text = STANDALONE_CHARS_FINDER.sub("", text)
    text = PAGE_FINDER.sub("", text)
    text = STICKY_NUMBER_FINDER.sub("\n", text)
    if "  " in text:
        text = MULTIPLE_SPACES_FINDER.sub(" ", text)
    return text


def clean_stream(data: Iterable[str]) -> Generator[str, None, None]:
    """Normalize and clean noisy text.

    Applies ``ftfy`` for mojibake repair, strips HTML tags, removes standalone
    characters, page-number artifacts, and re-joins list markers split across lines.

    NOTE: Plain strings are automatically wrapped into ``StringIO`` for streaming.

    Args:
        data: Iterable of raw text lines (or a plain string).

    Yields:
        Cleaned text lines.
    """
    if isinstance(data, str):
        data = io.StringIO(data)

    sent_buff = []   # To catch fragmented sentence
    for line in data:
        stripped_line = line.strip()
        if stripped_line:
            stripped_line = ftfy.fix_text(stripped_line)
            stripped_line = _clean_text(stripped_line)
            stripped_line = stripped_line.replace("''", '"')  # "Pseudo-Double" quote fix

            sent_buff.append(stripped_line)

            # Rejoin separated lists (e.g, 2\) from its content)
            if len(sent_buff) and HEADING_OR_LIST_FINDER.match(sent_buff[-1]):
                last_token = sent_buff.pop()
                yield from " ".join(sent_buff).splitlines()
                sent_buff = [last_token]

            if (
                sent_buff and sent_buff[-1]
                and not (sent_buff[-1][-1].isalpha() or sent_buff[-1][-1] in CONTINUATION_CHARS)
            ):
                yield from " ".join(sent_buff).splitlines()
                sent_buff = []

    if sent_buff:
        yield from " ".join(sent_buff).splitlines()


if __name__ == "__main__":
    texts = [
        "Hello <b>world</b>. How are you?",
        "Text with &lt;script&gt;evil&lt;/script&gt;",
        "line one\n. text two",
        "has {b^>inline<b^} formatting",
        "three///slashes",
        "1. ",
        "<font color=\"red\">Red text</font> and <span>span</span>",
        "<script>alert('xss')</script>clean text",
    ]

    for line in clean_stream(texts):
        print(repr(line))
