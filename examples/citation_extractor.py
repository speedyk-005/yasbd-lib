"""Extract academic citations sentence-by-sentence from a document.

Segments a text with yasbd, then finds citation mentions inside each
sentence: author-year forms (``Smith et al. (2020)``), parenthetical
multi-cites (``(Smith, 2020; Jones, 2019)``), bracket references
(``[2004]``), and locators (``p. 55``, ``pp. 128-129``).

Returns each citing sentence together with the citations found in it,
which is the usual input shape for reference linking and
citation-graph building.
"""

import re
from dataclasses import dataclass, field

from yasbd import BoundaryDetector

_detector = BoundaryDetector(lang="en")

CITATION_FINDER = re.compile(
    r"""
    (?:
        # 1. Author-year: "Smith et al. (2020)", "Smith et al. (2021, pp. 128-129)"
        [A-Z][\w\-']+(?:\s+(?:et\s+al\.|&\s+[A-Z][\w\-']+))?\s*\(\d{4}[^)]*\)
        |
        # 2. Parenthetical multi-cite: "(Smith, 2020; Jones, 2019; cf. Brown, 2018)"
        \([^()]*\b(?:19|20)\d{2}[^()]*\)
        |
        # 3. Bracket reference: "[2004]", "et al. [2004]"
        \[[^\[\]]*(?:19|20)\d{2}[^\[\]]*\]
        |
        # 4. Locators: "p. 55", "pp. 128-129", "p. 15"
        \bpp?\.?\s*\d+(?:\s*[-\u2013]\s*\d+)?
    )
    """,
    re.VERBOSE,
)


def _extract_citations(text: str, lang: str = "en") -> list[tuple[str, list[str]]]:
    """Return ``(sentence, citations)`` pairs for every citing sentence.

    Segments *text* into sentences with :class:`yasbd.BoundaryDetector`,
    then collects every citation mention inside each sentence. Sentences
    without citations are skipped.
    """

    _detector.lang = lang
    hits = []
    for sentence in _detector.segment(text):
        cites = CITATION_FINDER.findall(sentence)
        if cites:
            cleaned = CITATION_FINDER.sub("[...]", sentence)
            hits.append((cleaned, cites))
    return hits


@dataclass
class Citation:
    """A citation mention found in a document.

    Attributes:
        index: Position of this citation among all citations in the doc.
        sentence: The citing sentence, with citation spans masked as [...].
        sources: The citation strings found in the sentence.
    """

    index: int
    sentence: str
    sources: list[str] = field(default_factory=list)


class Doc:
    """A document with its citations extracted.

    Attributes:
        text: The raw document text.
        meta: Free-form metadata about the text (e.g. `{"page": 2}`).
        cit: The citations found in the text, in order.
    """

    def __init__(self, text: str, meta: dict | None = None, lang: str = "en") -> None:
        self.text = text
        self.meta = meta if meta is not None else {}
        self.cit = [
            Citation(index=i, sentence=sentence, sources=sources)
            for i, (sentence, sources) in enumerate(_extract_citations(text, lang=lang))
        ]


if __name__ == "__main__":
    paper = (
        "As Smith et al. (2021, pp. 128-129) noted: "
        '"The implications of this discovery are far-reaching '
        '(see also Jones & Lee, 2019; cf. Brown, 2018)." '
        "However, critics disagree (Miller, 2020). "
        "The proof is shown in eq. (7) and ex. IV. "
        "Further details appear on p. 55 of the supplement. "
        "No citations here, just background. "
        "Earlier work [2004] already hinted at this result."
    )
    doc = Doc(paper, meta={"page": 2})
    print(f"text: {doc.text[:40]}... (meta {doc.meta})")
    for cit in doc.cit:
        print(f"[{cit.index}] {cit.sentence}")
        for source in cit.sources:
            print(f"  - {source}")
