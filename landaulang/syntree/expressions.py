from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Tuple
from landaulang.enums import DataType


class Expression(ABC):
	@abstractmethod
	def __init__(self):
		raise NotImplementedError


class ArithOper(Expression):
	def __init__(self, oper: Any, left: Any, right: Any, deco: Optional[Dict[Any, Any]] = None):
		self.oper = oper
		self.left = left
		self.right = right
		self.deco = (deco or {}) | {'type': DataType.INTEGER}


class LogicOper(Expression):
	def __init__(self, oper: Any, left: Any, right: Any, deco: Optional[Dict[Any, Any]] = None):
		self.oper = oper
		self.left = left
		self.right = right
		self.deco = (deco or {}) | {'type': DataType.BOOLEAN}


class Integer(Expression):
	def __init__(self, value: int, deco: Optional[Dict[Any, Any]] = None):
		self.value = value
		self.deco = (deco or {}) | {'type': DataType.INTEGER}


class Boolean(Expression):
	def __init__(self, value: bool, deco: Optional[Dict[Any, Any]] = None):
		self.value = value
		self.deco = (deco or {}) | {'type': DataType.BOOLEAN}


class String(Expression):
	def __init__(self, value: str, deco: Optional[Dict[Any, Any]] = None):
		self.value = value
		self.deco = (deco or {}) | {'type': DataType.STRING}


class Variable(Expression):
	def __init__(self, name: str, deco: Optional[Dict[Any, Any]] = None):
		self.name = name
		self.deco = deco or {}


class FunctionCall(Expression):
	"""
	This class describes a function call.

	Can be a statement OR a expression
	"""

	def __init__(self, name: str, args: List[Tuple[Any]], deco: Optional[Dict[Any, Any]] = None):
		self.name = name
		self.args = args
		self.deco = deco or {}
