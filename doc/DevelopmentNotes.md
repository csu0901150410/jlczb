~~使用库[PyGerber](https://pypi.org/project/pygerber/)，参考[gerber层格式规格](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-03_en.pdf)。~~

20240623
- 1.使用库[gerbonara](https://pypi.org/project/gerbonara/)来解析gerber文件；
- 2.封装jlccam的python版本二次开发接口；
- 3.解析gerber文件提取到层中的图形位置和光圈之后，通过二次开发接口将图形添加到jlccam料号中，初步测试提取gerber中的pad写入jlccam料号成功；