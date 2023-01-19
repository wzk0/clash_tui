# Clash_TUI

> 一个基于clash的简陋的终端界面. 适用于Termux, 稍做修改可适用于所有Linux终端.

## 支持:

1. 添加订阅
2. 切换订阅
3. 删除订阅
4. 启动
5. 查看订阅信息
6. 还没做好的设置功能

## 使用:

使用`wget`下载`main.py`这个文件到Termux.

安装`pyyaml`模块: `pip install PyYAML`

启动: `python3 main.py`

流程和clash系的软件一样, 应当先添加配置, 再切换配置, 再启动.

## 其他

由于我对clash内核不清楚, 所以使用了另建一个配置文件夹的方式储存配置文件(其他clash系软件的思路大概也是这样?).

第五行的变量是储存配置文件的路径, 记得最后有/.

第六行是启动clash的方式, Linux终端用户可将其修改为./clash(core的文件名).

第七行是clash默认的配置文件路径, Linux用户需要修改.

## 开发

第一次编写时手头没有电脑, 只好用Termux, 眼睛非常难受. 所以这个项目未完待续.