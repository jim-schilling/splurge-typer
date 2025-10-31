# CLI Reference

The `splurge-typer` package provides a command-line interface (CLI) for accessing package information and utilities.

## Installation

To use the CLI, ensure the package is installed:

```bash
pip install splurge-typer
```

Once installed, the `splurge-typer` command is available globally.

## Usage



Both will print the help message and available options.

## Options

### `--version`

Print the installed version of `splurge-typer` and exit.

**Usage:**

```bash
splurge-typer --version
```

**Output Example:**

```
splurge-typer 2025.3.0
```

**Programmatic Usage:**

You can also retrieve the version programmatically from the package:

```python
from splurge_typer import __version__

print(f"Version: {__version__}")
```

## Examples

### Check Package Version

```bash
$ splurge-typer --version
splurge-typer 2025.3.0
```

For more information, see the [main documentation](../README-details.md) or visit the [GitHub repository](https://github.com/jim-schilling/splurge-typer).
