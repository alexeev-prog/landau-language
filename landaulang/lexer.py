from sly import Lexer


class LandauLexer(Lexer):
	tokens = {
		ID,
		BOOLVAL,
		INTVAL,
		STRING,
		PRINT,
		PRINTLN,
		INT,
		BOOL,
		SET,
		FUNCTION,
		IF,
		ELSE,
		WHILE,
		OUT,  # noqa: F821
		PLUS,
		MINUS,
		TIMES,
		DIVIDE,
		MOD,
		LTEQ,
		LT,
		GTEQ,
		GT,
		EQ,
		NOTEQ,
		AND,
		OR,
		NOT,  # noqa: F821
		LPAREN,
		RPAREN,
		BEGIN,
		END,
		ASSIGN,
		SEMICOLON,
		COLON,
		COMMA,
	}  # noqa: F821
	ignore = " \t\r"
	ignore_comment = r"\/\/.*"

	ID = r"[a-zA-Z_][a-zA-Z0-9_]*"	# a regex per token (except for the remapped ones)
	INTVAL = r"\d+"	 # N. B.: the order matters, first match will be taken
	PLUS = r"\+"
	MINUS = r"-"
	TIMES = r"\*"
	DIVIDE = r"/"
	MOD = r"%"
	LTEQ = r"<="
	LT = r"<"
	GTEQ = r">="
	GT = r">"
	EQ = r"=="
	NOTEQ = r"!="
	AND = r"\&\&"
	OR = r"\|\|"
	NOT = r"!"
	LPAREN = r"\("
	RPAREN = r"\)"
	BEGIN = r"\{"
	END = r"\}"
	ASSIGN = r"="
	COLON = r":"
	SEMICOLON = r";"
	COMMA = r","
	STRING = r'"[^"]*"'

	ID["True"] = BOOLVAL  # token remapping for keywords  # noqa: F821
	ID["False"] = (
		BOOLVAL	 # this is necessary because keywords match legal identifier pattern  # noqa: F821
	)
	ID["print"] = PRINT	 # noqa: F821
	ID["println"] = PRINTLN	 # noqa: F821
	ID["Integer"] = INT	 # noqa: F821
	ID["Boolean"] = BOOL  # noqa: F821
	ID["set"] = SET	 # noqa: F821
	ID["function"] = FUNCTION  # noqa: F821
	ID["if"] = IF  # noqa: F821
	ID["else"] = ELSE  # noqa: F821
	ID["while"] = WHILE	 # noqa: F821
	ID["out"] = OUT	 # noqa: F821

	@_(r"\n+")	# noqa: F821
	def ignore_newline(self, t):  # line number tracking
		self.lineno += len(t.value)

	def error(self, t):
		raise Exception("Line %d: illegal character %r" % (self.lineno, t.value[0]))
