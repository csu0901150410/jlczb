#coding=utf-8

from enum import Enum

# 层属性枚举
class LayerContext(Enum):
	LAYER_CONTEXT_BOARD = "board"
	LAYER_CONTEXT_MISC = "misc"

# 层类型枚举
class LayerType(Enum):
	SIGNAL = "signal"
	POWER_GROUND = "power_ground"
	MIXED = "mixed"
	SOLDER_MASK = "solder_mask"
	SILK_SCREEN = "silk_screen"
	SOLDER_PASTE = "solder_paste"
	DRILL = "drill"
	ROUT = "rout"
	DOCUMENT = "document"
	COMPONENT = "component"
	MASK = "mask"
	COND_PASTE = "cond_paste"
	COVERLAY = "coverlay"
	PI_STIFFENER = "pi_stifener"
	GP_STIFFENER = "gp_stiffener"
	FR4_STIFFENER = "fr4_stiffener"
	PS_STIFFENER = "3m_stiffener"
	ESCOAT = "escoat"
	DRAWING = "drawing"

# 极性枚举
class Polarity(Enum):
	POSITIVE = True
	NEGATIVE = False


'''
层表示
'''

class JlccamLayer:
	def __init__(self, context, name, polarity, order, type, start = "", end = ""):
		self.context = context
		self.name = name
		self.polarity = polarity
		self.order = order
		self.type = type
		self.start = start
		self.end = end

	def __str__(self) -> str:
		return f"Jlccam Layer(name={self.name},context={self.context},type={self.type},polarity={self.polarity},order={self.order},start={self.start},end={self.end}"
	
	def __repr__(self) -> str:
		return self.__str__()
