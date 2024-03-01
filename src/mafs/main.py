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
    full_msg: Annotated[
        bool,
        typer.Option()
    ] = True,
):
    """
    Pass two of the three options and get the third calculated for you. Example:

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
def rand():
    pass

@app.command()
def calc():
    pass

if __name__ == "__main__":
    app()
