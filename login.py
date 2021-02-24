import re

import requests
import logging
import time

from Jira import logging
from loading_config import config_obj_of_authority

class Login:
    def __init__(self, config_obj_of_authority):
        self.login_url = "https://hs-cas.hundsun.com/cas/login?service=https%3A%2F%2Fse.hundsun.com%2F"
        self.authority = config_obj_of_authority
        self.cookie = ""

    def phatomjs_login(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        # driver = webdriver.Chrome()
        # 模拟无界面谷歌浏览器操作
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url=self.login_url)
        time.sleep(1)
        # 登录
        driver.find_element_by_xpath(xpath='//*[@id="username"]').send_keys(self.authority['default']['username'])
        driver.find_element_by_xpath(xpath='//*[@id="password"]').send_keys(self.authority['default']['password'])
        driver.find_element_by_xpath(xpath='//*[@id="submit_psd"]/input').click()
        # 获取登录后token信息
        token = driver.get_cookie(name="atlassian.xsrf.token")
        logging.info("atlassian.xsrf.token info is [{}]".format(token))
        jessionid = driver.get_cookie(name="JSESSIONID")
        logging.info("JSESSIONID info is [{}]".format(jessionid))
        self.cookie += token.get("name") + "=" + token.get("value") + "; jira.editor.user.mode=wysiwyg;"
        self.cookie += jessionid.get("name") + "=" + jessionid.get("value")
        logging.info("The valid cookie is [{}]".format(self.cookie))
        driver.quit()

    def get_valid_cookie(self):
        return self.cookie


login = Login(config_obj_of_authority=config_obj_of_authority)
login.phatomjs_login()
valid_cookie = login.get_valid_cookie()