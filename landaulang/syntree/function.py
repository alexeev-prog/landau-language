from typing import List, Tuple, Any, Optional, Dict
from landaulang.syntree.statements import Node


class Function:
	"""
	This class describes a function.
	"""

	def __init__(self, name: str, args: List[Tuple[Any]], var: List[Tuple[Any]],
						function: List['Function'], body: List[Node], deco: Optional[Dict[Any, Any]] = None):
		"""
		Constructs a new instance.

		:param      name:      The name
		:type       name:      str
		:param      args:      The arguments
		:type       args:      List[Tuple[Any]]
		:param      var:       The variable
		:type       var:       List[Tuple[Any]]
		:param      function:  The function
		:type       function:  List[Function]
		:param      body:      The body
		:type       body:      List[Node]
		:param      deco:      The deco
		:type       deco:      Optional[Dict[Any, Any]]
		"""
		self.name = name
		self.args = args
		self.var = var
		self.function = function
		self.body = body
		self.deco = deco if deco else {}
