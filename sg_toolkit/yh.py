# -*- coding: utf-8 -*-
"""
外网安全考试自动答题
"""
import re
import os
import time
from typing import List
import logging
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
from tqdm import tqdm


class FuckAnGui:
    def __init__(self, username: str, password: str, url: str, answers_path: str, question_num: int = 100):
        """
        初始化\n
        :param username: 用户名
        :param password: 密码：Fk+身份证后六位+,
        :param url: 登陆网址
        :param answers_path: 题库文件路径
        :param question_num: 问题数量，可用于控制正确率
        """
        self.username = username
        self.password = password
        self.url = url
        self.driver = Chrome()
        self.driver.implicitly_wait(30)
        self.vars = {}
        self.answers = pd.read_excel(answers_path, dtype=str)
        self.answers = self.answers.fillna("")
        self.answers["题干"] = self.answers["题干"].apply(lambda x: re.sub(r"\s+", "", x).replace("()", "").replace("（）", ""))
        for _abcdef_ in "ABCDEF":
            self.answers[f"选项{_abcdef_}"] = self.answers[f"选项{_abcdef_}"].apply(lambda x: re.sub(r"\s+", "", x).replace("||", "|"))
        self.answers["答案"] = self.answers["答案"].apply(lambda x: re.sub(r"\s+", "", x))
        self.answers["题型"] = self.answers["答案"].apply(self.__get_question_type__)
        self.question_num = question_num

    @staticmethod
    def __get_question_type__(_answer_: str) -> str:
        """
        获得题型\n
        :param _answer_: 答案
        :return: 单选题、多选题、判断题
        """
        if _answer_ in ("正确", "错误"):
            return "判断题"
        if len(_answer_) == 1:
            return "单选题"
        else:
            return "多选题"

    def __find_elements_displayed__(self, xpath: str) -> List[WebElement]:
        """
        使用XPATH找非隐藏元素\n
        :param xpath: xpath路径
        :return: 非隐藏元素
        """
        result = self.driver.find_elements_by_xpath(xpath)
        return [x for x in result if x.is_displayed()]

    def __find_element_displayed__(self, xpath: str, index: int = -1) -> WebElement:
        """
        使用XPATH找非隐藏元素\n
        :param xpath: xpath路径
        :param index: 找第几个，默认-1
        :return: 非隐藏元素
        """
        return self.__find_elements_displayed__(xpath)[index]

    def teardown_method(self):
        """
        关闭浏览器\n
        :return:
        """
        self.driver.quit()

    def login(self):
        """
        登陆系统\n
        :return:
        """
        self.driver.get(self.url)
        self.driver.find_element_by_xpath("//input[@placeholder='请输入用户名']").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@placeholder='请输入密码']").send_keys(self.password)
        self.driver.find_element_by_xpath("//div[@id='loginBtn']").click()

    def enter(self):
        """
        进入考试界面\n
        :return:
        """
        self.driver.find_element_by_css_selector("div#tyks.intoType.ini_tk").click()
        self.driver.find_element_by_css_selector("div.examitem").click()
        self.driver.find_element_by_css_selector("button.swal2-confirm.swal2-styled").click()

    def __get_bg_title__(self):
        """
        获取题型\n
        :return: 题型
        """
        return re.sub(r"\s+", "", self.driver.find_element_by_css_selector("div.bg_title").text)

    def __get_question_title__(self):
        """
        获取题干\n
        :return: 题干
        """
        if self.__get_bg_title__() in ("单选题", "多选题"):
            result = self.driver.find_element_by_css_selector("div.question_choose_title").text
        else:
            result = self.driver.find_element_by_css_selector("div.question_judge_title").text
        result = re.sub(r"\s+", "", result).replace("(保命题)", "").replace("()", "").replace("（）", "")
        return result

    def __get_options_item__(self):
        """
        获取选项\n
        :return: 选项
        """
        return self.driver.find_elements_by_css_selector("div.question_choose_options_item_txt")

    def __get_bg_size__(self):
        """
        获取第几题\n
        :return: 第几题
        """
        return self.driver.find_element_by_css_selector("div.bg_size").text.strip()

    def search_answer(self):
        """
        寻找答案\n
        :return: 答案对应的文字内容，不包括ABCD字母
        """
        result = self.answers[(self.answers["题型"] == self.__get_bg_title__()) & (self.answers["题干"] == self.__get_question_title__())]
        final_result = []
        if result.shape[0] > 0:
            if result["题型"].iloc[0] in ("单选题", "多选题"):
                for _result_ in result["答案"].iloc[0]:
                    final_result.append(result.iloc[0].loc[f"选项{_result_}"])
            elif result["题型"].iloc[0] == "判断题":
                final_result.append(result["答案"].iloc[0])
            else:
                raise ValueError(f"不支持的题型 {result['题型'].iloc[0]}")
        else:
            logging.info(f"未找到答案: {self.__get_question_title__()}")
        return [x.strip() for x in final_result]

    def exam(self):
        """
        进行一场考试\n
        :return: 得分页面文字内容
        """
        time.sleep(2)
        for _ in tqdm(range(self.question_num)):
            answer = self.search_answer()
            if self.__get_bg_title__() in ("单选题", "多选题"):
                for ans in list(answer):
                    for option_item in self.__get_options_item__():
                        if re.sub(r"\s+", "", option_item.text.split("-", 1)[-1]) == ans:
                            option_item.click()
            elif self.__get_bg_title__() == "判断题":
                if "正确" == answer[0]:
                    self.driver.find_element_by_css_selector("img.question_judge_options_item.judge_true").click()
                elif "错误" == answer[0]:
                    self.driver.find_element_by_css_selector("img.question_judge_options_item.judge_false").click()
                else:
                    raise ValueError(f"判断题答案只能是 正确 或 错误 : {self.__get_question_title__()}")
            else:
                raise ValueError(f"不支持的题型: {self.__get_bg_title__()}")
            self.driver.find_element_by_css_selector("div.bg_btn.bg_next").click()
            time.sleep(2)
        self.driver.find_element_by_css_selector("img.submit-paper-btn").click()
        self.driver.find_element_by_css_selector("button.swal2-confirm.swal2-styled").click()
        time.sleep(2)
        return self.driver.find_element_by_tag_name("body").text

    def run(self):
        """
        登录，进入考试页面，进行一场考试\n
        :return: 得分页面文字内容
        """
        self.login()
        self.enter()
        return self.exam()
