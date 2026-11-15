"""Read and interpret key-value configuration files."""

from typing import Dict, Generator, Tuple

from a_maze_ing.parse.exceptions_parser import ExceptionParser


def lexer(read: str) -> Generator[Tuple[str, str], None, None]:
    """Validate configuration syntax and yield key-value pairs."""
    for line_number, line in enumerate(read.splitlines(), start=1):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        if '=' not in line:
            raise ExceptionParser(
                f"Error in line {line_number}: no '=' character found"
            )

        tokens = line.split("=")
        if len(tokens) != 2:
            raise ExceptionParser(
                f"Error in line {line_number}: "
                "invalid syntax or multiple '=' tokens"
            )

        key, val = tokens[0].strip(), tokens[1].strip()

        if '#' in key or '#' in val:
            raise ExceptionParser(
                f"Error in line {line_number}: "
                "invalid comment syntax inside key or value"
            )

        if not key.isupper():
            raise ExceptionParser(
                f"Error in line {line_number}: the key is not uppercase"
            )

        yield key, val


def interpretor(content: str) -> Dict[str, str]:
    """Parse configuration text and return its key-value pairs."""
    config: Dict[str, str] = {}
    for key, val in lexer(content):
        if key in config:
            raise ExceptionParser(
                f"Duplicate configuration key '{key}'"
            )
        config[key] = val
    return config
