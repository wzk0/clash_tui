from clash import self_config as config_path
from clash import start_clash as clash
import os

if os.path.exists("%sdata.json"%config_path):
	print('请运行clash.py')
else:
	print('正在检测clash...若输出版本号则正常:')
	os.system(clash+' -v')
	print('\n正在创建相关文件夹...')
	os.system('mkdir -p %sconfig'%config_path)
	print('\n正在创建数据文件...')
	os.system("echo '[]' > %sdata.json"%config_path)
	print('\n完成! 正在启动程序...\n')
	os.system('python3 clash.py')