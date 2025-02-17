from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, List


class Node(ABC):
	@abstractmethod
	def __init__(self):
		raise NotImplementedError


class Print(Node):
	def __init__(self, expr: str, newline: bool, deco: Optional[Dict[Any, Any]] = None):
		self.expr = expr
		self.newline = newline
		self.deco = deco or {}


class Return(Node):
	def __init__(self, expr: str, deco: Optional[Dict[Any, Any]] = None):
		self.expr = expr
		self.deco = deco or {}


class Assign(Node):
	def __init__(self, name: str, expr: str, deco: Optional[Dict[Any, Any]] = None):
		self.name = name
		self.expr = expr
		self.deco = deco or {}


class While(Node):
	def __init__(self, expr: str, body: List[Node], deco: Optional[Dict[Any, Any]] = None):
		self.expr = expr
		self.body = body
		self.deco = deco or {}


class IfThenElse(Node):
	def __init__(self, expr: str, ibody: List[Node], ebody: List[Node], deco: Optional[Dict[Any, Any]] = None):
		self.expr = expr
		self.ibody = ibody
		self.ebody = ebody
		self.deco = deco or {}
