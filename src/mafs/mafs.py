"""
CLI for math-related utilities.
"""

import typer
import random
from typing_extensions import Annotated


app = typer.Typer(name="mafs")


@app.command()
def perc(
    whole: Annotated[float, typer.Option("--whole", "-w", show_default=False)] = None,
    part: Annotated[float, typer.Option("--part", "-p", show_default=False)] = None,
    ratio: Annotated[float, typer.Option("--ratio", "-r", show_default=False)] = None,
    full_msg: Annotated[bool, typer.Option()] = True,
):
    """
    Take two of the three percentage-related options and calculate the remaining one.

    $ mafs perc --whole 100 --part 25

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
    Calculate a random number between 'lower' an 'upper'.
    """

    for i in range(quantity):
        number = random.randint(lower, upper)
        end_char = " " if i < (quantity-1) else "\n"
        print(number, end=end_char)


@app.command()
def calc(
    expression: Annotated[str, typer.Argument(show_default=False)],
):
    """
    Calculate the value of a mathematical expression.

    Warning: this function uses eval(), which makes it insecure!
    """

    try:
        result = eval(expression)
        print(result)
    except Exception as e:
        raise typer.BadParameter("Invalid expression.") from e


if __name__ == "__main__":
    app()
