"""Command line: arguments (role, data directory, port, store ID) and start-up errors. Holds no business rules."""

import argparse
import sys

from retail_pos import __version__


def not_implemented(ticket: int) -> int:
    """Report a command that a later ticket builds, and return a non-zero exit code."""
    print(f"not implemented yet: see #{ticket}", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m retail_pos",
        description="Run the store or the head-office process of the offline retail POS simulator (loopback only).",
    )
    parser.add_argument("--version", action="version", version=f"retail_pos {__version__}")
    parser.add_argument("--role", choices=["store", "head-office"], help="process to run")
    parser.add_argument("--data-dir", help="directory for this process's SQLite database")
    parser.add_argument("--port", type=int, help="loopback port to listen on")
    parser.add_argument("--store-id", help="fictional store ID, one of A to H (store role only)")
    parser.add_argument("--head-office-url", help="optional loopback head-office URL (store role only)")
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    return not_implemented(11)
