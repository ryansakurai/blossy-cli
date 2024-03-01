"""
"""

import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def perc(
    whole: Annotated[
        float,
        typer.Option("--whole", "-w", show_default=False)
    ] = None,
    part: Annotated[
        float,
        typer.Option("--part", "-p", show_default=False)
    ] = None,
    ratio: Annotated[
        float,
        typer.Option("--ratio", "-r", show_default=False)
    ] = None,
):
    """
    Pass two of the three options and get the third calculated for you.
    """

    if whole is not None and part is not None:
        ratio = part/whole
        print(f"Ratio: {ratio}")
    elif whole is not None and ratio is not None:
        part = whole*ratio
        print(f"Part: {part}")
    elif part is not None and ratio is not None:
        whole = part/ratio
        print(f"Whole: {whole}")
    else:
        raise typer.BadParameter("Two options must be specified (eg. whole and part).")

@app.command()
def rand():
    pass

@app.command()
def calc():
    pass

if __name__ == "__main__":
    app()
