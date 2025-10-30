import subprocess
import sys


def lint():
    """Run ruff check on heraldica and tests"""
    result = subprocess.run(["ruff", "check", "heraldica", "tests"], check=False)
    sys.exit(result.returncode)


def format_code():
    """Run ruff format on heraldica and tests"""
    result = subprocess.run(["ruff", "format", "heraldica", "tests"], check=False)
    sys.exit(result.returncode)


def test():
    """Run pytest"""
    result = subprocess.run(["pytest", "-q"], check=False)
    sys.exit(result.returncode)
