# -*- coding: utf-8 -*-
"""
网上学堂自动刷课
"""
import re
import time
from urllib.parse import urlparse
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm


class FuckGWXT:
    def __init__(self, username: str, password: str, company: str, url: str):
        """
        初始化\n
        :param username: ISC用户名
        :param password: ISC密码
        :param company: 公司
        :param url: 网课网址
        """
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        match = re.search(r"[?&]tcID=([a-zA-Z0-9]+)", url)
        if match:
            self.lesson_id = match.group(1)
        else:
            raise ValueError("无效的url")
        self.username = username
        self.password = password
        self.company = company
        self.url = url
        self.driver = Chrome()
        self.driver.implicitly_wait(30)
        self.vars = {}
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def login(self):
        self.driver.get(self.url)
        time.sleep(3)
        element = self.driver.find_element(By.ID, "department")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.CSS_SELECTOR, ".department_title")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.CSS_SELECTOR, "#fm1 > li:nth-child(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".tab_item2").click()
        self.driver.find_element(By.LINK_TEXT, self.company).click()

        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)

        self.driver.find_element(By.ID, "submit_login").click()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def process_row(self, tr: WebElement) -> bool:
        """
        处理表格中的一行\n
        :param tr: 一行对应的tr元素
        :return: 是否进行了学习
        """
        tds = tr.find_elements_by_tag_name("td")
        if "100%" == str(tr.find_element_by_css_selector("div.jdt_bg_num").text).strip():
            return False           # 已经学习进度到了100%，无需学习
        else:
            window_handle_past = self.driver.current_window_handle
            wh_past = self.driver.window_handles
            tr.find_element_by_css_selector("a[href^='javascript:_enterCourse']").click()
            time.sleep(3)
            try:
                self.driver.switch_to.window(set(self.driver.window_handles).difference(set(wh_past)).pop())
                self.driver.execute_script("document.querySelector('video').muted = true;")
                self.driver.execute_script("document.querySelector('video').play();")
                time.sleep(3)
                try:
                    self.driver.execute_script("document.querySelector('video').currentTime = document.querySelector('video').duration;")
                    self.driver.execute_script("document.querySelector('video').dispatchEvent(new Event('ended'));")
                except:
                    pass
                time.sleep(3)
                self.driver.close()
                self.driver.switch_to.window(window_handle_past)
            except KeyError as e:
                self.driver.back()
                time.sleep(3)
            return True

    def baodao(self):
        """
        点击报道\n
        :return: True 未报到->已报道; False 已报道
        """
        btn_bm = self.driver.find_element_by_css_selector("#ckmore").find_element_by_css_selector("div.btnbm").find_element_by_tag_name("a")
        if "报到" == btn_bm.text:
            btn_bm.click()
            time.sleep(3)
            self.driver.switch_to.alert.accept()
            return True
        elif "报名" == btn_bm.text:
            raise ValueError("该课程尚未报名，请检查")
        else:
            return False

    def learn(self) -> int:
        """
        学习课程\n
        :return: 学习了几个课
        """
        self.driver.get(f"http://{urlparse(self.url).hostname}/www/command/CollegeControl?flag=collegeTC&tcID={self.lesson_id}&tab=collTcLesson&type=&worktypeid=&pageNo1=1&pageSize1=999&comewho=null")
        self.baodao()
        table = self.driver.find_element_by_css_selector("table.tabbleys")
        rows = table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        result = 0
        for row in tqdm(rows):
            result = result + self.process_row(row)
        return result

    def refresh(self):
        return self.driver.refresh()

    def process(self):
        self.login()
        result = self.learn()
        self.refresh()
        return result
