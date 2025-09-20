"""'rand' command of the Blossy CLI."""

import random

import typer
from typing_extensions import Annotated

app = typer.Typer()


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
