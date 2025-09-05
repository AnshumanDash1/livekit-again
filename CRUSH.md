# CRUSH.md

This file contains important information for AI agents working in this repository.

## Build/Lint/Test Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Lint**: `ruff check .` (assuming ruff is installed)
- **Type-check**: `mypy .` (assuming mypy is installed)
- **Run tests**: `pytest` (assuming pytest is installed)
- **Run a single test**: `pytest <path_to_test_file>::<test_function_name>`

## Code Style Guidelines

- **Imports**: Organize imports into standard library, third-party, and local application imports, each in separate blocks. Sort imports alphabetically within each block.
- **Formatting**: Adhere to PEP 8. Use a linter like Black or Ruff for automated formatting.
- **Types**: Use type hints for function signatures and variable declarations where appropriate.
- **Naming Conventions**:
    - Variables and functions: `snake_case`
    - Classes: `CamelCase`
    - Constants: `UPPER_SNAKE_CASE`
- **Error Handling**: Use specific exception types, not generic `except Exception:`.
