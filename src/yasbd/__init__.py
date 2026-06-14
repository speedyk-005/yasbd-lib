from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from yasbd.boundary_detector import BoundaryDetector
from yasbd.boundary_detector import ParagraphEOF
from yasbd.exceptions import CleanStepError
from yasbd.exceptions import InvalidInputError
from yasbd.exceptions import UnsupportedLanguageError
from yasbd.exceptions import YasbdError
from yasbd.rules import get_supported_langs

try:
    __version__ = version("yasbd-lib")
except PackageNotFoundError:
    __version__ = "unknown"


def register_spacy_component():
    """Register the yasbd spaCy pipeline component on demand.

    Call this to add the ``yasbd`` component factory to spaCy's registry.
    Requires spaCy v3+ to be installed.

    Examples
    --------
    >>> import spacy
    >>> from yasbd import register_spacy_component
    >>> register_spacy_component()
    >>> nlp = spacy.blank("en")
    >>> nlp.add_pipe("yasbd", first=True, config={"lang": "en"})
    """
    from yasbd.utils.spacy_component import create_yasbd  # noqa: F401


# Expose utils submodules at package root level so both
#   from yasbd.utils.cleaner import StreamCleaner   (legacy)
#   from yasbd.cleaner import StreamCleaner          (flat)
# work without changing the physical file layout.
_utils_path = str(Path(__file__).parent / "utils")
if _utils_path not in __path__:
    __path__.append(_utils_path)

__all__ = [
    "BoundaryDetector",
    "ParagraphEOF",
    "CleanStepError",
    "InvalidInputError",
    "UnsupportedLanguageError",
    "YasbdError",
    "get_supported_langs",
    "register_spacy_component",
    "__version__",
]
