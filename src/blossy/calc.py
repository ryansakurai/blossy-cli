"""
Module dedicated to functionalities of the 'calc' command
"""
from typing import List, Optional, Tuple
from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class CalcLexer(Lexer):
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
    pass

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "EXPONENT", "UNARY_PLUS", "UNARY_MINUS"),
    )

    def error(self, token: Optional[Token]):
        if token:
            raise ParsingError(f"Operation absent or used incorrectly near index {token.index}")
        raise ParsingError("Operation absent or used incorrectly near the end of input")


    @_('expression')
    def start(self, prod: YaccProduction) -> int|float:
        return self.__normalize_num(prod.expression)

    def __normalize_num(self, num: int|float) -> int|float:
        if isinstance(num, int):
            return num
        return int(num) if num.is_integer() else round(num, 2)

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression0 + prod.expression1

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression0 - prod.expression1

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression0 * prod.expression1

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression0 / prod.expression1

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression0 ** prod.expression1

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> int|float:
        return 0 - prod.expression

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.expression

    @_("number")
    def expression(self, prod: YaccProduction) -> int|float:
        return prod.number

    @_("INT_CONST")
    def number(self, prod: YaccProduction) -> int:
        return int(prod.INT_CONST)

    @_("FLOAT_CONST")
    def number(self, prod: YaccProduction) -> float:
        return float(prod.FLOAT_CONST)

class VisualCalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "EXPONENT", "UNARY_PLUS", "UNARY_MINUS"),
    )

    def error(self, token: Optional[Token]):
        if token:
            raise ParsingError(f"Operation absent or used incorrectly near index {token.index}")
        raise ParsingError("Operation absent or used incorrectly near the end of input")


    @_('expression')
    def start(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression0 + prod.expression1 + ("+₂", )

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression0 + prod.expression1 + ("-₂", )

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression0 + prod.expression1 + ("*", )

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression0 + prod.expression1 + ("/", )

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression0 + prod.expression1 + ("^", )

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression + ("+₁", )

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression + ("-₁", )

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return prod.expression

    @_("number")
    def expression(self, prod: YaccProduction) -> Tuple[str]:
        return (prod.number, )

    @_("INT_CONST")
    def number(self, prod: YaccProduction) -> int:
        return prod.INT_CONST

    @_("FLOAT_CONST")
    def number(self, prod: YaccProduction) -> float:
        return prod.FLOAT_CONST

class CalcVisualizer:
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
        final_result = self.___to_num(final_result)
        final_result = round(final_result, 2)
        yield f"The result is {final_result}", None, None

    def ___to_num(self, num: str) -> int|float:
        return float(num) if "." in num else int(num)

    def __handle_unary(self,
                       operator: str,
                       operand: str) -> Tuple[str, str]:
        match operator:
            case "+₁":
                result = self.___to_num(operand)
                operation = f"+{operand} = {result}"
            case "-₁":
                result = 0 - self.___to_num(operand)
                operation = f"-{operand} = {result}"

        return str(result), operation

    def __handle_binary(self,
                       operator: str,
                       operand1: int|float,
                       operand2: int|float) -> Tuple[int|float, str]:
        match operator:
            case "+₂":
                result = self.___to_num(operand1) + self.___to_num(operand2)
                operation = f"{operand1} + {operand2} = {result}"
            case "-₂":
                result = self.___to_num(operand1) - self.___to_num(operand2)
                operation = f"{operand1} - {operand2} = {result}"
            case "*":
                result = self.___to_num(operand1) * self.___to_num(operand2)
                result = self.__trim_num(result)
                operation = f"{operand1} * {operand2} = {result}"
            case "/":
                result = self.___to_num(operand1) / self.___to_num(operand2)
                result = self.__trim_num(result)
                operation = f"{operand1} / {operand2} = {result}"
            case "^":
                result = self.___to_num(operand1) ** self.___to_num(operand2)
                result = self.__trim_num(result)
                operation = f"{operand1}^{operand2} = {result}"

        return str(result), operation

    def __trim_num(self, num: int|float) -> int|float:
        if isinstance(num, int):
            return num
        return int(num) if num.is_integer() else num
