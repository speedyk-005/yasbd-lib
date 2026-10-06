from retrie.trie import Trie

from yasbd.utils.input_validator import validate_inputs


def build_optimized_pattern(options: set[str] | list[str] | tuple[str, ...]) -> str:
    """Build an optimised and escaped regex alternation pattern.

    Returns a never-match pattern if no valid options exist.
    Ref: https://stackoverflow.com/questions/1723182/a-regex-that-will-never-be-matched-by-anything?
    """
    validate_inputs([(options, (list, set, tuple))])

    if not options:
        return r"(?!)"

    trie = Trie()
    return trie.add(*options).pattern()
