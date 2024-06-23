from gerbonara import GerberFile
from gerbonara.graphic_objects import *
from gerbonara.apertures import *
from gerbonara.utils import *

from pyjlccam import *

gerber_files_path = "../../res/7237039A_Y22/yg"
filepath = "{0}/1 .GTL".format(gerber_files_path)

# 打印gerber中的图元
flashs = []
lines = []
arcs = []
regions = []

def inch_2_mm(value):
	return convert(value, Inch, MM)

def read_gerber():
	# 读取单个gerber
	gerber_file = GerberFile.open(filepath)
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

	read_gerber()

	jlccam = JlccamClient("127.0.0.1", 4066)
	main(jlccam)