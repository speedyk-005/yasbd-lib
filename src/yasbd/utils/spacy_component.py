try:  # pragma: no cover
    import spacy
    from spacy import __version__ as sp_ver

    if spacy.__version__.split(".")[0] < "3":
        raise ImportError(
            f"spaCy v3+ is required. You have v{sp_ver}. Upgrade with: pip install -U spacy"
        ) from None

    from spacy.language import Language
    from spacy.tokens import Doc
except ImportError:
    raise ImportError(
        "spaCy is required for the yasbd spaCy component. Install it with: pip install spacy"
    ) from None

from yasbd.boundary_detector import BoundaryDetector


class YasbdComponent:
    """A pipeline component for spaCy."""

    def __init__(
        self,
        lang: str,
        preserve_quote_and_paren: bool = True,
        verbose: bool = False,
    ):
        self.detector = BoundaryDetector(
            lang=lang,
            preserve_quote_and_paren=preserve_quote_and_paren,
            verbose=verbose,
        )

    def __call__(self, doc: Doc) -> Doc:
        """Assign sentence sent_ends using yasbd."""

        if not doc:
            return doc

        # Clear any existing sentence annotations.
        for token in doc:
            token.is_sent_start = False

        # The first token always starts the first sentence.
        doc[0].is_sent_start = True

        # Sync yasbd sentence boundary offsets with spaCy token indices.
        # Marks token.is_sent_start=True at the first token crossing each boundary.
        sent_ends = iter(self.detector.detect(doc.text))
        boundary = next(sent_ends, None)
        for token in doc[1:]:
            if boundary is not None and token.idx >= boundary:
                token.is_sent_start = True
                boundary = next(sent_ends, None)

        return doc


@Language.factory(
    "yasbd",
    default_config={
        "lang": None,
        "preserve_quote_and_paren": True,
        "verbose": False,
    },
)
def create_yasbd(
    nlp: Language,
    name: str,
    lang: str | None,
    preserve_quote_and_paren: bool,
    verbose: bool,
):
    """Create a spaCy component powered by yasbd."""
    return YasbdComponent(
        lang=lang,
        preserve_quote_and_paren=preserve_quote_and_paren,
        verbose=verbose,
    )


if __name__ == "__main__":  # pragma: no cover
    import spacy

    # Create a blank pipeline containing only a tokenizer.
    nlp = spacy.blank("en")

    nlp.add_pipe(
        "yasbd",
        first=True,
        config={
            "lang": "en",
            "preserve_quote_and_paren": True,
            "verbose": False,
        },
    )

    text = (
        "This is the first sentence of our document. "
        "It contains some text. "
        "The second sentence starts here. "
        "Dr. Smith said, 'Hello!'. "
        "Is this the third sentence? "
        "Yes, it is. "
        "And here is another one. "
        "With multiple sentences."
    )

    # Process the text using spaCy + yasbd.
    doc = nlp(text)
    for i, sent in enumerate(doc.sents, start=1):
        print(f"Sentence {i}: {sent.text!r}")

    # Retrieve the component instance and mutate yasbd at runtime.
    yasbd_pipe = nlp.get_pipe("yasbd")
    yasbd_pipe.detector.lang = "fr"
    yasbd_pipe.detector.verbose = True
    print("\nAfter mod:")
    print(yasbd_pipe)
    print(yasbd_pipe.lang)
