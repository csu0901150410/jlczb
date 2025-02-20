#coding=utf-8

from .client import socket_client
import utils as utils
from .JlccamLayer import *

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

	def save(self):
		ret = self.call_script("script_save")
		return ret

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
	
	def get_layers(self):
		ret = self.call_script("script_get_layers")
		ret = ret["result"]
		# print(ret)
		layers = []
		for item in ret:
			context = item["context"]
			layername = item["layername"]
			polarity = item["polarity"]
			start = item["start"]
			end = item["end"]
			order = item["order"]
			layertype = item["layertype"]
			layer = JlccamLayer(context, layername, polarity, order, layertype, start, end)
			layers.append(layer)
		return layers
	
	def get_steps(self):
		ret = self.call_script("script_get_steps")
		return ret["result"]
	
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
	
	def import_tgz(self, tgz_path):
		param = {}
		param["tgz"] = tgz_path
		param["step"] = []
		param["layer"] = []
		param["prefix"] = ""
		ret = self.call_script("script_import_tgz", param)
		return ret
	
	def import_ddw(self, ddw_path):
		ret = self.call_script("script_open_ddw", utils.path_rel2abs(ddw_path))
		return ret
	
	def import_gerbers(self, gerber_path, jobname, stepname : str = "orig", repeat_aperture : bool = False):
		param = {}
		param["jobname"] = gerber_path
		param["path"] = jobname
		param["step"] = stepname
		param["repeat_aperture"] = repeat_aperture
		ret = self.call_script("script_import_gerber_dir", param)
		return ret
	
	def export_gerber(self, path, step, layers):

		params = {}
		params["path"] = utils.path_rel2abs(path)
		params["step"] = step
		params["prefix"] = ""
		params["suffix"] = ""
		params["check"] = False
		params["allow_zerosymbol"] = True
		params["inherit_taillstep"] = False
		params["format"] = {
			"breakrepeat" : True,
			"format" : "2:5",
			"lzero" : "lz",
			"surfaceraster" : True,
			"filmminbus" : 1,
			"unit" : "inch",
			"drillrepeat" : True,
			"drillbreaktext" : True,
			"drilloptpath" : True,
			"drilljump" : False,
			"drilljumpholedis" : 0.8,
			"drlformat" : "3:3",
			"drillsortbyscript" : True,
			"drllzero" : "tz",
			"drlunit" : "mm",
			"routrepeat" : False,
			"routformat" : "3:3",
			"routlzero" : "tz",
			"routunit" : "mm"
		}

		jslayers = []
		for layer in layers:
			# print(layer)
			layercontext = layer.context
			layername = layer.name
			layertype = layer.type
			jsl = {
				"centerx" : 0.0,
				"centery" : 0.0,
				"layercontext" : layercontext,
				"layername" : layername,
				"layertype" : layertype,
				"outname" : layername,
				"outtype" : layertype,
				"formatString" : "",
				"scalex" : 1.0,
				"scaley" : 1.0,
				"offsetx" : 0.0,
				"offsety" : 0.0,
				"angle" : 90,
				"mirr" : 0
			}
			jslayers.append(jsl)

		params["layers"] = jslayers

		ret = self.call_script("script_export_gerber", params)
		return ret

