"""Benchmark typer vs radicli for CLI startup time and import overhead."""

import shutil
import subprocess
import sys
import tempfile
import timeit
from pathlib import Path


def bench_code(code: str, label: str) -> float:
    """Time how long a python -c snippet takes (best of 3)."""
    times = []
    for _ in range(3):
        start = timeit.default_timer()
        subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
        )
        elapsed = timeit.default_timer() - start
        times.append(elapsed)
    return min(times)


def bench_help(cmd: list[str]) -> float:
    """Time how long `cmd --help` takes to run (best of 3)."""
    times = []
    for _ in range(3):
        start = timeit.default_timer()
        subprocess.run(cmd + ["--help"], capture_output=True, text=True)
        elapsed = timeit.default_timer() - start
        times.append(elapsed)
    return min(times)


def bench_exec(cmd: list[str]) -> float:
    """Time how long a simple command takes (best of 3)."""
    times = []
    for _ in range(3):
        start = timeit.default_timer()
        subprocess.run(cmd, capture_output=True, text=True)
        elapsed = timeit.default_timer() - start
        times.append(elapsed)
    return min(times)


PYTHON = sys.executable

# --- Import benchmarks ---
print("=== Import time (lower is better) ===")

for label, stmt in [
    ("typer       ", "import typer"),
    ("click       ", "import click"),
    ("radicli     ", "import radicli"),
]:
    t = bench_code(stmt, label)
    print(f"  {label}: {t * 1000:.2f}ms")

# --- --help benchmark ---
print("\n=== --help time (lower is better) ===")

tmpdir = Path(tempfile.mkdtemp())

# Minimal typer CLI
typer_cli = tmpdir / "typer_bench.py"
typer_cli.write_text("""\
import typer
app = typer.Typer()
@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")
@app.command()
def goodbye(name: str):
    typer.echo(f"Goodbye {name}")
if __name__ == "__main__":
    app()
""")

# Minimal radicli CLI (no decorator clutter)
radicli_cli = tmpdir / "radicli_bench.py"
radicli_cli.write_text("""\
from radicli import Radicli, Arg
cli = Radicli(prog="radicli_bench")
@cli.command("hello", name=Arg(help="Your name"))
def hello(name: str):
    print(f"Hello {name}")
@cli.command("goodbye", name=Arg(help="Your name"))
def goodbye(name: str):
    print(f"Goodbye {name}")
if __name__ == "__main__":
    cli.run()
""")

t = bench_help([PYTHON, str(typer_cli)])
print(f"  typer   --help:  {t * 1000:.2f}ms")

t = bench_help([PYTHON, str(radicli_cli)])
print(f"  radicli --help:  {t * 1000:.2f}ms")

# --- Execution benchmark ---
print("\n=== Execution time (lower is better) ===")

t = bench_exec([PYTHON, str(typer_cli), "hello", "world"])
print(f"  typer   hello:   {t * 1000:.2f}ms")

t = bench_exec([PYTHON, str(radicli_cli), "hello", "world"])
print(f"  radicli hello:   {t * 1000:.2f}ms")

# --- yasbd CLI startup (radicli-based) ---
print("\n=== yasbd CLI (built with typer) ===")

t = bench_help([PYTHON, "-m", "yasbd.cli"])
print(f"  yasbd --help:    {t * 1000:.2f}ms")

t = bench_exec([PYTHON, "-m", "yasbd.cli", "langs"])
print(f"  yasbd langs:     {t * 1000:.2f}ms")

# --- Cleanup ---
shutil.rmtree(tmpdir)
