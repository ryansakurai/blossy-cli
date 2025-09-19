"""
Module dedicated to functionalities of the 'calct' command.
"""

from collections.abc import Generator, Iterable
from dataclasses import dataclass

from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class Time:
    """Custom time class supporting arithmetic operations."""

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0) -> None:
        absolute = abs(seconds) + abs(minutes) * 60 + abs(hours) * 60 * 60
        if hours < 0 or minutes < 0 or seconds < 0:
            self._total_secs = 0 - absolute
        else:
            self._total_secs = absolute

    @property
    def hours(self) -> int:
        """Hours component in HH:MM:SS display format."""
        absolute = abs(self._total_secs) // (60 * 60)
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def minutes(self) -> int:
        """Minutes component in HH:MM:SS display format."""
        absolute = (abs(self._total_secs) % (60 * 60)) // 60
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def seconds(self) -> int:
        """Seconds component in HH:MM:SS display format."""
        absolute = abs(self._total_secs) % 60
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def total_hours(self) -> int:
        """Total duration converted to whole hours."""
        absolute = abs(self._total_secs) // (60 * 60)
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def total_minutes(self) -> int:
        """Total duration converted to whole minutes."""
        absolute = abs(self._total_secs) // 60
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def total_seconds(self) -> int:
        """Total duration in seconds."""
        return self._total_secs

    def __add__(self, other):
        if isinstance(other, Time):
            return Time(seconds=self.total_seconds + other.total_seconds)
        raise TypeError(
            f"unsupported operand type(s) for +: 'Time' and '{type(other).__name__}'"
        )

    def __sub__(self, other):
        if isinstance(other, Time):
            return Time(seconds=self.total_seconds - other.total_seconds)
        raise TypeError(
            f"unsupported operand type(s) for -: 'Time' and '{type(other).__name__}'"
        )

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Time(seconds=int(self.total_seconds * other))
        raise TypeError(
            f"unsupported operand type(s) for *: 'Time' and '{type(other).__name__}'"
        )

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Time(seconds=int(self.total_seconds * other))
        raise TypeError(
            f"unsupported operand type(s) for *: '{type(other).__name__}' and 'Time'"
        )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Time(seconds=int(self.total_seconds / other))
        raise TypeError(
            f"unsupported operand type(s) for /: 'Time' and '{type(other).__name__}'"
        )

    def __str__(self):
        if self.total_seconds < 0:
            return f"-{abs(self.hours)}:{abs(self.minutes):02}:{abs(self.seconds):02}"
        return f"{abs(self.hours)}:{abs(self.minutes):02}:{abs(self.seconds):02}"


class ExpressionLexer(Lexer):
    """Lexer for mathematical expressions with time."""

    operators = {
        "PLUS": "+",
        "MINUS": "-",
        "TIMES": "*",
        "DIVIDE": "/",
        "EXPONENT": "^",
    }

    tokens = tuple(operators.keys()) + (
        "TIME_CONST",
        "FLOAT_CONST",
        "INT_CONST",
        "L_PARENTH",
        "R_PARENTH",
    )

    ignore = " "

    TIME_CONST = r"([0-9]+:)?[0-9]+:[0-9]+"
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
    """Domain exception for parsing errors."""


class ExpressionParser(Parser):
    """Parser for mathematical expressions with time."""

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
    def start(self, prod: YaccProduction) -> Time:
        if not isinstance(prod.expression, Time):
            raise ParsingError("Result is not time (use 'calc' instead)")

        return prod.expression

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        if isinstance(prod.expression0, Time) and not isinstance(
            prod.expression1, Time
        ):
            raise ParsingError(
                "Number being added to time " + f"near index {prod.index}"
            )
        if not isinstance(prod.expression0, Time) and isinstance(
            prod.expression1, Time
        ):
            raise ParsingError(
                "Time being added to number " + f"near index {prod.index}"
            )

        return prod.expression0 + prod.expression1

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        if isinstance(prod.expression0, Time) and not isinstance(
            prod.expression1, Time
        ):
            raise ParsingError(
                "Number being subtracted from time " + f"near index {prod.index}"
            )
        if not isinstance(prod.expression0, Time) and isinstance(
            prod.expression1, Time
        ):
            raise ParsingError(
                "Time being subtracted from number " + f"near index {prod.index}"
            )

        return prod.expression0 - prod.expression1

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        if isinstance(prod.expression0, Time) and isinstance(prod.expression1, Time):
            raise ParsingError(
                "Time being multiplied by time " + f"near index {prod.index}"
            )

        return prod.expression0 * prod.expression1

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        if isinstance(prod.expression1, Time):
            raise ParsingError(f"Time used as divisor near index {prod.index}")

        return prod.expression0 / prod.expression1

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> int | float:
        if isinstance(prod.expression0, Time) or isinstance(prod.expression1, Time):
            raise ParsingError(
                f"Operation {prod.EXPONENT} used with time "
                + f"near index {prod.index}"
            )

        return prod.expression0**prod.expression1

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        return prod.expression

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        if isinstance(prod.expression, Time):
            return Time() - prod.expression
        return 0 - prod.expression

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        return prod.expression

    @_("operand")
    def expression(self, prod: YaccProduction) -> Time | int | float:
        return prod.operand

    @_("TIME_CONST")
    def operand(self, prod: YaccProduction) -> Time:
        parts = tuple(map(int, prod.TIME_CONST.split(":")))
        if len(parts) == 3:
            value = Time(hours=parts[-3], minutes=parts[-2], seconds=parts[-1])
        else:
            value = Time(minutes=parts[-2], seconds=parts[-1])

        return value

    @_("INT_CONST")
    def operand(self, prod: YaccProduction) -> int:
        return int(prod.INT_CONST)

    @_("FLOAT_CONST")
    def operand(self, prod: YaccProduction) -> float:
        return float(prod.FLOAT_CONST)


@dataclass
class ExpressionResult:
    """Represents the result of parsing an expression for visualization."""

    value: tuple[str] | str
    type: str


class PostfixedExpressionParser(Parser):
    """Parser for converting expressions with time to postfixed notation."""

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
        if prod.expression.type == "number":
            raise ParsingError("Result is not time (use 'calc' instead)")

        return prod.expression.value

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        if prod.expression0.type == "time" and prod.expression1.type == "number":
            raise ParsingError(
                "Number being added to time " + f"near index {prod.index}"
            )
        if prod.expression0.type == "number" and prod.expression1.type == "time":
            raise ParsingError(
                "Time being added to number " + f"near index {prod.index}"
            )

        return ExpressionResult(
            value=prod.expression0.value + prod.expression1.value + ("+₂",),
            type=prod.expression0.type,
        )

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        if prod.expression0.type == "time" and prod.expression1.type == "number":
            raise ParsingError(
                "Number being subtracted from time " + f"near index {prod.index}"
            )
        if prod.expression0.type == "number" and prod.expression1.type == "time":
            raise ParsingError(
                "Time being subtracted from number " + f"near index {prod.index}"
            )

        return ExpressionResult(
            value=prod.expression0.value + prod.expression1.value + ("-₂",),
            type=prod.expression0.type,
        )

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        if prod.expression0.type == "time" and prod.expression1.type == "time":
            raise ParsingError(
                "Time being multiplied by time " + f"near index {prod.index}"
            )

        if prod.expression0.type == "time" or prod.expression1.type == "time":
            return_type = "time"
        else:
            return_type = "number"

        return ExpressionResult(
            value=prod.expression0.value + prod.expression1.value + ("*",),
            type=return_type,
        )

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        if prod.expression1.type == "time":
            raise ParsingError(f"Time used as divisor near index {prod.index}")

        return ExpressionResult(
            value=prod.expression0.value + prod.expression1.value + ("/",),
            type=prod.expression0.type,
        )

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        if prod.expression0.type == "time" or prod.expression1.type == "time":
            raise ParsingError(
                f"Operation {prod.EXPONENT} used with time "
                + f"near index {prod.index}"
            )

        return ExpressionResult(
            value=prod.expression0.value + prod.expression1.value + ("^",),
            type=prod.expression0.type,
        )

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        return ExpressionResult(
            value=prod.expression.value + ("+₁",),
            type=prod.expression.type,
        )

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        return ExpressionResult(
            value=prod.expression.value + ("-₁",),
            type=prod.expression.type,
        )

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        return prod.expression

    @_("operand")
    def expression(self, prod: YaccProduction) -> ExpressionResult:
        return ExpressionResult(
            value=(prod.operand.value,),
            type=prod.operand.type,
        )

    @_("TIME_CONST")
    def operand(self, prod: YaccProduction) -> ExpressionResult:
        return ExpressionResult(
            value=prod.TIME_CONST,
            type="time",
        )

    @_("INT_CONST", "FLOAT_CONST")
    def operand(self, prod: YaccProduction) -> ExpressionResult:
        return ExpressionResult(
            value=getattr(prod, "INT_CONST") or getattr(prod, "FLOAT_CONST"),
            type="number",
        )


@dataclass
class VisualCalcStep:
    """Represents a single step in the calculation process."""

    operation: str | None
    stack: str | None
    input: str | None


def visualize_calc(postfixed_expr: tuple[str]) -> Generator[VisualCalcStep, None, None]:
    """Visualize the time calculation steps."""
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
    final_result = _to_time_or_num(final_result)
    yield VisualCalcStep(f"The result is {final_result}", None, None)


def _iter_to_str(iterable: Iterable[str]) -> str:
    return " ".join(iterable)


def _to_time_or_num(value: str) -> Time | int | float:
    if ":" in value:
        parts = tuple(map(int, value.split(":")))
        if len(parts) == 3:
            return Time(hours=parts[-3], minutes=parts[-2], seconds=parts[-1])
        return Time(minutes=parts[-2], seconds=parts[-1])
    return float(value) if "." in value else int(value)


def _handle_unary(operator: str, operand: str) -> tuple[str, str]:
    match operator:
        case "+₁":
            result = _to_time_or_num(operand)
            operation = f"+{operand} = {result}"
        case "-₁":
            if ":" in operand:
                result = Time() - _to_time_or_num(operand)
            else:
                result = 0 - _to_time_or_num(operand)
            operation = f"-{operand} = {result}"
        case _:
            raise ValueError(f"unknown operator '{operator}'")

    return str(result), operation


def _handle_binary(operator: str, operand_1: str, operand_2: str) -> tuple[str, str]:
    match operator:
        case "+₂":
            result = _to_time_or_num(operand_1) + _to_time_or_num(operand_2)
            operation = f"{operand_1} + {operand_2} = {result}"
        case "-₂":
            result = _to_time_or_num(operand_1) - _to_time_or_num(operand_2)
            operation = f"{operand_1} - {operand_2} = {result}"
        case "*":
            result = _to_time_or_num(operand_1) * _to_time_or_num(operand_2)
            result = _trim_time_or_num(result)
            operation = f"{operand_1} * {operand_2} = {result}"
        case "/":
            result = _to_time_or_num(operand_1) / _to_time_or_num(operand_2)
            result = _trim_time_or_num(result)
            operation = f"{operand_1} / {operand_2} = {result}"
        case "^":
            result = _to_time_or_num(operand_1) ** _to_time_or_num(operand_2)
            result = _trim_time_or_num(result)
            operation = f"{operand_1}^{operand_2} = {result}"
        case _:
            raise ValueError(f"unknown operator '{operator}'")

    return str(result), operation


def _trim_time_or_num(value: Time | int | float) -> Time | int | float:
    if isinstance(value, Time):
        return value
    if isinstance(value, int):
        return value
    return int(value) if value.is_integer() else value
