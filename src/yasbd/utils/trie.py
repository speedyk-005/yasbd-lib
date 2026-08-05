from retrie.trie import Trie


def build_optimized_pattern(options: set[str]) -> str:
    """Build an optimised and escaped regex alternation pattern.

    Returns a never-match pattern if no valid options exist.
    Ref: https://stackoverflow.com/questions/1723182/a-regex-that-will-never-be-matched-by-anything?
    """
    if not options:
        return r"(?!)"

    trie = Trie()
    return trie.add(*options).pattern()
