# -*- coding: utf-8 -*-
"""
安全考试自动答题
"""
import re
import os
import time
from typing import List
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd


class FuckAnGui:
    def __init__(self, username: str, password: str, url: str, answers_path: str):
        """
        初始化\n
        :param username: 用户名
        :param password: 密码：Fk+身份证后六位+,
        :param url: 登陆网址
        :param answers_path: 题库文件路径
        """
        self.username = username
        self.password = password
        self.url = url
        cache_path = os.path.join(os.path.abspath(os.getcwd()), self.username)
        os.makedirs(cache_path, exist_ok=True)
        options = Options()
        options.add_argument(f"--user-data-dir={cache_path}")
        self.driver = Chrome(options=options)
        self.driver.implicitly_wait(30)
        self.vars = {}
        self.answers = pd.read_excel(answers_path)
        self.answers["题干"] = self.answers["题干"].apply(lambda x: x.replace(" ", "").replace("\n", "").replace("()", "").replace("（）", ""))
        self.answers["选项"] = self.answers["选项"].apply(lambda x: x.replace("||", "|"))

    def __find_elements_displayed__(self, xpath: str) -> List[WebElement]:
        result = self.driver.find_elements_by_xpath(xpath)
        return [x for x in result if x.is_displayed()]

    def __find_element_displayed__(self, xpath: str, index: int = -1) -> WebElement:
        return self.__find_elements_displayed__(xpath)[index]

    def teardown_method(self):
        self.driver.quit()

    def login(self):
        self.driver.get(self.url)
        wh_past = self.driver.window_handles
        self.driver.find_element_by_xpath("//div[text()='安全知识考试']").click()
        time.sleep(1)
        try:
            self.driver.switch_to.window(set(self.driver.window_handles).difference(set(wh_past)).pop())
        except KeyError as e:
            self.driver.find_element_by_xpath("//div[@class='login-form']/form/div[1]//input").send_keys(self.username)
            self.driver.find_element_by_xpath("//div[@class='login-form']/form/div[2]//input").send_keys(self.password)
            exit()

    def enter(self):
        self.driver.find_element_by_css_selector("div#tyks.intoType.ini_tk").click()
        self.driver.find_element_by_css_selector("div.examitem").click()
        self.driver.find_element_by_css_selector("button.swal2-confirm.swal2-styled").click()

    def __get_bg_title__(self):
        return self.driver.find_element_by_css_selector("div.bg_title").text

    def __get_question_title__(self):
        if self.__get_bg_title__() in ("单选题", "多选题"):
            result = self.driver.find_element_by_css_selector("div.question_choose_title").text
        else:
            result = self.driver.find_element_by_css_selector("div.question_judge_title").text
        result = result.replace("(保命题)", "").replace(" ", "").replace("()", "").replace("（）", "")
        return result

    def __get_options_item__(self):
        return self.driver.find_elements_by_css_selector("div.question_choose_options_item_txt")

    def __get_bg_size__(self):
        return self.driver.find_element_by_css_selector("div.bg_size").text

    def search_answer(self):
        result = self.answers[(self.answers["题型"] == self.__get_bg_title__()) & (self.answers["题干"] == self.__get_question_title__())]
        final_result = []
        if result.shape[0] > 0:
            for res in result["选项"].iloc[0].split("|"):
                if res[0] in list(result["答案"].iloc[0]):
                    final_result.append(res)
        else:
            print("??", self.__get_question_title__())
        return [x.split("-", 1)[-1] for x in final_result]

    def exam(self):
        i = 0
        while i < 100:
            print(self.__get_bg_size__())
            answer = self.search_answer()
            if self.__get_bg_title__() in ("单选题", "多选题"):
                for ans in list(answer):
                    for option_item in self.__get_options_item__():
                        if option_item.text.split("-", 1)[-1] == ans:
                            option_item.click()
            elif self.__get_bg_title__() == "判断题":
                if len(answer) > 0:
                    if "正确" == answer[0]:
                        self.driver.find_element_by_css_selector("img.question_judge_options_item.judge_true").click()
                    else:
                        self.driver.find_element_by_css_selector("img.question_judge_options_item.judge_false").click()
            else:
                pass
            self.driver.find_element_by_css_selector("div.bg_btn.bg_next").click()
            time.sleep(2)
            i = i + 1
        self.driver.find_element_by_css_selector("img.submit-paper-btn").click()
        self.driver.find_element_by_css_selector("button.swal2-confirm.swal2-styled").click()
        time.sleep(2)
        print(self.driver.find_element_by_tag_name("body").text)

    def process(self):
        self.login()
        self.enter()
        self.exam()
