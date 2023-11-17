# 通用脚本

[![](https://img.shields.io/badge/home-tools-orange)](https://github.com/angshn/tools.git)

适用于YSU的科研脚本
内容待完善和增加

## 目录

- [通用脚本](#通用脚本)
  - [目录](#目录)
  - [背景](#背景)
  - [安装](#安装)
  - [用法](#用法)
  - [相关项目](#相关项目)
  - [主要项目负责人](#主要项目负责人)
  - [参与贡献方式](#参与贡献方式)
    - [贡献人员](#贡献人员)
  - [开源协议](#开源协议)

## 背景
用于YSU的科研工作环境设置
## 安装

```shell
$ git clone https://github.com/angshn/tools.git

```

## yauth用法
**yauth**

### 配置文件

yauth可以使用配置文件来指定用户名和密码，可以在用户目录下新建`.config/yauth.conf`文件，或者直接修改项目目录下的'conf'文件，并添加或修改以下内容：

```conf

[USER]
username=20222204xxxx
password=password

[SERV]
# 默认下线所有设备
OFFLINE_ALL=True

```

### 参数

1. -l 登录；
2. -i 指定isp，默认是[3] 中国电信，你可以在yauth源码中修改对应的默认值，或者直接-i 0指定宽带服务商；

   [0] 校园网 
   [1] 中国移动 
   [2] 中国联通 
   [3] 中国电信
3. -q 退出当前设备的登录状态；
4. -d 可选择的退出已登录的设备，如果配置了`OFFLINE_ALL`则会静默退出所有设备。

### 
```shell
# login
$ python yauth -l
>input your password hear
Login successfully.

# 使用校园网提供的宽带服务
$ python yauth -l -i 0
>input your password hear
Login successfully.

# logout
$ python yauth -q
下线成功

# 查看登录信息
$ python yauth -t
Logged!
Current user is xx.
IP is 10.20.xx.xx.
ISP is 中国yy

#退出所有设备服务
$ python yauth -d 

```
在yauth同目录下的conf文件，输入以下内容
```
[USER]
username=202x22010101
password=yourpassward
```

## 相关项目

暂无

## 主要项目负责人

[@syang](https://github.com/angshn)
[@yangn0](https://github.com/yangn0)

## 参与贡献方式


提交 [PR](https://github.com/angshn/tools/pulls) 申请，我会视情况通过。

### 贡献人员

感谢所有贡献的人。

[@syang](https://github.com/angshn)
[@yangn0](https://github.com/yangn0)

## 开源协议

[MIT](LICENSE) © syang
