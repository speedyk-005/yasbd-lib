# Changelog

---

## [0.1.1] - Unreleased

### Fixed
- **Single-quote dialog**: No longer splits before the dialogue tag (e.g., `'Is this great?' she said.`). ([#23])
- **Ellipsis mid-thought**: Three-dot ellipsis (`...`) no longer splits mid-sentence. Only four dots are sentence boundaries.
- **Initialism detection**: Pronoun `I` no longer triggers false splits in names like `Albert I. Jones`.
- **N° reference**: Added to reference abbreviations to prevent split in `N°. 1026.253.553.`

### Changed
- **HORIZONTAL_LIST_FINDER**: Switched to `re2` for lookbehind support. Uses `\b` + negative lookbehind for capitalized words instead of requiring a terminator prefix. Supports other scripts via `\p{Ll}`.

---

## [0.1.0] - 2026-05-29

Initial release.

- **5 languages**: English, French, Spanish, Haitian Creole, Japanese
- **2-pass algorithm**: Pre-processing (double abbreviations, names, lists) + main split via lookbehind-based abbreviation guard
- **Performance**: ~16.5× faster than pysbd on 10.8K character benchmarks
- **pysbd adapter**: Drop-in `Segmenter` compatible with pysbd's API (`segment()`, `clean`, `char_span`)
- **Dual API**: `detect()` for raw boundary offsets, `segment()` for sentence strings with `TextSpan` support
- **Benchmarks**: 7-library comparison across 5 languages and 7 edge cases

[0.1.0]: https://github.com/speedyk-005/yasbd-lib/releases/tag/v0.1.0
[0.1.1]: https://github.com/speedyk-005/yasbd-lib/compare/v0.1.0...HEAD
[#23]: https://github.com/speedyk-005/yasbd-lib/issues/23
