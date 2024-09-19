from typing import Union
from typing import Optional
from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class CalcLexer(Lexer):
    tokens = (
        "FLOAT_CONST",
        "INT_CONST",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "EXPONENT",
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
        else:
            raise ParsingError("Operation absent or used incorrectly near the end of input")


    @_('expression')
    def start(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression

    @_("expression PLUS expression")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression0 + prod.expression1

    @_("expression MINUS expression")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression0 - prod.expression1

    @_("expression TIMES expression")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression0 * prod.expression1

    @_("expression DIVIDE expression")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression0 / prod.expression1

    @_("expression EXPONENT expression")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression0 ** prod.expression1

    @_("PLUS expression %prec UNARY_PLUS")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression

    @_("MINUS expression %prec UNARY_MINUS")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return 0 - prod.expression

    @_("L_PARENTH expression R_PARENTH")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.expression

    @_("number")
    def expression(self, prod: YaccProduction) -> Union[int, float]:
        return prod.number

    @_("INT_CONST")
    def number(self, prod: YaccProduction) -> int:
        return int(prod.INT_CONST)

    @_("FLOAT_CONST")
    def number(self, prod: YaccProduction) -> float:
        return float(prod.FLOAT_CONST)
