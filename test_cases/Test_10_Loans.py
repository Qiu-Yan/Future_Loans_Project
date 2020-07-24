# coding=gbk

import unittest
from libs.ddt import ddt, data
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.RequestsHandler import HttpSessionHandler
from handler.LogHandler import log
from helper.helper import login_1, is_register_1

sheet = config.get('excel', 'loans_sheet')
ex = load_sheet(sheet)
test_case = ex.read()
is_register_1()


@ddt
class TestLoans(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = HttpSessionHandler()
        cls.url = config.get('api', 'base_url') + config.get('api', 'loans_url')
        cls.headers = eval(config.get('api', 'headers'))
        cls.headers.pop('Content-Type')

        token_info = login_1(cls.session)
        cls.headers['Authorization'] = token_info['token_type'] + ' ' + token_info['token']

        log.info(f'{cls.url}')

    @data(*test_case)
    def test_loans(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        if case_data['description'] == '未登录':
            self.headers.pop('Authorization')

        # 日志
        log.info(f'{self.headers}')
        log.info(f'{case_id},{method},{case_data["description"]},{json_data}')
        log.info(f'expected:{expected}')

        # 发起请求
        res_json = self.session.get_json(method=method, url=self.url, params=json_data, headers=self.headers)
        log.info(f'result:{res_json}\n')

        # 获取excel_title
        excel_title = ex.get_headers()
        result_index = excel_title.index('result') + 1
        msg_index = excel_title.index('msg') + 1
        code_index = excel_title.index('code') + 1
        res_data_index = excel_title.index('res_data') + 1

        # 回写excel
        ex.write(case_id + 1, msg_index, res_json['msg'])
        ex.write(case_id + 1, code_index, res_json['code'])

        code = expected['code']
        if code == 1003:
            try:
                self.assertEqual(code, res_json['code'])
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
        elif code != 0:
            try:
                self.assertEqual(code, res_json['code'])
                self.assertEqual(expected['data'], res_json['data'])
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
            finally:
                ex.write(case_id + 1, res_data_index, str(res_json['data']))
        else:
            try:
                self.assertEqual(code, res_json['code'])
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
            finally:
                ex.write(case_id + 1, res_data_index, str(res_json['data']))
