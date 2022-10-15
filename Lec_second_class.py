from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import selenium.webdriver
from selenium.webdriver.common.by import By
import time
import pymysql
import socket
from API import *


class Lec_S_C:
    def __init__(self):
        # 全局参数
        self.i = 1
        self.LSC_list = []
        self.LSC_Lt_list = []
        self.today = datetime.today().strftime('%Y.%m.%d')

        # 反爬
        self.opt = Options()
        self.opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.opt.add_experimental_option('useAutomationExtension', False)
        self.opt.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
        self.opt.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/92.0.4515.159 Safari/537.36')
        self.opt.add_argument('--disable-blink-features=AutomationControlled')

        # 后台自动运行
        self.opt.add_argument('--headless')
        self.opt.add_argument('disbale-gpu')

        driver_path = '/usr/bin/chromedriver'
        self.driver = selenium.webdriver.Chrome(executable_path=driver_path, options=self.opt)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
        })

    def update_SQL(self, idV):
        cur = self.SSPU_DB.cursor()
        sql = f'update Les_S_C set id = {idV} where id = "{self.find_SQL()}"'
        cur.execute(sql)
        self.SSPU_DB.commit()

    def find_SQL(self):
        cur = self.SSPU_DB.cursor()
        sql = f'select id from Les_S_C'
        cur.execute(sql)
        res = cur.fetchall()
        return res[0][0]

    def run_SQL(self):
        self.driver.implicitly_wait(10)
        url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3ODUzODczOA==&action=getalbum&album_id" \
              "=2611138528407896068&scene=173&from_msgid=2247489371&from_itemidx=1&count=3&nolastread=1" \
              "#wechat_redirect "
        self.driver.get(url)
        time.sleep(2)
        self.SSPU_DB = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456123',
            database='SSPU_AutoCheck',
            charset='utf8'
        )
        j = 1
        date, Lec_title, Lec_time, Lec_location, id = self.get_info_timAtxt(j)
        border = id
        while id > self.find_SQL():
            LSC_singDic = {"标题": Lec_title, "时间": Lec_time, "地点": Lec_location}
            self.LSC_Lt_list.append(LSC_singDic)
            print(id)
            j += 1
            date, Lec_title, Lec_time, Lec_location, id = self.get_info_timAtxt(j)

        print(self.LSC_Lt_list)
        self.update_SQL(border)
        self.SSPU_DB.close()
        if len(self.LSC_Lt_list):
            self.send_msg('[CQ:at,qq=all]第二课堂讲座有新出的！！快卷！')
            time.sleep(1)
            for i in range(0, len(self.LSC_Lt_list)):
                print(self.LSC_Lt_list)
                self.send_msg(f'{self.LSC_Lt_list[i]["标题"]}\n{self.LSC_Lt_list[i]["时间"]}\n{self.LSC_Lt_list[i]["地点"]}')

    def get_info_timAtxt(self, i):
        Lec_title = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div/div[5]/ul/li[{i}]/div[1]/div['
                                                  f'1]/div['f'2]/div[''1]/span[2]').text
        ids = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div/div[5]/ul/li[{i}]/div[1]/div[1]/div['
                                                 f'2]/div[1]/span[1]').text
        id = int(ids[:-1])
        self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div/div[5]/ul/li[{i}]/div[1]/div['
                                           f'1]/div['f'2]/div[''1]/span[2]').click()
        Lec_time = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div/div[1]/div['
                                                      f'3]/section/section[2]/section/section/section['
                                                      f'5]/section/section/section/section/section/section['
                                                      f'7]/section/section/section['
                                                      f'1]/section/section/section/section/section/section/p[1]').text
        Lec_location = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div/div[1]/div['
                                                          f'3]/section/section[2]/section/section/section['
                                                          f'5]/section/section/section/section/section/section['
                                                          f'7]/section/section/section['
                                                          f'1]/section/section/section/section/section/section/p['
                                                          f'2]').text
        self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div/div[1]/div[2]/span[1]/span[2]/span').click()
        date = "2022." + Lec_title[Lec_title.find('（') + 1:-1]
        self.i += 1
        return date, Lec_title, Lec_time, Lec_location, id

    def get_info(self):
        self.driver.implicitly_wait(10)
        url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3ODUzODczOA==&action=getalbum&album_id" \
              "=2611138528407896068&scene=173&from_msgid=2247489371&from_itemidx=1&count=3&nolastread=1" \
              "#wechat_redirect "
        self.driver.get(url)
        time.sleep(2)

        date, Lec_title, Lec_time, Lec_location, id = self.get_info_timAtxt(1)
        while datetime.strptime(date, "%Y.%m.%d") > datetime.strptime(self.today, "%Y.%m.%d"):
            LSC_singDic = {"标题": Lec_title, "时间": Lec_time, "地点": Lec_location}
            self.LSC_list.append(LSC_singDic)
            print(self.LSC_list)
            date, Lec_title, Lec_time, Lec_location, id = self.get_info_timAtxt(self.i)

    def send_msg(self, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload = None

        ip = '127.0.0.1'
        client.connect((ip, 5700))
        msg_type = 'group'
        number = QQ_Group

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

    def finish(self):
        time.sleep(2)
        self.driver.quit()

    def start_programme(self):
        self.get_info()
        self.finish()
        return self.LSC_list


if __name__ == '__main__':
    sspu = Lec_S_C()
    sspu.run_SQL()
