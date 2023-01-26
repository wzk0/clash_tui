# Clash_TUI

> 一个基于clash内核的简陋的终端界面. 适用于Termux和所有Linux终端.

## 支持

0. 添加订阅;
1. 删除订阅;
2. 更新订阅;
3. 重命名订阅;
4. 查看订阅信息;
5. 订阅储存与导出;
6. 静默启动clash;
7. 杀死clash.

## 界面

主界面:

```
Clash v1.12.0 linux amd64 with go1.19.3 Fri Nov 25 12:43:25 UTC 2022
 └─ clash已启动, 进程号: 307495
 └─ 当前共有1个配置.

0. 添加配置 │ 1. 删除配置 │ 2. 更新配置 │ 3. 重命名配置 │ 4. 编辑配置 │

5. 当前配置 │ 6. 选择配置 │ 7. 启动 │ 8. 结束进程 │ 

请输入序号以进行操作:
```

启动界面:

```
此配置信息如下:
 └─ 名称: pm
 └─ 地址: https://sub.pmsub.me/clash.yaml
 └─ socks端口: 7891
 └─ 模式: Rule
 └─ 外部控制端口: 9090
 └─ 节点个数: 62
 └─ 允许局域网: 是
 └─ 允许IPV6: 否
nohup: 把输出追加到 'nohup.out'

clash已在后台启动, 进程号: 307495
终端代理: export https_proxy=http://127.0.0.1:7891
Telegram代理: https://t.me/socks?server=127.0.0.1&port=7891
```

## 用法

首先应当确保电脑上有`git`, `python3`, `wget`, 以及`pyyaml`模块:

```sh
apt install git python3 wget python3-pip -y
pip install PyYAML
```

随后Linux用户需[点此选择正确的clash版本](https://github.com/Dreamacro/clash/releases)并下载解压到本地.

> Termux用户可以直接输入`pkg install clash`安装clash.

之后clone此仓库:

```sh
git clone https://github.com/wzk0/clash_tui
cd clash_tui
```

编辑`clash.py`第十到二十三行的内容:

```sh
nano clash.py
```

> 无需担心, 文件内有相关注释解释.


保存`clash.py`后, 请运行`setup.py`:

```sh
python3 setup.py
```

此后每次运行只需:

```sh
python3 clash.py
```

进入程序后, 其使用思路与cfw和cfa一样, 先`添加配置`, 再`选择配置`, 最后`启动`.

## 其他

若要迁移数据, 只需在`self_config`文件夹(上面自定义的变量)找到`data.json`即可按照文件内容进行恢复.

配置文件储存路径为`$self_config/config`.

## 开发

有部分注释!