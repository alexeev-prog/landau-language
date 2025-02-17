class SymbolTable:
	def __init__(self):
		self.variables = [{}]
		self.ret_stack = [None]

	def add_var(self, name, deco):
		if name in self.variables[-1]:
			raise Exception(f"Double declaration of the variable {name}")
		self.variables[-1][name] = deco

	def push_scope(self, deco):
		self.variables.append({})
		self.ret_stack.append(deco)

	def pop_scope(self):
		self.variables.pop()
		self.ret_stack.pop()

	def find_var(self, name):
		for i in reversed(range(len(self.variables))):
			if name in self.variables[i]:
				return self.variables[i][name]
		raise Exception(f"No declaration for the variable {name}")
