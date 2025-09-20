"""'perc' command of the Blossy CLI."""

import typer
from typing_extensions import Annotated

app = typer.Typer()


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
