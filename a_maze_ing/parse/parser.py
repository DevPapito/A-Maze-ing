import sys
from dataclasses import dataclass
from typing import Dict
from .exceptions_parser import (
    ExceptionParser,
    ExceptionLengthParser,
    ExceptionNameParser
)
from .config_interpretor import interpretor


@dataclass
class Config:
    width: int
    height: int
    entry: float
    exit: float
    output_file: str
    perfect: bool
    seed: int | None = None


def file_validate() -> None:
    try:
        with open("config.txt", "r"):
            pass
    except FileNotFoundError:
        print("File <config.txt> not found in the directory!")
        sys.exit(1)
    except PermissionError:
        print("Permission denied to open/read file <config.txt>")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)


def argument_validate() -> None:
    try:
        if len(sys.argv) != 2:
            raise ExceptionLengthParser()
        if sys.argv[1] != "config.txt":
            raise ExceptionNameParser()
    except ExceptionNameParser as e:
        print(e)
        sys.exit(1)
    except ExceptionLengthParser as e:
        print(e)
        sys.exit(1)
    except ExceptionParser as e:
        print(e)
        sys.exit(1)


def parser() -> "Config":
    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    }
    argument_validate()
    file_validate()
    config: Dict[str, str] = interpretor()
    parsed_keys = set(config.keys())
    missing_keys = required_keys - parsed_keys
    if missing_keys:
        print(
            "Erro: Faltam as seguintes chaves obrigatórias "
            f"no config.txt: {missing_keys}"
        )
        sys.exit(1)
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry = float(config["ENTRY"].replace(',', '.'))
        exit = float(config["EXIT"].replace(',', '.'))
        output_file = str(config["OUTPUT_FILE"])
        perfect_str = config["PERFECT"].strip().lower()
        if perfect_str not in ("true", "false"):
            raise ValueError(
                f"Invalid boolean value for PERFECT: {config['PERFECT']}"
            )
        perfect = perfect_str == "true"
    except ValueError as e:
        print(f"Type error: {e}")
        sys.exit(1)
    return Config(
        width,
        height,
        entry,
        exit,
        output_file,
        perfect,
    )
