"""'countc' command of the Blossy CLI."""

import os

import typer
from typing_extensions import Annotated


def execute(
    file: Annotated[
        str, typer.Argument(show_default=False, help="Relative path to the file.")
    ],
    ignore_unnec: Annotated[
        bool,
        typer.Option(
            "--ignore-unnec", help="Ignore unnecessary (repeated) whitespace."
        ),
    ] = False,
    ignore_ws: Annotated[
        bool, typer.Option("--ignore-ws", help="Ignore all whitespace.")
    ] = False,
    full_msg: Annotated[bool, typer.Option(help="Show full message.")] = True,
):
    """
    COUNT CHARACTERS

    Count the amount of characters in a text file.
    """

    current_dir = os.getcwd()
    file_abs_path = os.path.join(current_dir, file)

    try:
        with open(file_abs_path, "r", encoding="utf-8") as f:
            char_count = 0
            first_char = ""
            prev_char = ""
            while True:
                char = f.read(1)
                if not char:
                    break

                if ignore_ws and char.isspace():
                    pass
                elif ignore_unnec and char.isspace() and prev_char.isspace():
                    pass
                else:
                    char_count += 1

                if prev_char == "":
                    first_char = char
                prev_char = char

            last_char = prev_char
            if ignore_unnec:
                if first_char.isspace():
                    char_count -= 1
                if last_char.isspace():
                    char_count -= 1

            print(f"Character count: {char_count}" if full_msg else char_count)
    except FileNotFoundError as e:
        raise typer.BadParameter(f"'{file_abs_path}' does not exist.") from e
    except IsADirectoryError as e:
        raise typer.BadParameter(f"'{file_abs_path}' is not a file.") from e
