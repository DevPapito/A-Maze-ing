import sys
from typing import Dict, Generator, Tuple, Any

def lexer(read: str) -> Generator[Tuple[str, str], None, None]:
    """Analisa o arquivo linha por linha, valida a sintaxe e retorna pares (key, val)."""
    count_line = 1
    for line in read.splitlines():
        line = line.strip()

        if not line or line.startswith('#'):
            count_line += 1
            continue

        if '=' not in line:
            raise Exception(f"Error in line {count_line}: No character '=' found")

        tokens = line.split("=")
        if len(tokens) != 2:
            raise Exception(f"Error in line {count_line}: Invalid syntax or multiple '=' tokens")

        key, val = tokens[0].strip(), tokens[1].strip()

        if '#' in key or '#' in val:
            raise Exception(f"Error in line {count_line}: Invalid commentary syntax in key")

        yield key, val
        count_line += 1

def interpretor() -> Dict[str, str]:
    read_file = ""
    try:
        with open("config.txt", "r", encoding="utf-8") as file:
            read_file = file.read()
    except Exception as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)

    config: Dict[str, str] = {}

    try:
        for key, val in lexer(read_file):
            if key in config:
                raise Exception(f"Error: Duplicate configuration key '{key}'")
            config[key] = val

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    return config
