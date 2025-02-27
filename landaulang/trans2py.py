from landaulang.syntree import (
	ArithOper,
	Assign,
	Boolean,
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


def transpy(n):
	funname = n.name
	funargs = ", ".join([v for v, t in n.args])
	nonlocals = (
		("nonlocal " + ", ".join([v for v in n.deco["nonlocal"]]))
		if len(n.deco["nonlocal"])
		else "pass # no non-local variables"
	)
	allocvars = "".join(["%s = None\n" % v for v, t in n.var])
	nestedfunction = "".join(transpy(f) for f in n.function)
	functionbody = "".join([stat(s) for s in n.body])
	return (
		f"def {funname}({funargs}):\n"
		+ indent(f"{nonlocals}\n{allocvars}\n{nestedfunction}\n{functionbody}\n")
		+ (f"\n{funname}()\n" if n.name == "main" else "")
	)


def stat(n):
	if isinstance(n, Print):
		return "print(%s, end=%s)\n" % (expr(n.expr), ["''", "'\\n'"][n.newline])
	elif isinstance(n, Return):
		return "return %s\n" % (expr(n.expr) if n.expr is not None else "")
	elif isinstance(n, Assign):
		return "%s = %s\n" % (n.name, expr(n.expr))
	elif isinstance(n, FunctionCall):
		return expr(n) + "\n"
	elif isinstance(n, While):
		return "while %s:\n" % expr(n.expr) + indent(
			[stat(s) for s in n.body] or "pass"
		)
	elif isinstance(n, IfThenElse):
		return "if %s:\n%selse:\n%s\n" % (
			expr(n.expr),
			indent([stat(s) for s in n.ibody] or "pass"),
			indent([stat(s) for s in n.ebody] or "pass"),
		)

	raise Exception(f"Unknown statement type: {n}")


def expr(n):
	if isinstance(n, ArithOper) or isinstance(n, LogicOper):
		pyeq = {"||": "or", "&&": "and"}
		pyop = pyeq[n.oper] if n.oper in pyeq else n.oper
		return "(%s) %s (%s)" % (expr(n.left), pyop, expr(n.right))
	elif isinstance(n, Integer) or isinstance(n, Boolean):
		return str(n.value)
	elif isinstance(n, String):
		return '"' + n.value + '"'
	elif isinstance(n, Variable):
		return n.name
	elif isinstance(n, FunctionCall):
		return "%s(%s)" % (n.name, ", ".join([expr(s) for s in n.args]))
	raise Exception("Unknown expression type", n)


def indent(array):
	multiline = "".join([str(entry) for entry in array])

	if multiline == "":
		return ""

	return "\t" + "\n\t".join(multiline.splitlines()) + "\n"
