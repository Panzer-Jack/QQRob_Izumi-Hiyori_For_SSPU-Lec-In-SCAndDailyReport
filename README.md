 
<p align="center">
    <img src="https://pic1.imgdb.cn/item/634541a516f2c2beb15a911c.jpg" width="200" height="200" alt="go-cqhttp">
</p>

<div align="center">
    
# 和泉妃爱QQ小助手 
    
_✨ 基于 [go-cqhttp](https://github.com/mamoe/mirai) 以及 [Python]() 与 [MysQL]()  实现 ✨_  
    
Hiyori, a cute QQ Robot is used for SSPU Auto deportReport, developped by Python ( Based on go-cqhttp    
    
</div>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.7+-blue" alt="license">
    <img src="https://img.shields.io/badge/MySQL-MariaDB-green" alt="license">
</p>


## 功能
- 上海第二工业大学 每日一报 自动打卡 （ 会自动汇报账号池内的用户, 并提供 在QQ内 每日定时自动汇报结果功能
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
>(二) 妃爱酱特性
>>1. 和欧尼酱一样喜欢摆烂
>>2. 有时候会去学校食堂里头吃些好吃的, 所以知道些好吃的菜
>>3. 有点 homo 和 小坏


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
go-cqhtt下载: https://docs.go-cqhttp.org/  
如果你想扩展功能，或者自定义更多的新花样的话 可以具体用法参照文档：[go-cqhtt官方文档](https://docs.go-cqhttp.org/api)  

4. chromedriver:   
首先，你需要确认你的谷歌游览器版本-以及系统：
> ![](https://pic1.imgdb.cn/item/6345328516f2c2beb142af84.png)   
然后去 [chromedriver国内镜像](https://registry.npmmirror.com/binary.html?path=chromedriver/) 下载适合你系统 和 谷歌版本的 谷歌驱动


<mark><strong><big><font face="courier New" color=#1E90FF>好！正式进入使用介绍：<big></font><strong></mark>

## 使用教程：
1. 在`SSPU_AutoCheck.py`内配置 校园账号-用户池 写入所有你想要自动打卡的用户信息（会自动汇报完账号池内所有的账号）
```python3
# 二工大 用户池 ---------------> 字面意思 那个 假期 / 在校 （其实都无所谓的）
SSPU_AccountData_Holiday = [
    {"账号": "20211145140", "密码": "hengheng@1145141919810",
     "地址": ["上海", "上海市", "浦东新区", "金海路2360号上海第二工业大学"]}]

SSPU_AccountData_SchoolDay = [
    {"账号": "20211145140", "密码": "hengheng@1145141919810",
     "地址": ["上海", "上海市", "浦东新区", "金海路2360号上海第二工业大学"]}]
```           

2. 在`report_Server.py`里头 指定QQ内 每日汇报的QQ群:
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

5. 设置定时汇报
    如果你是Linux 或者 MacOS系统的话, 推荐使用`crontab`:
    在你的Linux终端：
    ```Linux
    crontab -e
    ```
    进入 crontab 定时管理  设定一个log 重定向你的脚本到这个log上用于接收执行日志
    ```Linux
    2 1-10/1 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    30 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    30 4 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    */10 5 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    */10 6 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    */10 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/SSPU_AutoCheck.py >> ~/dailyReport.log
    0 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/report_Server.py
    15 7 * * * /usr/bin/python3 /home/pi/Python_Crawler/report_Server.py
    ```
    Q: 你问为什么 要设置那么多脚本执行？        
    A: 因为我用是树莓派啊。。。所以脚本执行有时候会卡死，为了安全起见当然多设几个 （ 反正学校又没有反爬



