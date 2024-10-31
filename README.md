<h1 align="center">  🌸  Blossy CLI  🌸  </h1>

A multiuse utility CLI tool developed using:

- Python
- Typer (CLI building)
- Sly Lex Yacc (parsing)

## 🛠 Features

- [x] Calculate the value of an expression
- [x] Count the number of characters in a text file
- [x] Solve percentage equations
- [x] Generate random numbers
- [x] Stardardize the names of the files in a directory

## 🏁 How to Install

To install the CLI, you'll only need to have Python installed on your machine. Then, run the following command:

```bash
$ python3 -m pip install blossy
```

## ⚙️ Behavior

To have full instructions on how to use the CLI, run the following command:

```bash
$ blossy --help
```

### Calculate

This command will calculate the value of an expression. The following operators are supported:

- (expr)
- \+ expr
- \- expr
- expr ^ expr
- expr * expr
- expr / expr
- expr + expr
- expr - expr

Here's an example of how to use the command:

```bash
$ blossy calc "2*3+4^6"
4102
```

You can also use the `--visualize` flag to see the steps of the calculation, illustrated using postfix notation and a stack:

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

### Count

This command will count the number of characters in a text file. Here's an example of how to use the command:

```bash
$ blossy count file.txt 
Character count: 25
```

Using the `--ignore-unnec` flag, unnecessary whitespaces will be ignored. That way, a sequence of whitespaces will be counted as only one character:

```bash
$ blossy count file.txt --ignore-unnec
Character count: 21
```

Using the `--ignore-ws` flag, all whitespaces will be ignored:

```bash
$ blossy count file.txt --ignore-ws
Character count: 20
```

### Percentage

This command will solve percentage equations using the formula `ratio = part/whole`. Here's an example of how to use the command:

```bash
$ blossy perc --whole 100 --ratio 0.25
Part: 25.0
$ blossy perc --whole 100 --part 25
Ratio: 0.25
```

### Random

This command will generate a random number between two given values (inclusive). Here's an example of how to use the command:

```bash
$ blossy rand 1 10
2
```

You can also specify the quantity of random numbers to be generated (the default is 1):

```bash
$ blossy rand 1 10 --quantity 5
2 7 1 5 1
```

### Standardize

This command will standardize the names of the files in a directory, using the format `{prefix}-{id}`. Here's an example of how to use the command:

```bash
$ blossy stddz name folder/
```

You can use the flag `--start` to specify the starting number for the IDs:

```bash
$ blossy stddz name folder/ --start 10
```

You can also use the flag `--digits` to specify the quantity of digits used to represent the IDs (the default is 3):

```bash
$ blossy stddz name folder/ --digits 2
```
