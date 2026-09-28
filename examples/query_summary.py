"""Extract query-focused summaries from documents using YASBD and BM25.

Prerequisites:
    pip install bm25s
"""

import bm25s

from yasbd import BoundaryDetector


class QuerySummary:
    """Extract sentences relevant to a query."""

    BM25_LANGS = {
        "en",
        "de",
        "nl",
        "fr",
        "es",
        "pt",
        "it",
        "ru",
        "sv",
        "no",
        "zh",
        "tr",
        "ko",
    }

    def __init__(self, lang: str = "en") -> None:
        """Initialize the query-focused summarizer."""
        self._lang = lang
        self._detector = BoundaryDetector(lang=lang)
        self._retriever = None
        self._sentences = []

    def index(self, text: str) -> None:
        """Segment and index a document."""
        self._sentences = list(
            self._detector.segment(text)
        )

        tokens = bm25s.tokenize(
            self._sentences,
            stopwords=self._lang
            if self._lang in self.BM25_LANGS
            else None,
        )

        self._retriever = bm25s.BM25()
        self._retriever.index(tokens)

    def search(self, query: str, k: int = 5) -> str:
        """Extract sentences relevant to a query."""
        query_tokens = bm25s.tokenize(
            query,
            stopwords=self._lang
            if self._lang in self.BM25_LANGS
            else None,
        )

        results, _ = self._retriever.retrieve(
            query_tokens,
            k=min(k, len(self._sentences)),
        )

        return " ".join(
            self._sentences[index]
            for index in results[0]
        )


if __name__ == "__main__":
    text = (
        "Python is a high-level programming language created by Guido van Rossum. "
        "Python was first released in 1991. "
        "The language emphasizes code readability and simplicity. "
        "Python is widely used for web development and automation. "
        "Many developers use Python for machine learning and data science. "
        "Programming languages allow humans to give instructions to computers. "
        "Programming requires concepts such as variables, functions, and loops. "
        "Software developers use many different programming languages."
    )

    summarizer = QuerySummary()
    summarizer.index(text)

    for query in ("Python", "programming"):
        print(f"\nQuery: {query}")
        print(summarizer.search(query, k=3))
