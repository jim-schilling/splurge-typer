"""Pytest configuration helpers for the test suite.

This conftest ensures the repository root is on sys.path early so that
`splurge_typer` and its submodules can be imported when pytest is invoked
from different environments (IDE, pre-commit hooks, CI).

It is purposely minimal to avoid surprising test behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _add_repo_root_to_syspath() -> None:
    """Insert the repository root into sys.path if not already present.

    Pytest (and pre-commit's system runner) may run with a working
    directory that doesn't include the package on sys.path. Adding the
    repository root early in test collection ensures local imports like
    `splurge_typer.exceptions` resolve to the source tree.
    """

    repo_root = Path(__file__).resolve().parents[1]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        # Put repo root first so local package takes precedence over
        # installed distributions with the same name.
        sys.path.insert(0, repo_root_str)


# Perform insertion at import time (very early during pytest collection).
_add_repo_root_to_syspath()
