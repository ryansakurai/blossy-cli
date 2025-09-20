"""
A lil' bud that helps you with stuff (it's a utility CLI).
"""

import os
import random
import string

import typer
from typing_extensions import Annotated

from .calculate.service import (
    ExpressionLexer,
    ExpressionParser,
    PostfixedExpressionParser,
    visualize_calc,
)

app = typer.Typer(
    name="blossy", help="A lil' bud that helps you with stuff (it's a utility CLI)."
)


@app.command()
def calc(
    expression: Annotated[
        str, typer.Argument(show_default=False, help="Expression to be calculated.")
    ],
    visualize: Annotated[
        bool,
        typer.Option(
            "--visualize",
            "-v",
            help="Show a visualization using postfix notation and a stack.",
        ),
    ] = False,
):
    """
    CALCULATE

    Calculate the value of a mathematical expression involving numbers and time.

    Number syntax:\n
    • Integers: 123\n
    • Decimals: 12.34\n

    Time syntax:\n
    • 43:21 (43 minutes, 21 seconds)\n
    • 65:43:21 (65 hours, 43 minutes, 21 seconds)\n

    Available operations:\n
    • (expr) - Grouping\n
    • +expr - Unary plus\n
    • -expr - Unary minus\n
    • expr ^ expr - Exponentiation\n
    • expr * expr - Multiplication\n
    • expr / expr - Division\n
    • expr + expr - Addition\n
    • expr - expr - Subtraction\n

    Operation rules for time:\n
    • Time + Time = Time\n
    • Time - Time = Time\n
    • Time * Number = Time\n
    • Number * Time = Time\n
    • Time / Number = Time\n
    """
    try:
        if visualize:
            lexer = ExpressionLexer()
            parser = PostfixedExpressionParser()
            postfixed_expr: tuple[str] = parser.parse(lexer.tokenize(expression))

            for step in visualize_calc(postfixed_expr):
                if step.operation:
                    print(f"> {step.operation}")
                if step.stack and step.input:
                    print()
                    _print_with_padding(step.stack, step.input)
                input()
            return

        lexer = ExpressionLexer()
        parser = ExpressionParser()
        result: int | float = parser.parse(lexer.tokenize(expression))
        print(result)
    except Exception as e:
        raise typer.BadParameter(str(e)) from e


def _print_with_padding(left_side: str, right_side: str) -> None:
    terminal_width = os.get_terminal_size().columns
    padding = terminal_width - len(left_side) - len(right_side)
    if padding > 0:
        print(left_side + " " * padding + right_side)
    else:
        print(left_side + " " * 2 + right_side)


@app.command()
def countc(
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


@app.command()
def countl(
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


@app.command()
def perc(
    whole: Annotated[
        float | None, typer.Option("--whole", "-w", show_default=False)
    ] = None,
    part: Annotated[
        float | None, typer.Option("--part", "-p", show_default=False)
    ] = None,
    ratio: Annotated[
        float | None, typer.Option("--ratio", "-r", show_default=False)
    ] = None,
    full_msg: Annotated[bool, typer.Option(help="Show full message.")] = True,
):
    """
    PERCENTAGE

    Take two of the three percentage-related options and calculate the remaining one.

    Example:\n
    $ blossy perc --whole 100 --part 25\n
    Ratio: 0.25
    """

    if whole is not None and part is not None:
        if whole == 0:
            raise typer.BadParameter("Result does not exist.")
        ratio = part / whole
        print(f"Ratio: {ratio}" if full_msg else ratio)

    elif whole is not None and ratio is not None:
        part = whole * ratio
        print(f"Part: {part}" if full_msg else part)

    elif part is not None and ratio is not None:
        if ratio == 0:
            raise typer.BadParameter("Result does not exist.")
        whole = part / ratio
        print(f"Whole: {whole}" if full_msg else whole)

    else:
        raise typer.BadParameter("Less than two parameters passed.")


@app.command()
def rand(
    lower: Annotated[
        int,
        typer.Argument(show_default=False, help="Lower limit (inclusive)."),
    ],
    upper: Annotated[
        int,
        typer.Argument(show_default=False, help="Upper limit (inclusive)."),
    ],
    quantity: Annotated[
        int,
        typer.Option(
            "--quantity", "-q", help="Quantity of random numbers to generate."
        ),
    ] = 1,
):
    """
    RANDOM

    Generate a random number between 'lower' an 'upper'.
    """
    if lower > upper:
        raise typer.BadParameter("Invalid range.")

    for i in range(quantity):
        number = random.randint(lower, upper)
        end_char = " " if i < (quantity - 1) else "\n"
        print(number, end=end_char)


@app.command()
def stddz(
    prefix: Annotated[
        str,
        typer.Argument(show_default=False, help="Prefix of the files."),
    ],
    directory: Annotated[
        str,
        typer.Argument(show_default=False, help="Relative path to the directory."),
    ],
    start_idx: Annotated[
        int,
        typer.Option("--start", "-s", help="Starting number for the IDs."),
    ] = 0,
    qt_digits: Annotated[
        int,
        typer.Option(
            "--digits", "-d", help="Quantity of digits used to represent the ID."
        ),
    ] = 3,
):
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


if __name__ == "__main__":
    app()
