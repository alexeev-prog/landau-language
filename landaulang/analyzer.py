from landaulang.enums import DataType
from landaulang.symboltable import SymbolTable
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


def build_symtable(ast):
	if (
		not isinstance(ast, Function)
		or ast.name != "main"
		or ast.deco["type"] != DataType.VOID
		or len(ast.args) > 0
	):
		raise Exception("Cannot find a valid entry point")
	symtable = SymbolTable()
	process_scope(ast, symtable)


def process_scope(function, symtable):
	function.deco["nonlocal"] = (
		set()
	)  # set of nonlocal variable names in the functionction body, used in "readable" python transpilation only
	symtable.push_scope(function.deco)
	for v in function.args:	 # process functionction arguments
		symtable.add_var(*v)
	for v in function.var:	# process local variables
		symtable.add_var(*v)
	for f in function.function:	 # then process nested functionction bodies
		process_scope(f, symtable)
	for s in function.body:	 # process the list of statements
		process_stat(s, symtable)
	symtable.pop_scope()


def process_stat(n, symtable):	# process "statement" syntax tree nodes
	if isinstance(n, Print):
		process_expr(n.expr, symtable)
	elif isinstance(n, Return):
		if n.expr is None:
			return
		process_expr(n.expr, symtable)
	elif isinstance(n, Assign):
		process_expr(n.expr, symtable)
		deco = symtable.find_var(n.name)
		update_nonlocals(
			n.name, symtable
		)  # used in "readable" python transpilation only
	elif isinstance(n, FunctionCall):  # no type checking is necessary
		process_expr(n, symtable)
	elif isinstance(n, While):
		process_expr(n.expr, symtable)
		for s in n.body:
			process_stat(s, symtable)
	elif isinstance(n, IfThenElse):
		process_expr(n.expr, symtable)
		for s in n.ibody + n.ebody:
			process_stat(s, symtable)
	else:
		raise Exception("Unknown statement type")


def process_expr(n, symtable):	# process "expression" syntax tree nodes
	if isinstance(n, ArithOper):
		process_expr(n.left, symtable)
		process_expr(n.right, symtable)
	elif isinstance(n, LogicOper):
		process_expr(n.left, symtable)
		process_expr(n.right, symtable)
	elif isinstance(n, Integer):
		n.deco["type"] = DataType.INTEGER
	elif isinstance(n, Boolean):
		n.deco["type"] = DataType.BOOLEAN
	elif isinstance(n, Variable):
		deco = symtable.find_var(n.name)
		update_nonlocals(
			n.name, symtable
		)  # used in "readable" python transpilation only
	elif isinstance(n, FunctionCall):
		for s in n.args:
			process_expr(s, symtable)
	elif isinstance(n, String):
		pass
	else:
		raise Exception("Unknown expression type", n)


def update_nonlocals(var, symtable):  # add the variable name to the set of nonlocals
	for i in reversed(
		range(len(symtable.variables))
	):	# for all the enclosing scopes until we find the instance
		if var in symtable.variables[i]:
			break  # used in "readable" python transpilation only
		symtable.ret_stack[i]["nonlocal"].add(var)
