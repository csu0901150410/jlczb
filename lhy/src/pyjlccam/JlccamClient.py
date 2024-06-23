#coding=utf-8

import os
import time

from .client import socket_client
from .JlccamJob import JlccamJobInfo


class JlccamClient:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.client = socket_client(ip, port)

	# 获取所有打开的料号信息
	def get_all_open_jobinfo(self):
		ret = self.client.send_command("request_edits")
		result = ret["result"]

		jobinfo = []
		for dict in result:
			info = JlccamJobInfo(dict["name"], dict["pid"], dict["port"])
			jobinfo.append(info)
		
		return jobinfo
	
	# 通过进程id获取料号信息
	def get_jobinfo_by_pid(self, pid):
		param = {}
		param["pid"] = pid
		ret = self.client.send_command("get_edit_descript", param)
		result = ret["result"]
		info = JlccamJobInfo(result["name"], result["pid"], result["port"])

		return info
	
	# 根据料号名称新建料号
	def new_job(self, jobname):
		ret = self.client.send_command("script_new_job", jobname)
		success = ret["success"]

		return success
	
	# 通过料号名称打开料号
	def open_job(self, jobname, show = True):
		param = {}
		param["show"] = show
		param["job"] = jobname
		ret = self.client.send_command("script_open_job", param)
		success = ret["success"]

		return success
	
	# 获取料号文件目录(ddw工程所在文件目录)
	def get_work_directory(self):
		ret = self.client.send_command("script_get_work_directory")
		dir = ret["result"]
		dir = os.path.normpath(dir) # 路径标准化，去除对父级目录的引用

		return dir
	
	# 获取临时文件目录(嘉立创CAM临时缓存目录)
	def get_temp_directory(self):
		ret = self.client.send_command("script_get_tmp_directory")
		dir = ret["result"]
		dir = os.path.normpath(dir) # 路径标准化，去除对父级目录的引用

		return dir
	
	# 根据jobname获取料号信息，注意只能在料号打开命令之后执行，否则会一直获取不到
	def get_jobinfo_by_jobname(self, jobname):
		target = JlccamJobInfo("", 0, 0)
		while target.port == 0:
			time.sleep(1)
			jobinfo = self.get_all_open_jobinfo()
			for info in jobinfo:
				if jobname == info.jobname:
					target = info
		
		return target
	

	# 检查料号是否已经存在于料号目录中
	def check_job_exists(self, jobname):
		filename = jobname + ".ddw"
		work_dir = self.get_work_directory()
		for root, dirs, files in os.walk(work_dir):
			if filename in files:
				return True
		return False

	
	def close(self):
		self.client.send_command("script_quit_app")
		self.client.stop()
