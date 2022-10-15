from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from API import *



# 爬虫程序
class SchoolAutoCheckIn:
    def __init__(self, SSPU_AccountData):
        self.account = SSPU_AccountData["账号"]
        self.password = SSPU_AccountData["密码"]
        self.location = SSPU_AccountData["地址"]

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

    def check_in(self):
        self.driver.implicitly_wait(10)
        url = "https://hsm.sspu.edu.cn/"
        self.driver.get(url)
        time.sleep(2)

        # 自动签到
        self.driver.find_element(By.ID, "username").send_keys(f"{self.account}")
        self.driver.find_element(By.ID, "password").send_keys(f"{self.password}")
        self.driver.find_element(By.CLASS_NAME, "submit_button").click()

        time.sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/form/div[6]/ul/li[1]/a/div').click()

        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[4]/div[2]/div/table/tr/td[1]/div/div['
                                 '2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[5]/div[2]/div/table/tr/td[1]/div/div['
                                 '2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[9]/div[2]/div/table/tr[1]/td['
                                 '1]/div/div[2]/div/label').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[10]/div[2]/div/table/tr/td[1]/div/div['
                                 '2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[11]/div[2]/div/table/tr[2]/td['
                                 '2]/div/div[2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[12]/div[2]/div/table/tr[2]/td[2]/div'
                                 '/div[2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[15]/div[2]/div/table/tr[1]/td[1]/div'
                                 '/div[2]/div/label').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[16]/div[2]/div/table/tr/td[2]/div/div[2]'
                                 '/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[19]/div[2]/div/table/tr/td[2]/div/div['
                                 '2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[28]/div[2]/div/table/tr[1]/td/div/div['
                                 '2]/div/label').click()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[30]/div[2]/div/table/tr[2]/td['
                                 '1]/div/div[2]/div/label').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[7]/div[2]/div/div/div[1]'
                                 '/input').clear()
        self.driver.find_element(By.XPATH,
                                 '/html/body/form/div[5]/div/div[2]/div[1]/div[7]/div[2]/div/div/div[1]'
                                 '/input').send_keys("36.5")

        # Location
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[24]/div[2]/div/input[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[24]/div[2]/div/input[2]").find_element(
            By.XPATH, f"//li[@data-value='{self.location[0]}']"
        ).click()
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[25]/div[2]/div/input[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[25]/div[2]/div/input[2]").find_element(
            By.XPATH, f"//li[@data-value='{self.location[1]}']"
        ).click()
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[26]/div[2]/div/input[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[26]/div[2]/div/input[2]").find_element(
            By.XPATH, f"//li[@data-value='{self.location[2]}']"
        ).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[27]/div[2]/div/input").clear()
        self.driver.find_element(By.XPATH,
                                 "/html/body/form/div[5]/div/div[2]/div[1]/div[27]/div[2]/div/input").send_keys(self.location[3])
        time.sleep(1)
        self.driver.find_element(By.CLASS_NAME, "f-btn-text").click()

    def finish(self):
        print(f'{datetime.now()} : SSPU Crawler is finished by once')
        time.sleep(2)
        self.driver.quit()

    def start_programme(self):
        self.check_in()
        self.finish()


if __name__ == '__main__':
    for i in range(0, len(SSPU_AccountData_SchoolDay)):
        sspu = SchoolAutoCheckIn(SSPU_AccountData=SSPU_AccountData_SchoolDay[i])
        sspu.start_programme()