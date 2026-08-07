import pytest

from yasbd.utils.cleaner import StreamCleaner


def test_stream_cleaner_preserves_consecutive_slashes():
    """Verify StreamCleaner does not delete /// slashes or glue words together."""
    text1 = "a///b"
    assert list(StreamCleaner(text1)) == ["a///b"]

    text2 = "Text with ///slashes"
    assert list(StreamCleaner(text2)) == ["Text with ///slashes"]

    url_text = "file:///C:/Users/test/doc.txt"
    assert list(StreamCleaner(url_text)) == ["file:///C:/Users/test/doc.txt"]

    rust_doc = "/// This is a Rust doc comment"
    assert list(StreamCleaner(rust_doc)) == ["/// This is a Rust doc comment"]


def test_stream_cleaner_default_pipeline():
    """Test standard StreamCleaner operations like HTML unwrapping and space normalization."""
    html_text = "Hello <b>world</b>. <script>alert(1)</script>Clean text."
    assert list(StreamCleaner(html_text)) == ["Hello <b>world</b>. Clean text."]

    space_text = "Multiple    spaces   here."
    assert list(StreamCleaner(space_text)) == ["Multiple spaces here."]


def test_stream_cleaner_extra_steps_and_skip():
    """Test custom extra steps and skipping built-in steps."""
    text = "Hello  world"
    cleaner = StreamCleaner(text, steps_to_skip=["normalize_spaces"])
    assert list(cleaner) == ["Hello  world"]

    cleaner_extra = StreamCleaner("hello", extra_steps=[lambda t: t.upper()])
    assert list(cleaner_extra) == ["HELLO"]
