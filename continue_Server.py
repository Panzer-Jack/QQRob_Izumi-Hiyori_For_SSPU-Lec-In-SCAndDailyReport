import json
import random
import requests
import socket
import time

import Lec_second_class
import AuthorityDB_mysql
import SSPU_AutoCheck
import report_Server
# import GPIO_test
from API import *

null = None
true = True

# x = {"post_type": "message", "message_type": "group", "time": 1664504632, "self_id": 2506205190, "sub_type": "normal",
#      "anonymous": null, "message": "[CQ:at,qq=2506205190] //cmd: 查询指令-\u003e健康打卡",
#      "raw_message": "[CQ:at,qq=2506205190] //cmd: 查询指令-\u003e健康打卡",
#      "sender": {"age": 0, "area": "", "card": "", "level": "", "nickname": "Panzer_Jack", "role": "owner",
#                 "sex": "unknown", "title": "", "user_id": 1229328963}, "font": 0, "group_id": 553111215,
#      "message_seq": 6043, "user_id": 1229328963, "message_id": -2122639396}
#
# y = {'post_type': 'message', 'message_type': 'private', 'time': 1664893217, 'self_id': 2506205190, 'sub_type': 'friend',
#      'raw_message': '��˹��', 'font': 0,
#      'sender': {'age': 0, 'nickname': 'Panzer_Jack', 'sex': 'unknown', 'user_id': 1229328963},
#      'message_id': -1166300024, 'user_id': 1229328963, 'target_id': 2506205190, 'message': '��˹��'}

SSPU_AccountData_Holiday = SSPU_AutoCheck.SSPU_AccountData_Holiday
SSPU_AccountData_SchoolDay = SSPU_AutoCheck.SSPU_AccountData_SchoolDay

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)

HttpResponseHeader_OK = '''HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n\r\n
'''

HttpResponseHeader_Continue = '''HTTP/1.1 100 Continue\r\n
Content-Type: text/html\r\n\r\n
'''

command = ["健康打卡_查询指令", "健康打卡_手动打卡", "开启R18模式", "涩图", "添加使用权限", "HOMO图", "劝学"]
X1_canteen = ["蜂蜜鸡排饭", "牛肉刀削面", "色拉鸡排饭", "牛杂刀削面", "熟菜区：一荤一素一白米饭", "汉堡套餐", "林檎"]
X2_canteen = ["饺子", "熟菜区：一荤一素一白米饭", "铁板饭"]


class Rep_Funtion:
    def __init__(self):
        self.is_R18 = 0
        self.QQ_num = self.QQ_numType = []
        self.msg_type = None
        pass

    def report_cmd(self, num):
        self.send_msg("CMD执行指令：健康打卡_查询指令", num)
        time.sleep(0.5)
        self.send_msg("请输入查询账号", num)

        try:
            req2 = self.recv_msg()
            recv = req2[req2.find('"post_type') - 1:]
            recv = json.loads(recv)
            if self.permission(recv):
                cmd_recv = recv["raw_message"][recv["raw_message"].find("CQ:at,qq=2506205190") + 21:]
                flag = pwd = SCNdata = 0
                for ACdata in SSPU_AccountData_SchoolDay:
                    if ACdata["账号"] == cmd_recv:
                        flag = 1
                        psd = ACdata["密码"]
                        SCNdata = SSPU_AccountData_SchoolDay.index(ACdata)
                if flag == 1:
                    self.send_msg(f"正在查询账号：{cmd_recv}, 请稍后。。。", num)
                    sspuReport = report_Server.SchoolAutoCheckOK(SSPU_AccountData=SSPU_AccountData_SchoolDay[SCNdata],
                                                                 first=0)
                    sspuReport.start_programme()
                else:
                    self.send_msg(f"未查询到账号：{cmd_recv}, 请联系管理员检查服务器 打卡账号池", num)
        except:
            pass

        pass

    def art_check(self, num):
        # self.send_msg("功能还在开发中。。(小声) 主人在摆烂")
        self.send_msg("CMD执行指令：健康打卡_手动打卡", num)
        time.sleep(0.5)
        self.send_msg("请输入打卡账号", num)

        try:
            req2 = self.recv_msg()
            recv = req2[req2.find('"post_type') - 1:]
            recv = json.loads(recv)
            if self.permission(recv):
                cmd_recv = recv["raw_message"][recv["raw_message"].find("CQ:at,qq=2506205190") + 21:]
                flag = pwd = SCNdata = 0
                for ACdata in SSPU_AccountData_SchoolDay:
                    if ACdata["账号"] == cmd_recv:
                        flag = 1
                        psd = ACdata["密码"]
                        SCNdata = SSPU_AccountData_SchoolDay.index(ACdata)
                if flag == 1:
                    self.send_msg(f"正在查询账号：{cmd_recv}, 请稍后。。。", num)
                    sspuReport = SSPU_AutoCheck.SchoolAutoCheckIn(
                        SSPU_AccountData=SSPU_AccountData_SchoolDay[SCNdata])
                    sspuReport.start_programme()
                    self.send_msg(f"账号：{cmd_recv}, 已完成打卡（可通过查询指令确认）", num)
                else:
                    self.send_msg(f"未查询到账号：{cmd_recv}, 请联系管理员检查服务器 打卡账号池", num)
        except:
            pass

    def r18_open(self, num):
        self.send_msg("CMD执行指令：开启R18？", num)
        time.sleep(0.5)
        self.send_msg("请输入管理员密码：", num)
        try:
            req2 = self.recv_msg()
            recv = req2[req2.find('"post_type') - 1:]
            recv = json.loads(recv)
            if self.permission(recv):
                cmd_recv = recv["raw_message"][recv["raw_message"].find("CQ:at,qq=2506205190") + 21:]
                if cmd_recv == "欧尼酱！dasuki！！！":
                    self.is_R18 = 1
                    self.send_msg("R18模式开启了哦。。欧尼酱注意节制哦", num)
        except:
            pass

    def picSearch(self, num):
        if self.is_R18:
            tar_url = web_RanImg_R18_url
        else:
            self.send_msg("不能涩涩，瑟瑟就要挨打", num)
            tar_url = Web_RanImg_url
        tar_res = requests.get(tar_url)
        print(tar_res.json()["url"])
        self.send_msg(f'[CQ:image,file={tar_res.json()["url"]},type=flash,id=40004]', num)

    def homoSearch(self, num):
        tar_res = homoImg[random.randint(0, len(homoImg))]
        # tar_res = homoImg[0]
        self.send_msg(f'[CQ:image,file={tar_res},id=40004]', num)

    def learnSearch(self, num):
        tar_res = learnImg[random.randint(0, len(learnImg))]
        self.send_msg(f'[CQ:image,file={tar_res},id=40004]', num)

    def Lec_S_C(self, num):
        Lec_SC = Lec_second_class.Lec_S_C()
        LSC_list = Lec_SC.start_programme()
        if len(LSC_list):
            for i in range(0, len(LSC_list)):
                print(LSC_list)
                self.send_msg(f'{LSC_list[i]["标题"]}\n{LSC_list[i]["时间"]}\n{LSC_list[i]["地点"]}', num)
        else:
            self.send_msg(f'目前没有正在进行 的 第二课堂讲座', num)

    def talk(self, recv, num):
        if "摆烂" in recv["raw_message"]:
            if "?" in recv["raw_message"] or "？" in recv["raw_message"]:
                self.send_msg("当然，妃爱酱要去和欧尼酱一起打galgame！", num)
            else:
                self.send_msg("摆烂是人的梦想, HOMO是人的本质", num)
        elif "关闭R18" in recv["raw_message"]:
            self.is_R18 = 0
            self.send_msg("R18模式关闭", num)
        elif "开灯" in recv["raw_message"]:
            GPIO_test.openLight()
            self.send_msg("妃爱给你开灯咯！", num)
        elif "关灯" in recv["raw_message"]:
            GPIO_test.closeLight()
            self.send_msg("妃爱帮你把灯关拉!", num)
        elif "好累" in recv["raw_message"]:
            self.send_msg("欧尼,别写代码了，来陪妃爱酱一起玩galgame吧！", num)
        elif "晚上" in recv["raw_message"] or  "很晚了" in recv["raw_message"]:
            self.send_msg("欧尼，很晚了哦，要早点休息！", num)
        elif "女朋友" in recv["raw_message"]:
            self.send_msg("欧尼酱(乖巧)，如果你去勾搭别的小姐姐，我就掐死你哦~", num)
        elif "骂我" in recv["raw_message"]:
            self.send_msg("欧尼酱~ 笨蛋~！", num)
        elif "第二课堂" in recv["raw_message"] or  "讲座" in recv["raw_message"]:
            self.send_msg("roger ! Hiyori is trying to get the information now....", num)
            self.Lec_S_C(num)
        elif "食堂" in recv["raw_message"] or "吃什么" in recv["raw_message"]:
            self.send_msg("嗯嗯, 欧尼，想吃什么呢？妹妹? 一抹多? 还是说。。。wataxi ? ヾ(≧O≦)〃", num)
            try:
                req = self.recv_msg()
                recv = req[req.find('"post_type') - 1:]
                recv = json.loads(recv)

                if self.permission(recv):
                    if "西一" in recv["raw_message"]:
                        self.send_msg(f"emm, 那就吃{X1_canteen[random.randint(0, len(X1_canteen))]}", num)
                    elif "西二" in recv["raw_message"]:
                        self.send_msg(f"emm, 那就吃{X2_canteen[random.randint(0, len(X2_canteen))]}", num)
                    # elif "东一" in recv["raw_message"]:
                    #     pass
                    # elif "东二" in recv["raw_message"]:
                    #     pass
                    # elif "东三" in recv["raw_message"]:
                    #     pass
                    elif "妹妹" in recv["raw_message"] or "你" in recv["raw_message"] or \
                            "一抹多" in recv["raw_message"] or "wataxi" in recv["raw_message"] or "妃爱" in recv[
                        "raw_message"]:
                        self.send_msg("。。。。。噗~(笑)", num)
                    elif "(笑)" in recv["raw_message"]:
                        self.send_msg("哎，我刚才好像听见了非常轻蔑的笑声？被当成傻瓜了吗，我是被当成傻瓜了吗!?", num)
                    else:
                        self.send_msg("妃爱妃爱，还没去过你说的那家店哦", num)
                        pass
            except:
                pass
        else:
            self.send_msg("?", num)

    def SQL_rootAdd(self, num):
        self.send_msg("CMD执行指令：正在添加可使用妃爱酱权限的账号或QQ群,以及账号类型", num)
        self.send_msg("例(QQ群)：QQ群+114514 / 个人QQ+1919810", num)
        time.sleep(0.5)
        self.send_msg("请输入QQ账号或群号：", num)
        try:
            req2 = self.recv_msg()
            recv = req2[req2.find('"post_type') - 1:]
            recv = json.loads(recv)
            if self.permission(recv):
                cmd_recv = recv["raw_message"][recv["raw_message"].find("CQ:at,qq=2506205190") + 21:]

                if "QQ群" in cmd_recv:
                    QQ_num_T = cmd_recv[cmd_recv.find("+")+1:]
                    self.send_msg(f"添加权限给{QQ_num_T}", num)
                    AuthorityDB_mysql.mysql_QQ_rootAdd(QQ_num_T, 'group')
                    self.send_msg("功能还在开发中。。(小声) 主人在摆烂", num)
                elif "个人QQ" in cmd_recv:
                    QQ_num_T = cmd_recv[cmd_recv.find("+")+1:]
                    print(QQ_num_T)
                    self.send_msg(f"添加权限给{QQ_num_T}", num)
                    AuthorityDB_mysql.mysql_QQ_rootAdd(QQ_num_T, 'private')
                    self.send_msg("功能还在开发中。。(小声) 主人在摆烂", num)
                else:
                    self.send_msg(f"格式不对, 请重新输入", num)
        except:
            pass

    def find_command(self):

        try:
            req = self.recv_msg()
            recv = req[req.find('"post_type') - 1:]
            recv = json.loads(recv)

            if self.permission(recv):
                num = self.permission(recv)
                print(num)
                if "cmd-" in recv["raw_message"]:
                    cmd_recv = recv["raw_message"][recv["raw_message"].find("cmd-") + 4:]
                    if cmd_recv == command[0]:
                        self.report_cmd(num)
                    elif cmd_recv == command[1]:
                        self.art_check(num)
                    elif cmd_recv == command[2]:
                        self.r18_open(num)
                    elif cmd_recv == command[3]:
                        self.picSearch(num)
                    elif cmd_recv == command[4]:
                        self.SQL_rootAdd(num)
                    elif cmd_recv == command[5]:
                        self.homoSearch(num)
                    elif cmd_recv == command[6]:
                        self.learnSearch(num)
                    else:
                        self.send_msg("无效指令, 请去群公告查询指令集", num)
                else:
                    self.talk(recv, num)
        except:
            pass

            # print(req)
            # print(recv["user_id"])

    def permission(self, recv):
        self.SQL_rootFind()
        if recv["post_type"] == "message":
            if recv["message_type"] == "group":
                if recv["group_id"] in self.QQ_num:
                    if "CQ:at,qq=2506205190" in recv["raw_message"]:
                        return recv["group_id"]
            elif recv["message_type"] == "private":
                if recv["user_id"] in self.QQ_num:
                        return recv["user_id"]

    def SQL_rootFind(self):
        SQL_root = AuthorityDB_mysql.mysql_QQ_rootFind()
        self.QQ_num = []
        self.QQ_numType = []
        for i in range(0, len(SQL_root)):
            self.QQ_num.append(SQL_root[i][0])
            self.QQ_numType.append(SQL_root[i][1])
        # print(self.QQ_numType)

    def recv_msg(self):
        self.Client, self.Address = ListenSocket.accept()
        Request = self.Client.recv(1024).decode(encoding='utf-8')
        self.Client.sendall((HttpResponseHeader_OK).encode(encoding='utf-8'))
        self.Client.close()
        return Request

    def send_msg(self, msg, number):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload = None
        self.SQL_rootFind()

        ip = '127.0.0.1'
        client.connect((ip, 5700))
        msg_type = self.QQ_numType[self.QQ_num.index(number)]

        # 将字符中的特殊字符进行url编码
        msg = msg.replace(" ", "%20")
        msg = msg.replace("\n", "%0a")

        if msg_type == 'group':
            payload = "GET /send_group_msg?group_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
        elif msg_type == 'private':
            payload = "GET /send_private_msg?user_id=" + str(
                number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"

        print("发送" + payload)
        client.send(payload.encode("utf-8"))
        client.close()


if __name__ == '__main__':
    Rep_Server = Rep_Funtion()
    while 1:
        Rep_Server.find_command()
