 
<p align="center">
    <img src="https://pic.imgdb.cn/item/6376ffa816f2c2beb1e995d8.png" alt="go-cqhttp">
</p>

<div align="center">
    
# 和泉妃爱QQ校园小助手 
    
_✨ 基于 [go-cqhttp]() 以及 [Python]() + [MysQL]()  实现 ✨_  
    
Hiyori, a cute QQ Robot is used for SSPU Auto deportReport and the lecture infomation from the second class , developped by Python + MySQL( Based on go-cqhttp
    
</div>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.7+-blue" alt="license">
    <img src="https://img.shields.io/badge/MySQL-MariaDB-green" alt="license">
</p>


## 功能
- 上海第二工业大学 每日一报 自动打卡 （ 会自动汇报账号池内的用户, 并提供 在QQ内 每日定时自动汇报结果功能
- 上海第二工业大学 第二课堂讲座最新信息的 即时性监听 （ 只要有新讲座就会@你/全体成员 同时你也可以主动问她有多少个正在进行的讲座
- 日常看setu / HOMO图
- 食堂随机饭菜推荐
- 让你拥有一个随时可以和你互动的可爱伊抹多 陪你一起度过四年孤寡的校园生活
- 一个妃爱酱监管的小物联网系统 （如果你的HTTP服务器是搭建在树莓派或一些支持Python 环境的 嵌入式开发板上的话的话）

## 和泉·妃爱酱 的 指令-文档
注：1. 命令是指 双引号内部那些，双引号不要加
2. 所有指令必须@和泉·妃爱酱 才能识别
>(一) 专有命令
语法： “cmd- "+ "指令"
>命令指令集：
>>1. “健康打卡_查询指令”
>>2. “健康打卡_手动打卡”
>>3. “开启R18模式”(密码可以自行设置)
>>4. “涩图”
>>5. “HOMO图”
>>6. “劝学”
>>7. “添加权限用户”(关闭)
>
>(二) 妃爱酱特性  (暗示：你可以问她)
>>1. 和欧尼酱一样喜欢摆烂
>>2. 有时候会去学校食堂里头吃些好吃的, 所以知道些好吃的菜
>>3. 知道 所有 正在进行的 第二课堂讲座 的 消息 （快问她！
>>4. 并且 只要有 新出来的 第二课堂讲座 她就会@全体
>>5. 鉴于学校政策，每日一报凌晨自动打卡功能临时关闭了（ 虽然感觉马上又会要用到
>>6. 有点 homo 和 小坏


### 使用前所需的运行环境：
>1. 你需要一个Python的开发环境 以及 MySQL云/本地数据库服务器
>2. requirements 内的必要运行库
>3. go-cqhttp: 用来监听QQ的HTTP服务器 (如果你想扩展更多功能的话，可以参照它的官方文档)
>4. 符合你自己谷歌游览器的驱动版本 --> chromedriver ( 这里已经提供了一个适合Window系统的 谷歌游览器driver )

##### 还是不懂运行环境的安装？ ----> 没关系 这里给你详细说明：
1. Python安装 和MySQL数据库搭建 ---> 不解释了
2. requirements内运行库安装：
打开你的cmd / Linux终端：
```
pip3 install -r requirements.txt
```

3. go-cqhttp:     
这里简要介绍一下 该项目是使用Python的 套接字/Requests 实现监听 `127.0.0.1:5701` 端口 来控制QQ机器人
```
# 基于go-cqhttp 的 Socket 通信
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)
```
go-cqhtt下载: https://docs.go-cqhttp.org/  
如果你想扩展`妃爱酱`的功能，或者自定义更多的新花样的话 或者建立一个属于你自己的QQ机器人的话 可以具体用法参照文档：[go-cqhtt官方文档](https://docs.go-cqhttp.org/api)  

4. chromedriver:   
首先，你需要确认你的谷歌游览器版本-以及系统：
> ![](https://pic1.imgdb.cn/item/6345328516f2c2beb142af84.png)   
然后去 [chromedriver国内镜像](https://registry.npmmirror.com/binary.html?path=chromedriver/) 下载适合你系统 和 谷歌版本的 谷歌驱动


<mark><strong><big><font face="courier New" color=#1E90FF>好！正式进入使用介绍：<big></font><strong></mark>

## 使用教程：
1. 在`API.py`内配置 校园账号-用户池 写入所有你想要自动打卡的用户信息（会自动汇报完账号池内所有的账号）
```python3
# 二工大 用户池 ---------------> 字面意思 那个 假期 / 在校 （其实都无所谓的）
SSPU_AccountData_Holiday = [
    {"账号": "20211145140", "密码": "hengheng@1145141919810",
     "地址": ["上海", "上海市", "浦东新区", "金海路2360号上海第二工业大学"]}]

SSPU_AccountData_SchoolDay = [
    {"账号": "20211145140", "密码": "hengheng@1145141919810",
     "地址": ["上海", "上海市", "浦东新区", "金海路2360号上海第二工业大学"]}]
```           

2. 同样, 在`API.py`里头 指定QQ内 每日汇报的QQ群:
```python3
QQ_Group = xxxxxxx
```    

3. 在本地/服务器搭建好 MySQL数据库环境 ----> 这里存储了 能够使用`妃爱酱`的使用权限 的 用户/群  
这里使用的是MySQL语言，创建数据库结构：
```mysql
create table QQ_Num (number BIGINT, msg_type VARCHAR(20));
```
然后 在 你的MySQL相关数据库的表内加入 你想要的QQ用户   
### 参数说明：
`number`: QQ群号/个人QQ号  
`msg_type`: `private` ( 个人QQ )/ `group` ( QQ群 )          

然后在`AuthorityDB_mysql.py`内 配置你的数据库接口：
```python
# 你的数据库和表名
db = ""
db_table = ""
```
· 注：这里默认是使用本地数据库接口，若你使用的是云服务器的话可以自行配置 Host 成你的云数据库服务器的IP
    
4. 这时候 可以开启go-cqhttp服务器了。     
    配置好go-cqhttp设置, 然后去你的终端
    ```
    go-cqhttp
    ```

5. 设置凌晨自动打卡 + 每日早自动汇报签到结果
    如果你是Linux 或者 MacOS系统的话, 推荐使用`crontab`:
    在你的Linux终端：
    ```Linux
    crontab -e
    ```
    设置你的 crontab 任务：`SSPU_AutoCheck.py` 和 `report_Server.py` 和 `Lec_second_class.py`
    （crontab 语法）
    ```
    每五分钟执行   */5 * * * *
    每小时执行     0 * * * *
    每天执行       0 0 * * *
    每周执行       0 0 * * 0
    每月执行       0 0 1 * *
    每年执行       0 0 1 1 *
    ```
 
    如果你不想自己设置的话，也可以用下面的：    
 
    进入 crontab 定时管理  设定一个log 重定向你的脚本到这个log上用于接收执行日志 (注：鉴于学校政策，每日一报凌晨自动打卡功能临时关闭了（ 虽然感觉马上又会要用到)
    ```Linux
    #2 1-10/1 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    #30 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    #30 4 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    #*/10 5 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    #*/10 6 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    #*/10 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    #0 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/report_Server.py
    #15 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/report_Server.py
    * */2 * * * /usr/bin/python3 /home/pi/Python_Crawler/Lec_second_class.py
    ```
    Q: 你问为什么 要设置那么多脚本执行？        
    A: 因为我用是树莓派啊。。。所以脚本执行有时候会卡死，为了安全起见当然多设几个 （ 反正学校又没有反爬
 
 6. 开启go-cqhttp 服务器，打开终端执行界面 cd 到该项目文件夹：
 ```
 pyhon3 main.py
 ```

## 自定义你的功能
 1. 图片API `API.py`  你可以在这里定义属于你自己的 se (HO) tu (MO) 连接
 2. 如果你不是二工大的学生 但是也想用这个的话  你可以在 `SSPU_AutoCheck.py`  里编写 你的自动打卡程序
 3. 如果你想给妃爱酱自定义更多的 talk 的话 你可以在 `continue_Server.py` 里的 ``` def talk(self, recv, num): ``` 方法里加入 你想要的 感兴趣content
 4. `continue_Server.py` 也包含了现有的机器人的命令指令方法 你可以根据你自己的需求来增加或者修改，甚至可以完全自定义成属于你自己的QQ机器人
 5. 如果你觉得使用数据库来进行权限赋予 太麻烦， 你可以将 `self.QQ_num` 和 `self.QQ_numType` 直接改成你想要的 QQ和QQ类型，参数详见上方数据库建立的那两个
 6. 如果你是树莓派（或者其他嵌入式处理器）并且想通过QQ实现一些建议的物联网联动，你参考IO控制文件夹 和 已有的开灯关灯命令。


