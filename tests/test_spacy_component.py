import pytest

spacy = pytest.importorskip("spacy", reason="spaCy not installed — skip spaCy component tests")

from yasbd import register_spacy_component  # noqa: E402

register_spacy_component()


@pytest.fixture(scope="module")
def nlp():
    """return a blank English pipeline with yasbd registered."""
    nlp = spacy.blank("en")
    nlp.add_pipe("yasbd", first=True, config={"lang": "en"})
    return nlp


def test_lang_defaults_to_pipeline_lang():
    """test that lang inherits from pipeline when not in config."""
    nlp = spacy.blank("en")
    nlp.add_pipe("yasbd", first=True)  # no config
    pipe = nlp.get_pipe("yasbd")
    assert pipe.detector.lang == "en"


def test_empty_doc(nlp):
    """test that empty text produces no sentences."""
    doc = nlp("")
    assert list(doc.sents) == []


def test_basic_segmentation(nlp):
    """test that yasbd correctly splits multi-sentence text via spaCy."""
    text = (
        "This is the first sentence of our document. "
        "It contains some text. "
        "The second sentence starts here. "
        "Dr. Smith said, 'Hello!'. "
        "Is this the fourth sentence? "
        "And here is another one. "
    )
    doc = nlp(text)
    sents = list(doc.sents)
    assert len(sents) == 6
    assert sents[0].text == "This is the first sentence of our document."
    assert sents[1].text == "It contains some text."
    assert sents[3].text == "Dr. Smith said, 'Hello!'."
    assert sents[4].text == "Is this the fourth sentence?"


def test_language_switch(nlp):
    """test that the component's detector language can be changed at runtime."""
    pipe = nlp.get_pipe("yasbd")
    assert pipe.detector.lang == "en"

    pipe.detector.lang = "fr"
    assert pipe.detector.lang == "fr"

    pipe.detector.lang = "es"
    assert pipe.detector.lang == "es"
