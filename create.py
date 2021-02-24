# encoding=utf-8
import json
import re

import requests
import configparser

from login import  valid_cookie
from Jira import logging
from request_info import r_json
from loading_config import config_obj_of_jira_relation, config_obj_of_authority
from get_info_from_excel import GetInfoFromExcel


class Create:
    """创建jira"""
    SUGGESTIONS = ["项目", "问题类型"]
    OPTIONS = ["模块", "优先级", "复现概率", "遗留标志", "缺陷分类", "发现方式", "发现难度",
               "发现阶段", "发现版本", "是否一体化测试发现", "是否修改引入"]
    FIELDS_TO_RETAIN = ("project", "issuetype", "components", "priority", "customfield_11019",
                        "customfield_11020", "customfield_11024", "customfield_11023", "customfield_11004",
                        "customfield_11021", "customfield_11029", "customfield_11014", "assignee",
                        "customfield_11011", "customfield_11018", "reporter", "customfield_10001",
                        "customfield_11000", "customfield_11993", "customfield_11581", "customfield_11680",
                        "issuelinks", "labels", "customfield_10391", "customfield_12080")

    def __init__(self, json_text):
        # jira 接口QuickCreateIssue返回的数据
        self.json_text = json_text
        # jira字段中前端展示与实际传参对照字典 例如：{}
        self.argues_relation = {}
        # 创建jira bug时，经处理的实际传参数据
        # self.request_argues = {"fieldsToRetain": Create.FIELDS_TO_RETAIN}
        self.request_argues = {"atl_token": None,
                               "formToken": "",
                               "fieldsToRetain": Create.FIELDS_TO_RETAIN}
        self.headers = {"Cookie": valid_cookie}

    def get_main_info(self):
        """从QuickCreateIssue!default.jspa返回的json串中提取必要的数据信息> """
        for field_info in self.json_text["fields"]:
            self.set_aruges_relation(field_info=field_info)

    def set_aruges_relation(self, field_info):
        """判断是否为可选项数据， 若是返回可选项的数据列表； 否则，返回 False"""
        label_id = field_info.get("id")
        label = field_info.get("label")
        edit_html_info = field_info.get("editHtml")
        logging.info(label + "=" + label_id + ",1")
        if label in Create.OPTIONS:
            logging.info("*"*10 + label + "*"*10)
            argues_relation = self.extract_options_from_edit_html_label(edit_html_info=edit_html_info, label=label)
        elif label in Create.SUGGESTIONS:
            logging.info("=" * 10 + label + "=" * 10)
            argues_relation = self.extract_suggestions_from_edit_html_label(edit_html_info=edit_html_info, label=label)
        else:
            self.argues_relation.setdefault(label, label_id)
            logging.info("Label [{}] do not in OPTIONS or SUGGESTIONS.".format(label))
            return
        logging.debug("label:{0}\n{1}".format(label, argues_relation))
        return

    def extract_options_from_edit_html_label(self, edit_html_info, label):
        """提取 editHtml 中的 option标签的信息"""
        if not self.argues_relation.get(label):
            self.argues_relation.setdefault(label, {})
        options = re.findall('value=\\"(\w+?)\\"[\s\S]*?>\\n*\s*(\S+)\s*</option>', edit_html_info)
        for option in options:
            self.argues_relation.get(label).setdefault(option[-1], option[0])
            logging.debug(self.argues_relation.get(label))
            logging.info(option)
        return self.argues_relation.get(label)

    def extract_suggestions_from_edit_html_label(self, edit_html_info, label):
        """提取 editHtml 中的 suggestions-data 数据的信息"""
        if not self.argues_relation.get(label):
            self.argues_relation.setdefault(label, {})
        options = re.findall('&quot;label&quot;:&quot;([\s\S]{1,20})&quot;,&quot;value&quot;:&quot;(\d+)&quot;,&quot;icon&quot;', edit_html_info)
        options = set(options)
        for option in options:
            self.argues_relation.get(label).setdefault(option[0], option[-1])
            logging.info(option)
        return self.argues_relation.get(label)

    def set_request_argues(self, label, bug_content, config_obj):
        """请求入参格式化"""
        param, need_transform = config_obj["default"][label].split(",")
        try:
            if label == "描述":
                d1, d2, d3, d4 = bug_content.split("|||")
                description = """
                【前置条件】:{0}\n【操作步骤】:{1}\n【预期结果】:{2}\n【实际结果】:{3}\n
                """.format(d1, d2, d3, d4)
                self.request_argues.setdefault(param, description)
                return
            self.request_argues.setdefault(param, self.argues_relation.get(label).get(bug_content))
            logging.info("Request argue [{0}] is [{1}]".format(param, self.request_argues.get(param)))
        except AttributeError as e:
            self.request_argues.setdefault(self.argues_relation.get(label), bug_content)
            logging.warning("Something wrong when dealing with label.Argues is: [label:{0}],[bug_content:{1}]"\
                          .format(label, bug_content))

    def create(self, template_header, bug_info, config_obj_of_jira_relation, config_obj_of_authority, **kwargs):
        """创建jira"""
        # 获取jira凭证信息，例如：cookie
        self.request_argues.update({"atl_token": self.headers.get("Cookie").split(";")[0].split("=")[1]})

        self.get_main_info()
        # 扫描excel表中每一行的bug记录，并调用接口创建对应bug
        for no, bug_content in bug_info.items():
            label = template_header.get(int(no.split("-")[1]))
            self.set_request_argues(label=template_header.get(int(no.split("-")[1])), bug_content=bug_content,
                                     config_obj=config_obj_of_jira_relation)
        logging.debug("Finally Argues: \n{0}".format(self.request_argues))
        r = requests.post(url="https://se.hundsun.com/secure/QuickCreateIssue.jspa?decorator=none",
                          headers=self.headers,
                          data=self.request_argues)
        logging.debug(r.json())


get_info_from_excel = GetInfoFromExcel(filename="config/jira_template.xls")
template_header, bug_info = get_info_from_excel.get_data(table=get_info_from_excel.workbook.sheet_by_name("bugs"))

create = Create(json_text=r_json)
create.create(template_header=template_header, bug_info=bug_info,
              config_obj_of_jira_relation=config_obj_of_jira_relation,
              config_obj_of_authority=config_obj_of_authority)

