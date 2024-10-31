<h1 align="center">  🌸  Blossy CLI  🌸  </h1>

A multiuse utility CLI tool developed using:

- Python
- Typer (CLI building)
- Sly Lex Yacc (parsing)

## 🛠 Features

- [x] Calculate the value of an expression
- [x] Count the quantity of characters in a text file
- [x] Solve percentage equations
- [x] Generate random numbers
- [x] Stardardize the names of the files in a directory

## 🏁 How to Install

To install the CLI, you'll only need to have Python installed on your machine. Then, run the following command:

```bash
$ python3 -m pip install blossy
```

## ⚙️ Behavior

### 🧮 Calculate

To calculate the value of an expression, use the `calc` command. The following operators are supported:

- (expr)
- \+ expr
- \- expr
- expr ^ expr
- expr * expr
- expr / expr
- expr + expr
- expr - expr

```bash
$ blossy calc "2*3+4^6"
4102
```

You can use the `--visualize` flag to see the steps of the calculation, illustrated using postfix notation and a stack.

```bash
$ blossy calc "2*3+4^6" --visualize

$                                                          2 3 * 4 6 ^ +₂ $

> Stack 2

$ 2                                                          3 * 4 6 ^ +₂ $

> Stack 3

$ 2 3                                                          * 4 6 ^ +₂ $

> 2 * 3 = 6

$ 6                                                              4 6 ^ +₂ $

> Stack 4

$ 6 4                                                              6 ^ +₂ $

> Stack 6

$ 6 4 6                                                              ^ +₂ $

> 4^6 = 4096

$ 6 4096                                                               +₂ $

> 6 + 4096 = 4102

$ 4102                                                                    $

> The result is 4102
```

### 🔢 Count

To count the quantity of characters in a text file, use the `calc` command.

```bash
$ blossy count file.txt 
Character count: 58
```

```
Blossy is my favorite puppy.

Did somebody say meatloaf?


```

You can use the `--ignore-unnec` flag to ignore unnecessary whitespaces. That way, a sequence of whitespaces will be counted as only one character, and trailing whitespaces will be completely ignored.

```bash
$ blossy count file.txt --ignore-unnec
Character count: 55
```

```
Blossy is my favorite puppy. Did somebody say meatloaf?
```

You can also use the `--ignore-ws` flag to ignore all whitespaces.

```bash
$ blossy count file.txt --ignore-ws
Character count: 47
```

```
Blossyismyfavoritepuppy.Didsomebodysaymeatloaf?
```

### 📊 Percentage

To solve percentage equations, use the `perc` command. This command uses the formula `ratio = part/whole`.

```bash
$ blossy perc --whole 100 --ratio 0.25
Part: 25.0
$ blossy perc --whole 100 --part 25
Ratio: 0.25
```

### 🎲 Random

To generate a random number between two given values (inclusive), use the `rand` command.

```bash
$ blossy rand 1 10
2
```

You can specify the quantity of random numbers that'll be generated (the default is 1):

```bash
$ blossy rand 1 10 --quantity 5
2 7 1 5 1
```

### 🗂️ Standardize

To rename the files in a directory, using the format `{prefix}-{id}`, use the `stddz` command. Here's an example of how to use the command:

```bash
$ blossy stddz my-johnson nice-folder/
```

```
nice-folder/
├── my-johnson-000.png
├── my-johnson-001.png
├── my-johnson-002.png
└── my-johnson-003.png
```

You can use the flag `--start` to specify the starting number for the IDs:

```bash
$ blossy stddz my-johnson nice-folder/ --start 10
```

```
nice-folder/
├── my-johnson-010.png
├── my-johnson-011.png
├── my-johnson-012.png
└── my-johnson-013.png
```

You can also use the flag `--digits` to specify the quantity of digits that'll be used to represent the IDs (the default is 3):

```bash
$ blossy stddz my-johnson nice-folder/ --digits 2
```

```
nice-folder/
├── my-johnson-00.png
├── my-johnson-01.png
├── my-johnson-02.png
└── my-johnson-03.png
```
