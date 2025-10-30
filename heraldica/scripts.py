import subprocess
import sys


def run_command(command: list[str]) -> None:
    """Ejecuta un comando en un subproceso y sale con su código de retorno."""
    result = subprocess.run(command, check=False)
    sys.exit(result.returncode)


def lint():
    """Run ruff check on heraldica and tests"""
    run_command(["ruff", "check", "heraldica", "tests"])


def format_code():
    """Run ruff format on heraldica and tests"""
    run_command(["ruff", "format", "heraldica", "tests"])


def test():
    """Run pytest"""
    run_command(["pytest", "-q"])
