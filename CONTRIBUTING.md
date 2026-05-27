# Contributing to yasbd: Technician & Calibration Manual

The maintenance bench is open. Grab your protective eyewear, pick up your calipers, and let's calibrate some high-speed sentence shearing equipment.

We don't do sloppy hacks or blunt tears here. yasbd is a zero-copy, low-memory, pointer-scanning boundary shearing unit. If you are here to modify the cutting edge, you must adhere to the strict mechanical tolerances outlined in this manual.

## 1. Bench Setup & Tooling Installation

Before you touch the live micro-blades, you need to set up an isolated diagnostic environment.

### Step 1: Clone the Unit Blueprint

Pull the official schematics from the main repository:

```bash
git clone https://github.com/speedyk-005/yasbd.git
cd yasbd
```

### Step 2: Establish an Isolated Calibration Field

Create and activate your virtual environment using uv. Do not install dependencies globally unless you enjoy contaminating your workshop.

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Calibration-Grade Tooling

Install the development package with the necessary testing rigs using uv pip.

```bash
uv pip install -e ".[dev]"      # Standard calibration suite
uv pip install -e ".[dev-all]"  # Full stress-test configuration
```

> [!WARNING]
> #### Field Operations: Termux (Android)
> Handheld diagnostic terminals running Termux do not ship with a Rust compiler by default. Without it, the pydantic-core assembly will fail to compile (especially on Python 3.13).
>
> To bypass this compilation error, inject pre-built wheels directly into the path before mounting the main package:
>
> ```bash
> uv pip install typing-extensions
> uv pip install pydantic-core --index-url https://termux-user-repository.github.io/pypi/
> uv pip install "pydantic>=2.12.4,<2.13"
> uv pip install -e ".[dev-all]"
> ```

## 2. Making Modifications (Adjusting the Blade)

Do not make adjustments directly to the main production line. Work on an isolated branch.

### Step 1: File an Engineering Sub-Branch

Use a standardized prefix so the telemetry system knows what you are touching:

```bash
# For mechanical upgrades:
git checkout -b feature/my-feature-branch

# For structural repairs:
git checkout -b bugfix/issue-number-description
```

### Step 2: Run the Diagnostic Rig

If you change the teeth of a blade, you must verify it still cuts straight. Run the test suite using uv run:

```bash
uv run pytest
```

### Step 3: Machine the Surfaces (Formatting & Linting)

Our code surfaces must be perfectly smooth. Any micro-roughness will block compile-time caching. Before pushing, sand down the rough edges:

```bash
uv run ruff format && uv run ruff check --fix
```

### Step 4: Build Documentation

If you changed any docstrings or public interfaces, regenerate the docs:

```bash
uv pip install -e ".[dev]"

# Generate API_REFERENCES.md from docstrings
uv run python -m python_docstring_markdown ./src/yasbd API_REFERENCES.md

# Generate/update README TOC (GitHub-compatible)
npx doctoc --github README.md
```

## 3. Engineering Quality Guidelines

### Mechanical Component Ordering (Method Ordering)

To keep the machinery readable for other technicians, arrange class components strictly from top to bottom. Do not throw private helpers wherever you feel like it. Keep the internal components ordered like this:

1. Class docstring (describes what the machine does)
2. Constants and static configuration attributes
3. Constructor (`__init__`)
4. Read-only instrumentation properties (`@property`)
5. Private helper components (`_private_method`)
6. Public operational controls (`public_method`)

```python
class ExampleClass:
    """Detailed structural docstring explaining the component's purpose."""

    STATIC_TOLERANCE_BOUND = 0.005

    def __init__(self):
        """Prepares internal state and registers caching arrays."""
        self._value = None

    @property
    def current_tolerance(self):
        """Exposes raw tracking metrics to downstream monitors."""
        return self._value

    def _execute_lookahead(self):
        """Low-level scan step. No docstring needed unless it gets weird."""
        pass

    def execute_split(self):
        """Triggers the primary physical slice on the input text stream."""
        pass
```

### Docstring Standards

All public interface controls must be documented using Google-style docstrings. Explain your arguments, return types, and exceptions clearly. If your code is too complex for a standard docstring, simplify your logic or document the mathematical assumptions clearly.

## 4. Maintenance Report Template (Pull Request)

When submitting your modifications to the main system, use the following engineering template.

### Mechanical Objective

Brief, precise summary of why the machinery needed modification.

### Applied Modifications

- Component 'X' was swapped out for 'Y'.
- Caching layer was optimized to prevent O(N²) lockups.
- Fixed boundary-slippage bug near abbreviation patterns.

### Diagnostic Verification

- Confirm that `pytest` executed successfully.
- Mention any new test cases added to the validation suite.

### Referenced Blueprints

- Fixes #issue-number

## 5. Operator Conduct & Behavior Protocols

We are adults here trying to build high-performance software. Be civil, respect different architectural opinions, and remember that behind every GitHub profile is a human being who probably has better things to do than argue over irrelevant formatting details.

If you cannot cooperate on the workshop floor without making the experience miserable or hostile for other technicians, please pack up your tools and find a different project to work on. We are here to ship fast code, not to psychoanalyze each other's lifestyle choices. Keep your communication professional, direct, and constructive, and the machinery will run perfectly.
