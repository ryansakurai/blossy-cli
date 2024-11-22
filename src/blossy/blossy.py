"""
A lil' bud that helps you with stuff (it's a utility CLI).
"""

import random
import os
import string
from typing import List, Tuple
import typer
from typing_extensions import Annotated
from .calc import CalcLexer, CalcParser, VisualCalcParser, CalcVisualizer
from .calct import CalcTimeLexer, CalcTimeParser, VisualCalcTimeParser, CalcTimeVisualizer

app = typer.Typer(name="blossy", help="A lil' bud that helps you with stuff (it's a utility CLI).")


@app.command()
def calc(
    expression: Annotated[
        str,
        typer.Argument(show_default=False, help="Expression to be calculated."),
    ],
    visualize: Annotated[
        bool,
        typer.Option(
            "--visualize", "-v",
            help="Show a visualization using postfix notation and a stack.",
        ),
    ] = False,
):
    """
    CALCULATE

    Calculate the value of a mathematical expression.

    Available syntax:\n
    • (expr)\n
    • + expr\n
    • - expr\n
    • expr ^ expr\n
    • expr * expr\n
    • expr / expr\n
    • expr + expr\n
    • expr - expr
    """
    try:
        if visualize:
            lexer = CalcLexer()
            parser = VisualCalcParser()
            result = parser.parse(lexer.tokenize(expression))
            visualizer = CalcVisualizer(result)

            for operation, stack_state, input_state in visualizer.visualize():
                if operation:
                    print(f"> {operation}")
                if stack_state and input_state:
                    print()
                    terminal_width = os.get_terminal_size().columns
                    left_side = stack_state
                    right_side = input_state
                    padding = terminal_width - len(left_side) - len(right_side)
                    if padding > 0:
                        print(left_side + " " * padding + right_side)
                    else:
                        print(left_side + "\t" + right_side)
                input()
            return

        lexer = CalcLexer()
        parser = CalcParser()
        result = parser.parse(lexer.tokenize(expression))
        print(result)
    except Exception as e:
        raise typer.BadParameter(str(e)) from e


@app.command()
def calct(
    expression: Annotated[
        str,
        typer.Argument(show_default=False, help="Expression to be calculated."),
    ],
    visualize: Annotated[
        bool,
        typer.Option(
            "--visualize", "-v",
            help="Show a visualization using postfix notation and a stack.",
        ),
    ] = False,
):
    """
    CALCULATE TIME

    Calculate the value of a mathematical expression using time.

    Available syntax:\n
    • (expr)\n
    • + expr\n
    • - expr\n
    • expr ^ expr\n
    • expr * expr\n
    • expr / expr\n
    • expr + expr\n
    • expr - expr
    """
    try:
        if visualize:
            lexer = CalcTimeLexer()
            parser = VisualCalcTimeParser()
            result = parser.parse(lexer.tokenize(expression))
            visualizer = CalcTimeVisualizer(result)

            for operation, stack_state, input_state in visualizer.visualize():
                if operation:
                    print(f"> {operation}")
                if stack_state and input_state:
                    print()
                    terminal_width = os.get_terminal_size().columns
                    left_side = stack_state
                    right_side = input_state
                    padding = terminal_width - len(left_side) - len(right_side)
                    if padding > 0:
                        print(left_side + " " * padding + right_side)
                    else:
                        print(left_side + "\t" + right_side)
                input()
            return

        lexer = CalcTimeLexer()
        parser = CalcTimeParser()
        result = parser.parse(lexer.tokenize(expression))
        print(result)
    except Exception as e:
        raise typer.BadParameter(str(e)) from e


@app.command()
def countc(
    file: Annotated[
        str,
        typer.Argument(show_default=False, help="Relative path to the file."),
    ],
    ignore_unnec: Annotated[
        bool,
        typer.Option("--ignore-unnec", help="Ignore unnecessary (repeated) whitespace."),
    ] = False,
    ignore_ws: Annotated[
        bool,
        typer.Option("--ignore-ws", help="Ignore all whitespace."),
    ] = False,
    full_msg: Annotated[
        bool,
        typer.Option(help="Show full message.")
    ] = True,
):
    """
    COUNT CHARACTERS

    Count the amount of characters in a text file.
    """

    current_dir = os.getcwd()
    full_file_path = os.path.join(current_dir, file)

    try:
        with open(full_file_path, "r", encoding="utf-8") as file:
            char_count = 0
            first_char = ""
            prev_char = ""
            while True:
                char = file.read(1)
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
    except FileNotFoundError:
        if full_msg:
            print(f"The file '{full_file_path}' does not exist.")


@app.command()
def countl(
    file: Annotated[
        str,
        typer.Argument(show_default=False, help="Relative path to the file."),
    ],
    ignore_blank: Annotated[
        bool,
        typer.Option(help="Ignore all blank lines."),
    ] = True,
    full_msg: Annotated[
        bool,
        typer.Option(help="Show full message.")
    ] = True,
):
    """
    COUNT LINES

    Count the amount of lines in a code source file.
    """

    current_dir = os.getcwd()
    full_file_path = os.path.join(current_dir, file)

    try:
        with open(full_file_path, "r", encoding="utf-8") as file:
            line_count = 0
            for line in file:
                if ignore_blank and (line.isspace() or len(line) == 0):
                    continue
                line_count += 1

            print(f"Line count: {line_count}" if full_msg else line_count)
    except FileNotFoundError:
        if full_msg:
            print(f"The file '{full_file_path}' does not exist.")


@app.command()
def perc(
    whole: Annotated[float, typer.Option("--whole", "-w", show_default=False)] = None,
    part: Annotated[float, typer.Option("--part", "-p", show_default=False)] = None,
    ratio: Annotated[float, typer.Option("--ratio", "-r", show_default=False)] = None,
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
        ratio = part/whole
        print(f"Ratio: {ratio}" if full_msg else ratio)
    elif whole is not None and ratio is not None:
        part = whole*ratio
        print(f"Part: {part}" if full_msg else part)
    elif part is not None and ratio is not None:
        whole = part/ratio
        print(f"Whole: {whole}" if full_msg else whole)
    else:
        raise typer.BadParameter("Two options must be passed.")


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
        typer.Option("--quantity", "-q", help="Quantity of random numbers to generate."),
    ] = 1,
):
    """
    RANDOM

    Generate a random number between 'lower' an 'upper'.
    """

    for i in range(quantity):
        number = random.randint(lower, upper)
        end_char = " " if i < (quantity-1) else "\n"
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
        typer.Option("--digits", "-d", help="Quantity of digits used to represent the ID.")
    ] = 3,
):
    """
    STARDARDIZE

    Rename all files in a DIRECTORY to '{PREFIX}-{ID}', in which the ID is
    calculated incrementally.
    """

    dir_abs_path = os.path.abspath(directory)
    files = get_files(dir_abs_path)

    last_id = start_idx + len(files) - 1
    max_qt_digits = len(str(last_id))
    qt_digits = max(qt_digits, max_qt_digits)

    # to prevent overriding previous files
    temp_prefix = "".join(random.choices(string.ascii_letters, k=10))
    rename(dir_abs_path, files, temp_prefix, qt_digits, start_idx)

    files = get_files(dir_abs_path)
    rename(dir_abs_path, files, prefix, qt_digits, start_idx)

def get_files(directory_path: str) -> Tuple[str]:
    files = []
    for item in os.listdir(directory_path):
        file_abs_path = os.path.join(directory_path, item)
        if os.path.isfile(file_abs_path):
            files.append(item)
    return tuple(files)

def rename(dir_path: str,
           files: List[str],
           prefix: str,
           qt_digits: int,
           start_idx: int) -> None:
    idx = start_idx
    for filename in files:
        _, ext = os.path.splitext(filename)
        new_file = build_file_name(prefix, idx, qt_digits) + ext
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_file))

        idx += 1

def build_file_name(prefix: str, index: int, qt_digits: int) -> str:
    num_str = f"{index:0{qt_digits}}"
    return f"{prefix}-{num_str}"


if __name__ == "__main__":
    app()
