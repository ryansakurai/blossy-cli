"""'stddz' command of the Blossy CLI."""

import os
import random
import string

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def stddz(
    prefix: Annotated[
        str, typer.Argument(show_default=False, help="Prefix of the files.")
    ],
    directory: Annotated[
        str, typer.Argument(show_default=False, help="Relative path to the directory.")
    ],
    start_idx: Annotated[
        int, typer.Option("--start", "-s", help="Starting number for the IDs.")
    ] = 0,
    qt_digits: Annotated[
        int,
        typer.Option(
            "--digits", "-d", help="Quantity of digits used to represent the ID."
        ),
    ] = 3,
) -> None:
    """
    STARDARDIZE

    Rename all files in a DIRECTORY to '{PREFIX}-{ID}', in which the ID is
    calculated incrementally.
    """
    if start_idx < 0:
        raise typer.BadParameter("Negative starting number.")

    try:
        dir_abs_path = os.path.abspath(directory)
        files = _get_files(dir_abs_path)

        last_id = start_idx + len(files) - 1
        min_qt_digits = len(str(last_id))
        if min_qt_digits > qt_digits:
            qt_digits = min_qt_digits
            qt_reajusted = True
        else:
            qt_reajusted = False

        # to prevent overriding previous files
        temp_prefix = "".join(random.choices(string.ascii_letters, k=10))
        _rename(dir_abs_path, files, temp_prefix, qt_digits, start_idx)

        files = _get_files(dir_abs_path)
        _rename(dir_abs_path, files, prefix, qt_digits, start_idx)

        if qt_reajusted:
            print("Quantity of digits had to be reajusted.")
    except FileNotFoundError as e:
        raise typer.BadParameter(f"'{dir_abs_path}' does not exist.") from e
    except NotADirectoryError as e:
        raise typer.BadParameter(f"'{dir_abs_path}' is not a directory.") from e


def _get_files(directory_path: str) -> tuple[str]:
    files = []
    for item in os.listdir(directory_path):
        file_abs_path = os.path.join(directory_path, item)
        if os.path.isfile(file_abs_path):
            files.append(item)
    return tuple(files)


def _rename(
    dir_path: str, files: list[str], prefix: str, qt_digits: int, start_idx: int
) -> None:
    idx = start_idx
    for filename in files:
        _, ext = os.path.splitext(filename)
        new_file = _build_file_name(prefix, idx, qt_digits) + ext
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_file))

        idx += 1


def _build_file_name(prefix: str, index: int, qt_digits: int) -> str:
    num_str = f"{index:0{qt_digits}}"
    return f"{prefix}-{num_str}"
