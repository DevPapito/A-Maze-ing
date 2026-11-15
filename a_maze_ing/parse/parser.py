"""Validate command-line input and build the maze configuration."""

import sys
from dataclasses import dataclass
from typing import Dict

from a_maze_ing.parse.config_interpretor import interpretor
from a_maze_ing.parse.exceptions_parser import (
    ExceptionLengthParser,
    ExceptionParser,
)


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
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError as e:
        raise ValueError(f"Invalid coordinate pair: {value}") from e
    return x, y


def argument_validate() -> None:
    """Validate that a single configuration file path was provided."""
    if len(sys.argv) != 2:
        raise ExceptionLengthParser()


def read_config_file(path: str) -> str:
    """Return the content of the configuration file at the given path."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except OSError as e:
        raise ExceptionParser(
            f"Cannot read configuration file '{path}': {e}"
        ) from e


def parser() -> "Config":
    """Parse the configuration file and return a validated Config."""
    argument_validate()
    content = read_config_file(sys.argv[1])
    config: Dict[str, str] = interpretor(content)

    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    }
    missing_keys = required_keys - config.keys()
    if missing_keys:
        raise ExceptionParser(
            "Missing required keys in the configuration file: "
            f"{missing_keys}"
        )

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
    except ValueError as e:
        raise ExceptionParser(
            f"WIDTH and HEIGHT must be integers: {e}"
        ) from e
    if width < 1 or height < 1:
        raise ExceptionParser("WIDTH and HEIGHT must be positive integers")

    entry = parse_coordinates(config["ENTRY"])
    exit_coord = parse_coordinates(config["EXIT"])
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ExceptionParser(
            f"ENTRY coordinates {entry} are outside grid bounds "
            f"(Width: {width}, Height: {height})"
        )
    if not (0 <= exit_coord[0] < width and 0 <= exit_coord[1] < height):
        raise ExceptionParser(
            f"EXIT coordinates {exit_coord} are outside grid bounds "
            f"(Width: {width}, Height: {height})"
        )

    output_file = config["OUTPUT_FILE"]
    perfect_str = config["PERFECT"].strip().lower()
    if perfect_str not in ("true", "false"):
        raise ExceptionParser(
            f"Invalid boolean value for PERFECT: {config['PERFECT']}"
        )
    perfect = perfect_str == "true"

    seed: int | None = None
    seed_str = config.get("SEED")
    if seed_str is not None:
        try:
            seed = int(seed_str)
        except ValueError as e:
            raise ExceptionParser(f"SEED must be an integer: {e}") from e

    return Config(
        width,
        height,
        entry,
        exit_coord,
        output_file,
        perfect,
        seed,
    )
