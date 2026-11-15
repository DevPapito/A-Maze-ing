"""Validate command-line input and build the maze configuration."""

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
    """Store the dimensions, endpoints, and settings for a maze."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_coordinates(value: str) -> tuple[int, int]:
    """Parse a coordinate pair in the form x,y."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate pair: {value}")
    return int(parts[0].strip()), int(parts[1].strip())


def file_validate() -> None:
    """Ensure config.txt exists and is readable."""
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
    """Validate that config.txt is the sole command-line argument."""
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
    """Parse config.txt and return its validated maze configuration."""
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
            f"Error: Missing required keys in config.txt: {missing_keys}"
        )
        sys.exit(1)
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry = parse_coordinates(config["ENTRY"])
        exit = parse_coordinates(config["EXIT"])
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError(
                f"ENTRY coordinates {entry} are outside grid bounds "
                f"(Width: {width}, Height: {height})"
            )
        if not (0 <= exit[0] < width and 0 <= exit[1] < height):
            raise ValueError(
                f"EXIT coordinates {exit} are outside grid bounds "
                f"(Width: {width}, Height: {height})"
            )
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
