import socket
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import selenium.webdriver
from selenium.webdriver.common.by import By
import time
from API import *


class SchoolAutoCheckOK:
    def __init__(self, SSPU_AccountData, first):
        self.account = SSPU_AccountData["账号"]
        self.password = SSPU_AccountData["密码"]
        self.location = SSPU_AccountData["地址"]
        self.name = self.data = self.time = self.flag = None
        self.first = first

        # 反爬技术
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

    def send_msg(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload = None

        ip = '127.0.0.1'
        client.connect((ip, 5700))

        msg_type = 'group'
        number = QQ_Group

        if self.first == 1:
            msg = '7点了 起床了！！！和泉妃爱 来给你们汇报当日的签到结果啦: '

        else:
            if self.flag == 1:
                checkOK = "签到成功"
            else:
                checkOK = "签到失败"
            msg = f"二工大-每日一报 自动打卡：\n" \
                  f"{self.name}\n" \
                  f"账号: {self.account}\n" \
                  f"填报日期: {self.data}\n" \
                  f"填报时间: {self.time}\n" \
                  f"签到结果：{checkOK}"

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

    def check_ok(self):
        self.driver.implicitly_wait(10)
        url = "https://hsm.sspu.edu.cn/"
        self.driver.get(url)
        time.sleep(2)

        # 自动签到
        self.driver.find_element(By.ID, "username").send_keys(f"{self.account}")
        self.driver.find_element(By.ID, "password").send_keys(f"{self.password}")
        self.driver.find_element(By.CLASS_NAME, "submit_button").click()

        time.sleep(1)
        try:
            self.name = self.driver.find_element(By.XPATH, '/html/body/form/div[5]/div/span[2]').text
            self.driver.find_element(By.XPATH, '/html/body/form/div[6]/ul/li[2]/a/div').click()
            self.driver.find_element(By.XPATH,
                                     '/html/body/form/div[5]/div/div[2]/div[1]/div/ul/li[1]/a').click()
            self.data = self.driver.find_element(By.XPATH,
                                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[1]/div[2]/div/div/span').text
            self.time = self.driver.find_element(By.XPATH,
                                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[2]/div[2]/div/div/span').text
            self.flag = 1
            # self.driver.find_element(By.XPATH, '').click()

        except:
            self.flag = 0

    def finish(self):
        print(f'{datetime.now()} : SSPU Crawler is finished by once')
        time.sleep(2)
        self.driver.quit()

    def start_programme(self):
        if self.first != 1:
            self.check_ok()
        self.send_msg()
        self.finish()


if __name__ == '__main__':
    fir = SchoolAutoCheckOK(SSPU_AccountData=SSPU_AccountData_SchoolDay[0], first=1)
    fir.start_programme()
    for i in range(0, len(SSPU_AccountData_SchoolDay)):
        sspu = SchoolAutoCheckOK(SSPU_AccountData=SSPU_AccountData_SchoolDay[i], first=0)
        sspu.start_programme()
