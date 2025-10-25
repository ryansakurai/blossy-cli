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

app.command("calc")(calculate.execute)
app.command("countc")(count_chars.execute)
app.command("countl")(count_lines.execute)
app.command("perc")(percentage.execute)
app.command("rand")(random_cmd.execute)
app.command("stddz")(standardize.execute)
