from importlib.metadata import PackageNotFoundError, version

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

__all__ = [
    "BoundaryDetector",
    "ParagraphEOF",
    "CleanStepError",
    "InvalidInputError",
    "UnsupportedLanguageError",
    "YasbdError",
    "get_supported_langs",
    "__version__",
]
