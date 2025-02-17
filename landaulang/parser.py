from sly import Parser

from landaulang.enums import DataType
from landaulang.lexer import LandauLexer
from landaulang.syntree import (
	ArithOper,
	Assign,
	Boolean,
	Function,
	FunctionCall,
	IfThenElse,
	Integer,
	LogicOper,
	Print,
	Return,
	String,
	Variable,
	While,
)


class LandauParser(Parser):
	tokens = LandauLexer.tokens
	precedence = (	# arithmetic operators take precedence over logical operators
		("left", OR),
		("left", AND),
		("right", NOT),
		("nonassoc", LT, LTEQ, GT, GTEQ, EQ, NOTEQ),
		("left", PLUS, MINUS),
		("left", TIMES, DIVIDE, MOD),
		("right", UMINUS),	# unary operators
		("right", UPLUS),
	)

	@_("function_decl function_body")
	def function(self, p):
		return Function(*(p.function_decl[:-1] + p.function_body), p.function_decl[-1])

	@_("FUNCTION ID LPAREN [ param_list ] RPAREN [ COLON type ]")
	def function_decl(self, p):
		deco, name, params = (
			{"type": (p.type or DataType.VOID), "lineno": p.lineno},
			p[1],
			(p.param_list or []),
		)
		return [name, params, deco]

	@_("param { COMMA param }")
	def param_list(self, p):
		return [p.param0] + p.param1

	@_("ID COLON type")
	def param(self, p):
		return (p[0], {"type": p.type, "lineno": p.lineno})

	@_("BEGIN [ set_list ] [ function_list ] [ statement_list ] END")
	def function_body(self, p):
		return [p.set_list or [], p.function_list or [], p.statement_list or []]

	@_("set { set }")
	def set_list(self, p):
		return [p.set0] + p.set1

	@_("SET ID COLON type SEMICOLON")
	def set(self, p):
		return (p[1], {"type": p.type, "lineno": p.lineno})

	@_("function { function }")
	def function_list(self, p):
		return [p.function0] + p.function1

	@_("statement { statement }")
	def statement_list(self, p):
		return [p.statement0] + p.statement1

	@_("WHILE expr BEGIN [ statement_list ] END")
	def statement(self, p):
		return While(p.expr, p.statement_list or [], {"lineno": p.lineno})

	@_(
		"IF expr BEGIN [ statement_list ] END [ ELSE BEGIN statement_list_optional END ]"
	)
	def statement(self, p):
		return IfThenElse(
			p.expr,
			p.statement_list or [],
			p.statement_list_optional or [],
			{"lineno": p.lineno},
		)

	@_("statement_list")  # sly does not support nested
	def statement_list_optional(self, p):  # optional targets, therefore
		return p.statement_list	 # this rule

	@_("")
	def statement_list_optional(self, p):
		return []

	@_("PRINT	STRING SEMICOLON", "PRINTLN STRING SEMICOLON")
	def statement(self, p):
		return Print(String(p[1][1:-1]), p[0] == "println", {"lineno": p.lineno})

	@_("PRINT	expr SEMICOLON", "PRINTLN expr SEMICOLON")
	def statement(self, p):
		return Print(p.expr, p[0] == "println", {"lineno": p.lineno})

	@_("OUT SEMICOLON")
	def statement(self, p):
		return Return(None, {"lineno": p.lineno})

	@_("OUT expr SEMICOLON")
	def statement(self, p):
		return Return(p.expr, {"lineno": p.lineno})

	@_("ID ASSIGN expr SEMICOLON")
	def statement(self, p):
		return Assign(p[0], p.expr, {"lineno": p.lineno})

	@_("ID LPAREN [ args ] RPAREN SEMICOLON")
	def statement(self, p):
		return FunctionCall(p[0], p.args or [], {"lineno": p.lineno})

	@_("MINUS expr %prec UMINUS")
	def expr(self, p):
		return ArithOper("-", Integer(0), p.expr, {"lineno": p.lineno})

	@_("PLUS expr %prec UPLUS", "LPAREN expr RPAREN")
	def expr(self, p):
		return p.expr

	@_(
		"expr PLUS expr",
		"expr MINUS expr",
		"expr TIMES expr",
		"expr DIVIDE expr",
		"expr MOD expr",
	)
	def expr(self, p):
		return ArithOper(p[1], p.expr0, p.expr1, {"lineno": p.lineno})

	@_(
		"expr LT expr",
		"expr LTEQ expr",
		"expr GT expr",
		"expr GTEQ expr",
		"expr EQ expr",
		"expr NOTEQ expr",
		"expr AND expr",
		"expr OR expr",
	)
	def expr(self, p):
		return LogicOper(p[1], p.expr0, p.expr1, {"lineno": p.lineno})

	@_("NOT expr")
	def expr(self, p):
		return LogicOper("==", Boolean("False"), p.expr, {"lineno": p.lineno})

	@_("ID")
	def expr(self, p):
		return Variable(p[0], {"lineno": p.lineno})

	@_("ID LPAREN [ args ] RPAREN")
	def expr(self, p):
		return FunctionCall(p[0], p.args or [], {"lineno": p.lineno})

	@_("expr { COMMA expr }")
	def args(self, p):
		return [p.expr0] + p.expr1

	@_("INTVAL")
	def expr(self, p):
		return Integer(int(p.INTVAL), {"lineno": p.lineno})

	@_("BOOLVAL")
	def expr(self, p):
		return Boolean(p.BOOLVAL == "True", {"lineno": p.lineno})

	@_("INT", "BOOL")
	def type(self, p):
		return DataType.INTEGER if p[0] == "integer" else DataType.BOOLEAN

	def error(self, token):
		if not token:
			raise Exception("Syntax error: unexpected EOF")
		raise Exception(f"Syntax error at line {token.lineno}, token={token}")
