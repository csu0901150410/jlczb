#coding=utf-8

import os

# 相对路径转绝对路径
def path_rel2abs(relative_path):
	absolute_path = os.path.abspath(relative_path)
	return absolute_path