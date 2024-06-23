#coding=utf-8

from enum import Enum

from .JlccamJob import *

'''
对料号STEP模块中的脚本进行封装
'''

class JlccamStep:
	def __init__(self, job : JlccamJob, stepname : str):
		self.job = job
		self.stepname = stepname
