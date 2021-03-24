# IWF-project
IWF 是 I Wanna Fly 的简称，该项目旨在建立我要飞外卖代取平台的服务器原型
服务器的基本组成是一个内存数据库和一个提供服务的主程序
应该提供一个命令行接口以供直接对数据进行增删改查
应当提供命令行接口控制服务的运行与否
项目还提供一个简易的客户端脚本以供测试
理想状态下该项目仅依赖C标准库，运行在标准unix环境下
作者:吕赫 在MIT协议的规范下保留所有权力

## 0.1
测试用客户端设定的交互为：创建账户A，创建账户B，账户A创建订单，账户B获取订单，共四个过程
服务端需要完成的服务为，创建账户数据库，创建账户A，放入磁盘，创建账户B，放入磁盘，创建订单数据库，在内存中存储订单信息，接受A的订单，将订单分配给B，实时更新状态，完成后只保留订单记录而不保留订单本身。
创建账户和创建订单都采用TCP连接，传递JSON格式的文本，而获取订单分为两步，若仅获取订单则UDP传递简单列表，若成功接单则TCP连接下载JSON订单信息，更新订单状态采用的也是简单列表
原型采用Python完成
完成后将服务端替换为Cpp版本
一个账户信息包括学号\姓名\学生证照片\
一个订单信息包括学号\单号\内容\取地址\送地址\创建时间\取到时间
一个订单记录包括单号\学号\最终状态\记录时间
一个简单列表项包括单号\取地址\送地址\取到时间
一个状态更新信息包括单号\状态

## 0.2
测试用服务端将分为3个文件
第一个文件处理用户信息
第二个文件接受订单请求并应答
第三个文件为内存订单更新信息

## 0.3
不用json文件，用json格式的字符串


# IWF-projrct
# IWF-projrct