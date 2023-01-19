import yaml
import os

raw_number=5
my_clash_config="/data/data/com.termux/files/home/.config/clash_config/"
start_clash="clash"
clash_yaml="/data/data/com.termux/files/home/.config/clash/config.yaml"

def list_print(raw_list):
    for element in range(len(raw_list)):
        print(str(element)+'. '+str(raw_list[element]),end='  │  ') if (element+1)%raw_number!=0 else print(str(element)+'. '+str(raw_list[element])+'  │\n')
    print("\n")
    
def install():
    print("正在安装/更新...")
    os.system("pkg update -y && pkg upgrade -y && pkg install clash -y && pkg install wget -y")

def list_config():
    configs=os.listdir(my_clash_config)
    configs.remove(".data")
    list_print(configs) if os.path.exists(my_clash_config) else print("没有找到配置!")

def add_config(url,name):
    os.system("wget '%s' -O '%s%s'"%(url,my_clash_config,name))

def change_config(name):
    os.system("cp '%s%s' '%s'"%(my_clash_config,name,clash_yaml))
    with open(my_clash_config+".data","w")as file:
        file.write(name)

def read_config(name):
    with open(my_clash_config+name,"r")as file:
        temp_data=yaml.load(file,Loader=yaml.FullLoader)
        allow_lan="是" if temp_data["allow-lan"]==True else "否"
        try:
            ipv6="是" if temp_data["ipv6"] ==True else "否"
        except:
            ipv6="否"
        data={"名称":name,"外部控制器端口":temp_data["external-controller"],"socks端口":temp_data["socks-port"],"允许局域网":allow_lan,"允许IPV6":ipv6,"模式":temp_data["mode"],"节点数":len(temp_data["proxies"])}
        return data
        
def menu():
    list_print(["安装或更新","列出配置","切换配置","添加配置","删除配置","当前配置","启动"])
    mode=input("请输入要使用的功能:")
    os.system("clear")
    if mode=="0":
        install()
    elif mode=="1":
        list_config()
    elif mode=="2":
        config=os.listdir(my_clash_config)
        config.remove(".data")
        config.sort()
        list_print(config)
        name=config[int(input("请输入配置前的序号以切换:"))]
        change_config(name)
    elif mode=="3":
        print("目前已有的配置:")
        list_config() if os.path.exists(my_clash_config) else os.system("mkdir %s"%my_clash_config)
        add_config(input("请输入配置地址:"),input("请输入配置名:"))
    elif mode=="4":
        config=os.listdir(my_clash_config)
        config.remove(".data")
        config.sort()
        list_print(config)
        for rm_ready in input("请输入要删除的配置前的序号(多个序号间用空格分开):").split(" "):
            os.system("rm %s%s"%(my_clash_config,config[int(rm_ready)]))
    elif mode=="5":
        try:
            with open(my_clash_config+".data","r")as file:
                data=read_config(file.read())
            for element in data.keys():
                print(element+": %s"%data[element])
        except:
            print("配置文件不存在!")                
    elif mode=="6":
        os.system(start_clash) if os.path.exists(clash_yaml) else print("似乎还没有选择一个配置...")

menu()
