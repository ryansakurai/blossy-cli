"""'countl' command of the Blossy CLI."""

import os

import typer
from typing_extensions import Annotated


def execute(
    file: Annotated[
        str, typer.Argument(show_default=False, help="Relative path to the file.")
    ],
    ignore_blank: Annotated[bool, typer.Option(help="Ignore all blank lines.")] = True,
    full_msg: Annotated[bool, typer.Option(help="Show full message.")] = True,
):
    """
    COUNT LINES

    Count the amount of lines in a code source file.
    """

    current_dir = os.getcwd()
    file_abs_path = os.path.join(current_dir, file)

    try:
        with open(file_abs_path, "r", encoding="utf-8") as f:
            line_count = 0
            for line in f:
                if ignore_blank and (line.isspace() or len(line) == 0):
                    continue
                line_count += 1

            print(f"Line count: {line_count}" if full_msg else line_count)
    except FileNotFoundError as e:
        raise typer.BadParameter(f"'{file_abs_path}' does not exist.") from e
    except IsADirectoryError as e:
        raise typer.BadParameter(f"'{file_abs_path}' is not a file.") from e
