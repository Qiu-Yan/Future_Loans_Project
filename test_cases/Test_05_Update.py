# coding=gbk

import unittest
from libs.ddt import ddt, data
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.RequestsHandler import HttpSessionHandler
from handler.LogHandler import log
from helper.helper import is_register_1, login_1, get_user_info


"""读取测试数据"""
sheet = config.get('excel', 'update_sheet')
ex = load_sheet(sheet)
test_case = ex.read()

"""获取用户信息"""
# 判断是否注册，回写配置文件member_id
is_register_1()
member_id = eval(config.get('user', 'member_id'))


@ddt
class TestUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = config.get('api', 'base_url') + config.get('api', 'update_url')
        cls.headers = eval(config.get('api', 'headers'))
        # 日志记录
        log.info(f'{cls.url}')

        cls.session = HttpSessionHandler()

    def setUp(self):
        # 登录, 获取token
        token_info = login_1(self.session)
        token = token_info['token_type'] + ' ' + token_info['token']
        self.headers['Authorization'] = token

    @data(*test_case)
    def test_update(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # 特殊数据处理
        if json_data['member_id'] == 'id':
            json_data['member_id'] = member_id
        elif json_data['member_id'] == 'wrong_id':
            json_data['member_id'] = member_id - 1

        # 日志记录
        log.info(f'{case_id},{method},{description},{json_data}')
        log.info(f'expected:{expected}')

        # 发送请求
        res_json = self.session.get_json(method=method, url=self.url, json=json_data, headers=self.headers)
        # 日志记录
        log.info(f'result:{res_json}\n')

        # 获取sheet表头
        sheet_title = ex.get_headers()
        result_index = sheet_title.index('result') + 1
        msg_index = sheet_title.index('msg') + 1
        code_index = sheet_title.index('code') + 1
        res_data_index = sheet_title.index('res_data') + 1

        # 回写
        ex.write(case_id + 1, msg_index, res_json['msg'])
        ex.write(case_id + 1, code_index, str(res_json['code']))
        ex.write(case_id + 1, res_data_index, str(res_json['data']))

        code = expected['code']
        if code != 0:
            try:
                self.assertEqual(code, res_json['code'])
                self.assertEqual(expected['data'], res_json['data'])
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
        else:
            try:
                self.assertEqual(code, res_json['code'])

                # 查询数据库用户信息
                user_info = get_user_info(member_id)

                self.assertEqual(user_info['reg_name'], res_json['data']['reg_name'])
                self.assertEqual(expected['reg_name'], res_json['data']['reg_name'])
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
