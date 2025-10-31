"""End-to-end tests for the splurge-typer CLI.

Tests the command-line interface without mocking, ensuring that the CLI
behaves correctly when invoked with various arguments.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

import subprocess
import sys

import pytest

from splurge_typer import __version__


class TestCliVersion:
    """Tests for CLI --version flag."""

    def test_version_flag_subprocess(self) -> None:
        """Test --version flag via subprocess (true end-to-end test).

        This test invokes the CLI as a subprocess to validate that
        --version prints the correct version string without mocking.
        """
        # Run the CLI with --version flag
        result = subprocess.run(
            [sys.executable, "-m", "splurge_typer.cli", "--version"],
            capture_output=True,
            text=True,
        )

        # Expect exit code 0
        assert result.returncode == 0, f"CLI failed with: {result.stderr}"

        # Expect version output in stdout
        assert __version__ in result.stdout, f"Expected version '{__version__}' in output, got: {result.stdout}"

        # Ensure version is formatted as expected (e.g., "splurge-typer 2025.3.0")
        assert "splurge-typer" in result.stdout

    def test_version_flag_direct_call(self) -> None:
        """Test --version flag via direct function call (unit integration).

        This test calls the CLI main() function directly and validates
        that it correctly processes the --version argument by checking
        the exit code and captured output without mocking.
        """
        from io import StringIO

        from splurge_typer.cli import main

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # The --version argument should cause argparse to print and exit.
            # argparse.ArgumentParser exits with code 0 after printing version.
            with pytest.raises(SystemExit) as exc_info:
                main(["--version"])

            # Check exit code
            assert exc_info.value.code == 0, f"Expected exit code 0, got {exc_info.value.code}"

            # Check that version string was printed
            output = sys.stdout.getvalue()
            assert __version__ in output, f"Expected version '{__version__}' in output, got: {output}"
            assert "splurge-typer" in output

        finally:
            sys.stdout = old_stdout

    def test_no_args_shows_help(self) -> None:
        """Test that calling CLI with no args shows help and exits cleanly.

        When no arguments are provided, the CLI should print help
        (as per the implementation) and return 0.
        """
        from io import StringIO

        from splurge_typer.cli import main

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            exit_code = main([])
            assert exit_code == 0, f"Expected exit code 0, got {exit_code}"

            output = sys.stdout.getvalue()
            # Help output should contain usage/description
            assert "usage:" in output or "Splurge Typer" in output or "--version" in output

        finally:
            sys.stdout = old_stdout
