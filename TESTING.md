# Testing

Run the cleaning steps tests:

```bash
cd /data/data/com.termux/files/home/.openclaw/workspace/yasbd-lib
python -m pytest tests/test_cleaning_steps.py -v
```

## Coverage

The tests cover the three named cleaning functions that were extracted from the `DEFAULT_CLEANING_PIPELINE`:

- `unwrap_htmls`: Removes HTML tags, preserving `<b>`, `<i>`, and `<u>` tags
- `normalize_slashes`: Replaces triple forward slashes with single slashes
- `normalize_spaces`: Reduces consecutive whitespace to a single space

## Local Development

Tests can be run directly from the repository root:

```bash
# From workspace root
python -m pytest yasbd-lib/tests/test_cleaning_steps.py -v
```

Note: Tests may encounter permission issues due to environment constraints. Check `/proc/self/cwd` for current working directory if encountering permission errors.