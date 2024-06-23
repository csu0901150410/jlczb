#coding=utf-8

from enum import Enum
from .client import socket_client

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

class JlccamJobInfo:
	"""料号信息类。记录料号名称、进程id、通信端口号
	"""	

	def __init__(self, jobname, pid, port):
		"""初始化料号信息实例

		Args:
			jobname (str): 料号名称
			pid (int): 进程id
			port (int): 通信端口号
		"""		
		self.jobname = jobname
		self.pid = pid
		self.port = port

	def __str__(self):
		return f"JlccamJobInfo(jobname={self.jobname}, pid={self.pid}, port={self.port})"

class JlccamJob:
	"""料号客户端类。对料号的一系列处理都要通过料号客户端
	"""	

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.client = socket_client(ip, port)

	# 调用脚本
	def call_script(self, command : str, param = {}):
		return self.client.send_command(command, param)

	# 获取料号名
	def get_jobname(self):
		ret = self.call_script("script_get_job_name")
		jobname = ret["result"]
		return jobname

	def close(self):
		self.client.send_command("script_quit_app")
		self.client.stop()

	def add_step(self, stepname : str):
		ret = self.call_script("script_add_step", stepname)
		return ret
	
	def del_step(self, stepname : str):
		ret = self.call_script("script_del_step", stepname)
		return ret
	
	def copy_step(self, from_stepname : str, to_stepname : str, flip : bool = False):
		param = {
			"src": from_stepname,
			"des": to_stepname,
			"flip": flip,
		}

		ret = self.call_script("script_copy_step", param)
		return ret
	
	def rename_step(self, from_stepname : str, to_stepname : str):
		param = {
			"stepname": from_stepname,
			"newname": to_stepname,
		}

		ret = self.call_script("script_step_rename", param)
		return ret
	
	def set_work_layer(self, stepname : str, layername : str):
		param = {
			"stepname": stepname,
			"layername": layername,
		}

		ret = self.call_script("script_make_work_layer", param)
		return ret
	
	def set_affect_layer(self, stepname : str, layername : str, affect : bool):
		param = {
			"stepname": stepname,
			"layername": layername,
			"affect": affect,
		}

		ret = self.call_script("script_affect_layer", param)
		return ret
	
	def set_only_work_layer(self, stepname : str, layername : str):
		param = {
			"stepname": stepname,
			"layername": layername,
		}

		ret = self.call_script("script_make_only_work_layer", param)
		return ret
	
	# 显示工作层所在的step所有层,工作层不存在则显示第一个step所有层
	def show_all_layer(self):
		ret = self.call_script("script_show_all_layer")
		return ret
	
	def autosort_layer(self, stepname : str):
		ret = self.call_script("script_autosort_layer", stepname)
		return ret
	
	def step_profile_to_outline(self, stepname : str, layername : str, linewidth : float, polarity : bool):
		param = {
			"stepname": stepname,
			"layername": layername,
			"linewidth": linewidth,
			"polarity": polarity,
		}

		ret = self.call_script("script_profile_to_outline", param)
		return ret
	

	def add_layer(self, layername : str, layertype : str, board : bool, positive : bool):
		if isinstance(layertype, LayerType):
			layertype = layertype.value

		if isinstance(positive, Polarity):
			positive = positive.value
		
		param = {
			"board": board,
			"layername": layername,
			"layertype": layertype,
			"polarity": positive,
		}
		
		ret = self.call_script("script_add_layer", param)
		return ret

	def del_layer(self, layername : str):
		ret = self.call_script("script_del_layer", layername)
		return ret

	def rename_layer(self, from_layername : str, to_layername : str):
		param = {
			"layername": from_layername,
			"new_layername": to_layername,
		}

		ret = self.call_script("script_rename_layer", param)
		return ret
	
	# 位置单位是mm
	def add_pad(self, symbol : str, x : float, y : float):
		
		position = {
			"x": x,
			"y": y
		}

		param = {
			"symbol": symbol,
			"polarity": True,
			"angle": 0,
			"mirrx": False,
			"mirry": False,
			"position": position,
			"detx": 0,
			"dety": 0,
			"nx": 1,
			"ny": 1
		}

		ret = self.call_script("script_add_pad", param)
		return ret

