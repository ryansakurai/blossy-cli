"""
A lil' bud that helps you with stuff (it's a utility CLI).
"""

import random
import os
import typer
from typing_extensions import Annotated
from .calc import CalcLexer, CalcParser, VisualCalcParser, CalcVisualizer

app = typer.Typer(name="blossy", help="A lil' bud that helps you with stuff (it's a utility CLI).")


@app.command()
def perc(
    whole: Annotated[float, typer.Option("--whole", "-w", show_default=False)] = None,
    part: Annotated[float, typer.Option("--part", "-p", show_default=False)] = None,
    ratio: Annotated[float, typer.Option("--ratio", "-r", show_default=False)] = None,
    full_msg: Annotated[bool, typer.Option()] = True,
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
    lower: Annotated[int, typer.Argument(show_default=False)],
    upper: Annotated[int, typer.Argument(show_default=False)],
    quantity: Annotated[int, typer.Option("--quantity", "-q")] = 1,
):
    """
    RANDOM

    Calculate a random number between 'lower' an 'upper'.
    """

    for i in range(quantity):
        number = random.randint(lower, upper)
        end_char = " " if i < (quantity-1) else "\n"
        print(number, end=end_char)


@app.command()
def calc(
    expression: Annotated[str, typer.Argument(show_default=False)],
    visualize: Annotated[bool, typer.Option("--visualize", "-v")] = False,
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
def stddz(
    prefix: Annotated[str, typer.Argument(show_default=False)],
    directory: Annotated[str, typer.Argument(show_default=False)],
    starting_number: Annotated[int, typer.Option("--start", "-s")] = 0,
    qt_digits: Annotated[int, typer.Option("--digits", "-d")] = 3,
):
    """
    STARDARDIZE

    Rename all files in a DIRECTORY to '{PREFIX}-{ID}', in which the ID is
    calculated incrementally.
    """

    dir_abs_path = os.path.abspath(directory)
    files = [f for f in os.listdir(dir_abs_path) if os.path.isfile(os.path.join(dir_abs_path, f))]
    last_id = starting_number + len(files) - 1
    max_qt_digits = len(str(last_id))
    qt_digits = max(qt_digits, max_qt_digits)

    num = starting_number
    for filename in files:
        _, ext = os.path.splitext(filename)
        num_str = f"{num:0{qt_digits}}"
        new_file = f"{prefix}-{num_str}{ext}"
        os.rename(os.path.join(dir_abs_path, filename), os.path.join(dir_abs_path, new_file))

        num += 1


@app.command()
def count(
    file_path: Annotated[str, typer.Argument(show_default=False)],
    ignore_ws: Annotated[bool, typer.Option("--ignore-ws")] = False,
    ignore_trail: Annotated[bool, typer.Option("--ignore-trail")] = False,
    full_msg: Annotated[bool, typer.Option()] = True,
):
    current_dir = os.getcwd()
    full_file_path = os.path.join(current_dir, file_path)

    try:
        with open(full_file_path, "r", encoding="utf-8") as file:
            content = file.read()

            char_count = 0
            prev_char = ""
            for char in content:
                if ignore_ws and char.isspace():
                    pass
                elif ignore_trail and char.isspace() and prev_char.isspace():
                    pass
                else:
                    char_count += 1
                prev_char = char

            if ignore_trail:
                if content[0].isspace():
                    char_count -= 1
                if content[-1].isspace():
                    char_count -= 1

            print(f"Character count: {char_count}" if full_msg else char_count)
    except FileNotFoundError:
        if full_msg:
            print(f"The file '{full_file_path}' does not exist.")


if __name__ == "__main__":
    app()
