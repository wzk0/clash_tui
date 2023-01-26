import os
import json
import yaml
import sys
from getpass import getuser
import requests
import psutil
from time import sleep

clash_config='/home/%s/.config/clash/config.yaml'%getuser()
# Linux用户无需修改, Termux用户请填写: /data/data/com.termux/files/home/.config/clash/config.yaml

self_config='./我的配置/'
# 此为存放clash配置及用户数据的路径, 请在最后加/

start_clash='clash'
# 此为启动clash的指令, Linux用户请填写clash内核可执行文件的绝对路径

editor='micro'
# 编辑配置文件时使用的编辑器

raw_number=5
# 此为一行输出的信息长度, Termux用户可改为3

# 美观输出列表
def list_print(raw_list):
	for element in range(len(raw_list)):
		print(str(element)+'. '+str(raw_list[element]),end=' │ ') if (element+1)%raw_number!=0 else print(str(element)+'. '+str(raw_list[element])+' │\n')
	print("\n")

# 输出报错的同时退出程序
def error(reason):
	print('由于%s, 请自行修改后重启程序.'%reason)
	sys.exit()

# 地址类
class link:
	# 添加配置
	def add(url,name):
		if not url.startswith('http'):
			error('配置地址无效')
		print('正在获取...')
		os.system("wget -q '%s' -O '%sconfig/%s'"%(url,self_config,name))
		with open(self_config+'data.json','r')as file:
			old_data=json.loads(file.read())
			one_data={'name':name,'url':url}
			old_data.append(one_data)
		with open(self_config+'data.json','w')as file:
			file.write(json.dumps(old_data,ensure_ascii=False))
		config.info(name)
	# 通过配置名获取配置地址
	def get_url(data,name):
		for one_data in data:
			if one_data['name']==name:
				return one_data['url']
			else:
				pass

# 配置类
class config:
	# 更新配置
	def update(name_list):
		with open(self_config+'data.json','r')as file:
			data=json.loads(file.read())
		for name in name_list:
			url=link.get_url(data,name)
			print('正在更新配置%s...'%name)
			os.system("wget -q '%s' -O '%sconfig/%s'"%(url,self_config,name)) if requests.get(url).ok else print('配置%s出现错误, 已跳过.'%name)
	# 删除配置
	def delete(name_list):
		with open(self_config+'data.json','r')as file:
			old_data=json.loads(file.read())
		for name in name_list:
			os.system('rm %sconfig/%s'%(self_config,name))
			for data in old_data:
				if data['name']==name:
					old_data.remove(data)
		with open(self_config+'data.json','w')as file:
			file.write(json.dumps(old_data,ensure_ascii=False))
	# 重命名配置
	def rename(old_name,new_name):
		os.system('mv %s/config/%s %s/config/%s'%(self_config,old_name,self_config,new_name))
		with open(self_config+'data.json','r')as file:
			old_data=json.loads(file.read())
			for data in old_data:
				if data['name']==old_name:
					data['name']=new_name
		with open(self_config+'data.json','w')as file:
			file.write(json.dumps(old_data,ensure_ascii=False))
	# 配置信息
	def info(name):
		with open(self_config+'config/%s'%name,'r')as file:
			try:
				all_data=yaml.load(file,Loader=yaml.FullLoader)
			except:
				error('配置文件不符合yaml规则')
		try:
			ipv6='是' if all_data['ipv6'] else '否'
		except:
			ipv6='否'
		try:
			allow_lan='是' if all_data['allow-lan'] else '否'
		except:
			allow_lan='否'
		with open(self_config+'data.json','r')as file:
			for a_data in json.loads(file.read()):
				if a_data['name']==name:
					url=a_data['url']
		info={'名称':name,'地址':url,'socks端口':all_data['socks-port'],'模式':all_data['mode'],'外部控制端口':all_data['external-controller'],'节点个数':len(all_data['proxies']),'允许局域网':allow_lan,'允许IPV6':ipv6}
		os.system('clear')
		print('此配置信息如下:')
		for item in info.items():
			print(' └─ '+item[0]+': %s'%item[1])
		return info
	# 编辑配置
	def edit(name):
		os.system(editor+' %sconfig/%s'%(self_config,name))

# clash类
class clash:
	# 选择配置
	def choose(name):
		os.system('cp %s/config/%s %s'%(self_config,name,clash_config))
		with open('%s.now'%self_config,'w')as file:
			file.write(name)
		config.info(name)
	# 获取clash进程号
	def get_pid():
		for pid in psutil.process_iter():
			if pid.name()=='clash':
				return pid.pid
			else:
				pass
	# 杀死clash进程
	def kill():
		os.system('kill %s'%clash.get_pid())
	# 启动clash
	def start():
		try:
			with open(self_config+'.now','r')as file:
				name=file.read()
			info=config.info(name)
			os.system('nohup %s &'%start_clash)
			print('\nclash已在后台启动, 进程号: %s'%clash.get_pid())
			print('终端代理: export https_proxy=http://127.0.0.1:%s\nTelegram代理: https://t.me/socks?server=127.0.0.1&port=%s'%(info['socks端口'],info['socks端口']))
		except:
			error('未选择配置或配置格式无法读取')

# main函数
def main():
	if os.path.exists('nohup.out'):
		os.system('rm nohup.out')
	menu=['添加配置','删除配置','更新配置','重命名配置','编辑配置','当前配置','选择配置','启动','结束进程']
	config_dir=os.listdir(self_config+'config')
	os.system(start_clash+' -v')
	if clash.get_pid()!=None:
		print(' └─ clash已启动, 进程号: %s'%clash.get_pid())
	print(' └─ 当前共有%s个配置.\n'%len(config_dir))
	list_print(menu)
	mode=int(input('请输入序号以进行操作:'))
	os.system('clear')
	# 添加配置
	if mode==0:
		print('已有配置:')
		list_print(config_dir)
		url=input('请输入配置地址:')
		name=input('请为此配置命名:')
		link.add(url,name)
		clash.choose(name) if input('\n添加完成! 是/否(y/n)切换为此配置:')=='y' else print('若要使用此配置, 记得稍后手动切换!')
	# 删除配置
	elif mode==1:
		print('已有配置:')
		list_print(config_dir)
		remove_list=[]
		for a_id in input('请输入要删除的配置前的序号(多个序号用空格分开):').split(' '):
			remove_list.append(config_dir[int(a_id)])
		config.delete(remove_list)
		print('\n删除完成!')
	# 更新配置
	elif mode==2:
		print('已有配置:')
		list_print(config_dir)
		update_list=[]
		for a_id in input('请输入要更新的配置前的序号(多个序号用空格分开):').split(' '):
			update_list.append(config_dir[int(a_id)])
		config.update(update_list)
		print('\n更新完成!')
	# 重命名配置
	elif mode==3:
		print('已有配置:')
		list_print(config_dir)
		config.rename(config_dir[int(input('请输入要重命名的配置前的序号:'))],input('请输入新的名称:'))
		print('\n重命名完成!')
	# 编辑配置
	elif mode==4:
		print('已有配置:')
		list_print(config_dir)
		config.edit(config_dir[int(input('请输入要编辑的配置前的序号:'))])
	# 输出当前配置信息
	elif mode==5:
		try:
			with open(self_config+'.now','r')as file:
				name=file.read()
			config.info(name)
		except:
			error('未选择配置')
	# 选择配置
	elif mode==6:
		print('已有配置:')
		list_print(config_dir)
		clash.choose(config_dir[int(input('请输入要选择的配置前的序号:'))])
		print('\n切换成功!')
	# 启动clash
	elif mode==7:
		clash.start()
	# 杀死clash进程
	elif mode==8:
		clash.kill()
	else:
		pass

if __name__ == '__main__':
	try:
		main()
	except FileNotFoundError:
		print('似乎没有运行setup.py?')
	except KeyboardInterrupt:
		print('')
