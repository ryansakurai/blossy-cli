"""
Module dedicated to functionalities of the 'calct' command
"""
from datetime import timedelta
from typing import Dict, List, Optional, Tuple
from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class CalcTimeLexer(Lexer):
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
    pass


class CalcTimeParser(Parser):
    tokens = CalcTimeLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "EXPONENT", "UNARY_PLUS", "UNARY_MINUS"),
    )

    def error(self, token: Optional[Token]):
        if token:
            raise ParsingError(f"Operation absent or used incorrectly near index {token.index}")
        raise ParsingError("Operation absent or used incorrectly near the end of input")


    @_("expression")
    def start(self, prod: YaccProduction) -> timedelta:
        if not isinstance(prod.expression, timedelta):
            raise ParsingError("Result is not time (use 'calc' instead)")

        return prod.expression

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        if isinstance(prod.expression0, timedelta) and not isinstance(prod.expression1, timedelta):
            raise ParsingError("Number being added to time " + \
                               f"near index {prod.index}")
        if not isinstance(prod.expression0, timedelta) and isinstance(prod.expression1, timedelta):
            raise ParsingError("Time being added to number " + \
                               f"near index {prod.index}")

        return prod.expression0 + prod.expression1

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        if isinstance(prod.expression0, timedelta) and not isinstance(prod.expression1, timedelta):
            raise ParsingError("Number being subtracted from time " + \
                               f"near index {prod.index}")
        if not isinstance(prod.expression0, timedelta) and isinstance(prod.expression1, timedelta):
            raise ParsingError("Time being subtracted from number " + \
                               f"near index {prod.index}")

        return prod.expression0 - prod.expression1

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        if isinstance(prod.expression0, timedelta) and isinstance(prod.expression1, timedelta):
            raise ParsingError("Time being multiplied by time " + \
                               f"near index {prod.index}")

        return prod.expression0 * prod.expression1

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        if isinstance(prod.expression1, timedelta):
            raise ParsingError(f"Time used as divisor near index {prod.index}")

        return prod.expression0 / prod.expression1

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> int|float:
        if isinstance(prod.expression0, timedelta) or isinstance(prod.expression1, timedelta):
            raise ParsingError(f"Operation {prod.EXPONENT} used with time " + \
                               f"near index {prod.index}")

        return prod.expression0 ** prod.expression1

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        return prod.expression

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        if isinstance(prod.expression, timedelta):
            return timedelta() - prod.expression
        return 0 - prod.expression

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        return prod.expression

    @_("operand")
    def expression(self, prod: YaccProduction) -> timedelta|int|float:
        return prod.operand

    @_("TIME_CONST")
    def operand(self, prod: YaccProduction) -> timedelta:
        parts = tuple(map(int, prod.TIME_CONST.split(":")))
        if len(parts) == 3:
            value = timedelta(hours=parts[-3], minutes=parts[-2], seconds=parts[-1])
        else:
            value = timedelta(minutes=parts[-2], seconds=parts[-1])

        return value

    @_("INT_CONST")
    def operand(self, prod: YaccProduction) -> int:
        return int(prod.INT_CONST)

    @_("FLOAT_CONST")
    def operand(self, prod: YaccProduction) -> float:
        return float(prod.FLOAT_CONST)


class VisualCalcTimeParser(Parser):
    tokens = CalcTimeLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "EXPONENT", "UNARY_PLUS", "UNARY_MINUS"),
    )

    def error(self, token: Optional[Token]):
        if token:
            raise ParsingError(f"Operation absent or used incorrectly near index {token.index}")
        raise ParsingError("Operation absent or used incorrectly near the end of input")


    @_("expression")
    def start(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        if prod.expression["type"] == "number":
            raise ParsingError("Result is not time (use 'calc' instead)")

        return prod.expression["value"]

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        if prod.expression0["type"] == "time" and prod.expression1["type"] == "number":
            raise ParsingError("Number being added to time " + \
                               f"near index {prod.index}")
        if prod.expression0["type"] == "number" and prod.expression1["type"] == "time":
            raise ParsingError("Time being added to number " + \
                               f"near index {prod.index}")

        return {
            "value": prod.expression0["value"] + prod.expression1["value"] + ("+₂", ),
            "type": prod.expression0["type"],
        }

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        if prod.expression0["type"] == "time" and prod.expression1["type"] == "number":
            raise ParsingError("Number being subtracted from time " + \
                               f"near index {prod.index}")
        if prod.expression0["type"] == "number" and prod.expression1["type"] == "time":
            raise ParsingError("Time being subtracted from number " + \
                               f"near index {prod.index}")

        return {
            "value": prod.expression0["value"] + prod.expression1["value"] + ("-₂", ),
            "type": prod.expression0["type"],
        }

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        if prod.expression0["type"] == "time" and prod.expression1["type"] == "time":
            raise ParsingError("Time being multiplied by time " + \
                               f"near index {prod.index}")

        if prod.expression0["type"] == "time" or prod.expression1["type"] == "time":
            return_type = "time"
        else:
            return_type = "number"

        return {
            "value": prod.expression0["value"] + prod.expression1["value"] + ("*", ),
            "type": return_type,
        }

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        if prod.expression1["type"] == "time":
            raise ParsingError(f"Time used as divisor near index {prod.index}")

        return {
            "value": prod.expression0["value"] + prod.expression1["value"] + ("/", ),
            "type": prod.expression0["type"],
        }

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        if prod.expression0["type"] == "time" or prod.expression1["type"] == "time":
            raise ParsingError(f"Operation {prod.EXPONENT} used with time " + \
                               f"near index {prod.index}")

        return {
            "value": prod.expression0["value"] + prod.expression1["value"] + ("^", ),
            "type": prod.expression0["type"],
        }

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        prod.expression["value"] += ("+₁", )
        return prod.expression

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        prod.expression["value"] += ("-₁", )
        return prod.expression

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        return prod.expression

    @_("operand")
    def expression(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        prod.operand["value"] = (prod.operand["value"], )
        return prod.operand

    @_("TIME_CONST")
    def operand(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        return {
            "value": prod.TIME_CONST,
            "type": "time",
        }

    @_("INT_CONST", "FLOAT_CONST")
    def operand(self, prod: YaccProduction) -> Dict[str, Tuple[str]|str]:
        return {
            "value": getattr(prod, "INT_CONST") or getattr(prod, "FLOAT_CONST"),
            "type": "number",
        }


class CalcTimeVisualizer:
    UNARY_OPERATORS = ("+₁", "-₁")
    BINARY_OPERATORS = ("+₂", "-₂", "*", "/", "^")

    def __init__(self, values: Tuple[str]) -> None:
        self.values_tuple = values

    def visualize(self):
        stack: List[str] = ["$"]
        values = list(self.values_tuple) + ["$"]
        yield None, " ".join(stack), " ".join(values)

        while len(values) > 1:
            value = values[0]
            values.pop(0)

            if value in self.UNARY_OPERATORS:
                operand = stack.pop()
                operator = value
                result, operation = self.__handle_unary(operator, operand)
                stack.append(result)
            elif value in self.BINARY_OPERATORS:
                operand2 = stack.pop()
                operand1 = stack.pop()
                operator = value
                result, operation = self.__handle_binary(operator, operand1, operand2)
                stack.append(result)
            else:
                number = value
                stack.append(number)
                operation = f"Stack {number}"

            stack_str = " ".join(stack)
            values_str = " ".join(values)
            yield operation, stack_str, values_str

        final_result = stack.pop()
        yield f"The result is {final_result}", None, None

    def __from_str(self, operand: str) -> timedelta|int|float:
        if ":" in operand:
            parts = tuple(map(int, operand.split(":")))
            if len(parts) == 3:
                value = timedelta(hours=parts[-3], minutes=parts[-2], seconds=parts[-1])
            else:
                value = timedelta(minutes=parts[-2], seconds=parts[-1])
            return value
        if "." in operand:
            float(operand)
        return int(operand)

    def __to_str(self, operand: timedelta|int|float) -> str:
        if isinstance(operand, timedelta):
            total_seconds = int(operand.total_seconds())
            hours, remainder = divmod(total_seconds, 60*60)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        if isinstance(operand, float):
            operand = int(operand) if operand.is_integer() else operand
            return str(operand)
        return str(operand)

    def __handle_unary(self,
                       operator: str,
                       operand: str) -> Tuple[str, str]:
        match operator:
            case "+₁":
                result = operand
                operation = f"+{operand} = {result}"
            case "-₁":
                if isinstance(operand, timedelta):
                    result = timedelta() - self.__from_str(operand)
                else:
                    result = 0 - self.__from_str(operand)
                result = self.__to_str(result)
                operation = f"-{operand} = {result}"

        return result, operation

    def __handle_binary(self,
                       operator: str,
                       operand1: timedelta|int|float,
                       operand2: timedelta|int|float) -> Tuple[timedelta|int|float, str]:
        match operator:
            case "+₂":
                result = self.__from_str(operand1) + self.__from_str(operand2)
                result = self.__to_str(result)
                operation = f"{operand1} + {operand2} = {result}"
            case "-₂":
                result = self.__from_str(operand1) - self.__from_str(operand2)
                result = self.__to_str(result)
                operation = f"{operand1} - {operand2} = {result}"
            case "*":
                result = self.__from_str(operand1) * self.__from_str(operand2)
                result = self.__to_str(result)
                operation = f"{operand1} * {operand2} = {result}"
            case "/":
                result = self.__from_str(operand1) / self.__from_str(operand2)
                result = self.__to_str(result)
                operation = f"{operand1} / {operand2} = {result}"
            case "^":
                result = self.__from_str(operand1) ** self.__from_str(operand2)
                result = self.__to_str(result)
                operation = f"{operand1}^{operand2} = {result}"

        return result, operation
