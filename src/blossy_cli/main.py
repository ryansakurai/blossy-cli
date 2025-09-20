"""Entry point for the Blossy CLI."""

import typer

from .command import (
    calculate,
    count_chars,
    count_lines,
    percentage,
    random_cmd,
    standardize,
)

app = typer.Typer(
    name="blossy", help="A lil' bud that helps you with stuff (it's a utility CLI)."
)

app.add_typer(calculate.app, name="calc")
app.add_typer(count_chars.app, name="countc")
app.add_typer(count_lines.app, name="countl")
app.add_typer(percentage.app, name="perc")
app.add_typer(random_cmd.app, name="rand")
app.add_typer(standardize.app, name="stddz")
