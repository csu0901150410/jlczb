from gerbonara import GerberFile
from gerbonara.graphic_objects import *
from gerbonara.apertures import *
from gerbonara.utils import *

from pyjlccam import *

import argparse

# 打印gerber中的图元
flashs = []
lines = []
arcs = []
regions = []

def read_gerber(filename):
	# 读取单个gerber
	gerber_file = GerberFile.open(filename)
	print(gerber_file)

	for obj in gerber_file.objects:
		if isinstance(obj, Flash):
			flashs.append(obj)
		elif isinstance(obj, Line):
			lines.append(obj)
		elif isinstance(obj, Arc):
			arcs.append(obj)
		elif isinstance(obj, Region):
			regions.append(obj)

# 打开jlccam写数据
def main(jlccam):
	jobname = "1234"

	if jlccam.check_job_exists(jobname):
		jlccam.open_job(jobname)
	else:
		jlccam.new_job(jobname)
		jlccam.open_job(jobname)

	# 创建料号客户端
	jobinfo = jlccam.get_jobinfo_by_jobname(jobname)
	job = JlccamJob("127.0.0.1", jobinfo.port)

	# 添加step
	stepname = "orig"
	ret = job.add_step(stepname)
	print(ret)

	# 添加层
	layername = "tl"
	ret = job.add_layer(layername, LayerType.SIGNAL, True, Polarity.POSITIVE)
	print(ret)

	# 加pad
	job.set_only_work_layer(stepname, layername)

	for flash in flashs:
		# 光圈
		aperture = flash.aperture

		# 单位
		object_unit = flash.unit
		aperture_unit = aperture.unit

		# 位置
		x = object_unit.convert_to("mm", flash.x)
		y = object_unit.convert_to("mm", flash.y)

		# 根据光圈类型处理
		if isinstance(aperture, RectangleAperture):
			w = aperture_unit.convert_to("mm", aperture.w)
			h = aperture_unit.convert_to("mm", aperture.h)

			# 转成um
			w = w * 1000
			h = h * 1000

			symbol = f'rect{round(w)}x{round(h)}'
			job.add_pad(symbol, x, y)
			pass
		elif isinstance(aperture, CircleAperture):
			pass
		elif isinstance(aperture, ObroundAperture):
			pass
		elif isinstance(aperture, PolygonAperture):
			pass

if __name__ == "__main__":

	# parser = argparse.ArgumentParser(description="Script read gerber file")

	# parser.add_argument("-i", "--input", help="input gerber file", default="")

	# args = parser.parse_args()

	# filename = args.input

	ddw_path = "../res/7237039A_Y22/ok/7237039a_y7.ddw"

	if len(ddw_path) != 0:
		jlccam = JlccamClient("127.0.0.1", 4066)

		jobname = "7237039a_y7"
		if jlccam.check_job_exists(jobname):
			jlccam.open_job(jobname)
		else:
			jlccam.new_job(jobname)
			jlccam.open_job(jobname)

		# 创建料号客户端
		jobinfo = jlccam.get_jobinfo_by_jobname(jobname)
		job = JlccamJob("127.0.0.1", jobinfo.port)
		job.import_ddw(ddw_path)

		ret = job.save()
		print(ret)

		path = os.path.dirname(ddw_path)
		steps = job.get_steps()
		layers = job.get_layers()

		for step in steps:
			step_path = os.path.join(path, step)
			print(step)
			ret = job.autosort_layer(step)
			print(ret)

			ret = job.export_gerber(step_path, step, layers)
			print(ret)
