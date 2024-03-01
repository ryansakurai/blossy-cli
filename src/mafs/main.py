import typer

app = typer.Typer()

@app.command()
def perc():
    pass

@app.command()
def rand():
    pass

@app.command()
def calc():
    pass

if __name__ == "__main__":
    app()
