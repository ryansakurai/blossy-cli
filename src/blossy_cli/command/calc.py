"""
Module dedicated to functionalities of the 'calc' command
"""

from collections.abc import Generator, Iterable
from dataclasses import dataclass

from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction

# TODO: ditch sly, cause WTF


class ExpressionLexer(Lexer):
    """Lexer for simple mathematical expressions"""

    operators = {
        "PLUS": "+",
        "MINUS": "-",
        "TIMES": "*",
        "DIVIDE": "/",
        "EXPONENT": "^",
    }

    tokens = tuple(operators.keys()) + (
        "FLOAT_CONST",
        "INT_CONST",
        "L_PARENTH",
        "R_PARENTH",
    )

    ignore = " "

    FLOAT_CONST = r"[0-9]+\.[0-9]+"
    INT_CONST = r"[0-9]+"
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    EXPONENT = r"\^"
    L_PARENTH = r"\("
    R_PARENTH = r"\)"


class ParsingError(Exception):
    """Custom exception for parsing errors"""


class ExpressionParser(Parser):
    """Parser for simple mathematical expressions"""

    tokens = ExpressionLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "EXPONENT", "UNARY_PLUS", "UNARY_MINUS"),
    )

    def error(self, token: Token | None) -> None:
        if token:
            raise ParsingError(
                f"Operation absent or used incorrectly near index {token.index}"
            )
        raise ParsingError("Operation absent or used incorrectly near the end of input")

    @_("expression")
    def start(self, prod: YaccProduction) -> int | float:
        return self._normalize_num(prod.expression)

    def _normalize_num(self, num: int | float) -> int | float:
        if isinstance(num, int):
            return num
        return int(num) if num.is_integer() else round(num, 2)

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression0 + prod.expression1

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression0 - prod.expression1

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression0 * prod.expression1

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression0 / prod.expression1

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression0**prod.expression1

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> int | float:
        return 0 - prod.expression

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.expression

    @_("number")
    def expression(self, prod: YaccProduction) -> int | float:
        return prod.number

    @_("INT_CONST")
    def number(self, prod: YaccProduction) -> int:
        return int(prod.INT_CONST)

    @_("FLOAT_CONST")
    def number(self, prod: YaccProduction) -> float:
        return float(prod.FLOAT_CONST)


class PostfixedExpressionParser(Parser):
    """Parser for converting expressions to postfixed notation."""

    tokens = ExpressionLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "EXPONENT", "UNARY_PLUS", "UNARY_MINUS"),
    )

    def error(self, token: Token | None) -> None:
        if token:
            raise ParsingError(
                f"Operation absent or used incorrectly near index {token.index}"
            )
        raise ParsingError("Operation absent or used incorrectly near the end of input")

    @_("expression")
    def start(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression0 + prod.expression1 + ("+₂",)

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression0 + prod.expression1 + ("-₂",)

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression0 + prod.expression1 + ("*",)

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression0 + prod.expression1 + ("/",)

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression0 + prod.expression1 + ("^",)

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression + ("+₁",)

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression + ("-₁",)

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return prod.expression

    @_("number")
    def expression(self, prod: YaccProduction) -> tuple[str]:
        return (prod.number,)

    @_("INT_CONST")
    def number(self, prod: YaccProduction) -> int:
        return prod.INT_CONST

    @_("FLOAT_CONST")
    def number(self, prod: YaccProduction) -> float:
        return prod.FLOAT_CONST


@dataclass
class VisualCalcStep:
    """Represents a single step in the calculation process."""

    operation: str | None
    stack: str | None
    input: str | None


def visualize_calc(postfixed_expr: tuple[str]) -> Generator[VisualCalcStep, None, None]:
    """Visualize the calculation steps."""
    ops = {
        "unary": ("+₁", "-₁"),
        "binary": ("+₂", "-₂", "*", "/", "^"),
    }
    state = {
        "stack": ["$"],
        "input": list(postfixed_expr) + ["$"],
    }

    yield VisualCalcStep(
        None, _iter_to_str(state["stack"]), _iter_to_str(state["input"])
    )

    while len(state["input"]) > 1:
        value = state["input"].pop(0)

        if value in ops["unary"]:
            operand = state["stack"].pop()
            operator = value
            result, operation = _handle_unary(operator, operand)
            state["stack"].append(result)
        elif value in ops["binary"]:
            operand_2 = state["stack"].pop()
            operand_1 = state["stack"].pop()
            operator = value
            result, operation = _handle_binary(operator, operand_1, operand_2)
            state["stack"].append(result)
        else:
            state["stack"].append(value)
            operation = f"Stack {value}"

        stack_str = _iter_to_str(state["stack"])
        input_str = _iter_to_str(state["input"])
        yield VisualCalcStep(operation, stack_str, input_str)

    final_result = state["stack"].pop()
    final_result = _to_num(final_result)
    final_result = round(final_result, 2)
    yield VisualCalcStep(f"The result is {final_result}", None, None)


def _iter_to_str(iterable: Iterable[str]) -> str:
    return " ".join(iterable)


def _to_num(num: str) -> int | float:
    return float(num) if "." in num else int(num)


def _handle_unary(operator: str, operand: str) -> tuple[str, str]:
    match operator:
        case "+₁":
            result = _to_num(operand)
            operation = f"+{operand} = {result}"
        case "-₁":
            result = 0 - _to_num(operand)
            operation = f"-{operand} = {result}"
        case _:
            raise ValueError(f"unknown operator '{operator}'")

    return str(result), operation


def _handle_binary(operator: str, operand_1: str, operand_2: str) -> tuple[str, str]:
    match operator:
        case "+₂":
            result = _to_num(operand_1) + _to_num(operand_2)
            operation = f"{operand_1} + {operand_2} = {result}"
        case "-₂":
            result = _to_num(operand_1) - _to_num(operand_2)
            operation = f"{operand_1} - {operand_2} = {result}"
        case "*":
            result = _to_num(operand_1) * _to_num(operand_2)
            result = _trim_num(result)
            operation = f"{operand_1} * {operand_2} = {result}"
        case "/":
            result = _to_num(operand_1) / _to_num(operand_2)
            result = _trim_num(result)
            operation = f"{operand_1} / {operand_2} = {result}"
        case "^":
            result = _to_num(operand_1) ** _to_num(operand_2)
            result = _trim_num(result)
            operation = f"{operand_1}^{operand_2} = {result}"
        case _:
            raise ValueError(f"unknown operator '{operator}'")

    return str(result), operation


def _trim_num(num: int | float) -> int | float:
    if isinstance(num, int):
        return num
    return int(num) if num.is_integer() else num
