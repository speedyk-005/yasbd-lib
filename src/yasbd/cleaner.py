import re
import io
from collections.abc import Iterator

import ftfy


# https://regex101.com/r/SSQfUY/1
# A number followed by a latin-1/Slovak uppercase letter
STICKY_NUMBER_SPLITTER = re.compile(r"""
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

# Rubular: http://rubular.com/r/IQ4TPfsbd8
CONSECUTIVE_FORWARD_SLASH_FINDER = re.compile(r"\/{3}")

# Rubular: http://rubular.com/r/FseyMiiYFT
NEWLINE_FOLLOWED_BY_PERIOD_FINDER = re.compile(r"\n(?=\.(\s|\n))")

# Rubular: http://rubular.com/r/bAJrhyLNeZ (original)
# https://regex101.com/r/Zo8RlK/1 (modified)
INLINE_FORMATTING_FINDER = re.compile(r"{b\^&gt;[^<]*&lt;b\^}|{b\^>[^<]*<b\^}")


def _clean_text(text: str) -> str:
    if "<" in text:
        text = HTML_TAGS_FINDER.sub("", text)
    if "{" in text:
        text = INLINE_FORMATTING_FINDER.sub("", text)
    if "///" in text:
        text = CONSECUTIVE_FORWARD_SLASH_FINDER.sub("", text)

    text = STANDALONE_CHARS_FINDER.sub("", text)
    text = PAGE_FINDER.sub("", text)

    if "\n" in text:
        text = NEWLINE_FOLLOWED_BY_PERIOD_FINDER.sub("", text)
    text = STICKY_NUMBER_SPLITTER.sub("\n", text)
    if "  " in text:
        text = MULTIPLE_SPACES_FINDER.sub(" ", text)
    return text


def clean_input(data: io.IOBase | Iterator) -> Iterator[str]:
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
                last_tok = sent_buff.pop()
                yield from " ".join(sent_buff).splitlines()
                sent_buff = [last_tok]

            if (
                sent_buff and sent_buff[-1]
                and not (sent_buff[-1][-1].isalpha() or sent_buff[-1][-1] in ".-*)")
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

    for line in clean_input(texts):
        print(repr(line))
