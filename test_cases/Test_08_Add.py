# coding=gbk

import unittest
from decimal import Decimal
from libs.ddt import ddt, data
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.LogHandler import log
from handler.RequestsHandler import HttpSessionHandler
from helper.helper import is_register_1, login_1, get_loan_info

"""获取测试数据"""
sheet = config.get('excel', 'add_sheet')
ex = load_sheet(sheet)
test_case = ex.read()

# 判断用户是否注册，回写新的member_id
is_register_1()

# 获取member_id
member_id = eval(config.get('user', 'member_id'))


@ddt
class TestLoanAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = config.get('api', 'base_url') + config.get('api', 'add_url')
        cls.headers = eval(config.get('api', 'headers'))

        cls.session = HttpSessionHandler()

        # 记录日志
        log.info(f'{cls.url}')

    def setUp(self):
        # 登录 获取token
        token_info = login_1(self.session)
        self.token = token_info['token_type'] + ' ' + token_info['token']
        self.headers['Authorization'] = self.token

        log.info(f'{self.headers}')

    @data(*test_case)
    def test_loan_add(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # 特殊数据处理
        if json_data['member_id'] == 'id':
            json_data['member_id'] = member_id
        elif json_data['member_id'] == 'other_id':
            json_data['member_id'] = member_id - 1
        elif json_data['member_id'] == 'not_login':
            json_data['member_id'] = member_id
            self.headers.pop('Authorization')
            log.info(self.headers)

        # 日志
        log.info(f'{case_id},{method},{description},{json_data}')
        log.info(f'expected:{expected}')

        # 发起请求
        res_json = self.session.get_json(method=method, url=self.url, json=json_data, headers=self.headers)
        log.info(f'result:{res_json}\n')

        # 获取sheet表头
        sheet_title = ex.get_headers()
        result_index = sheet_title.index('result') + 1
        msg_index = sheet_title.index('msg') + 1
        code_index = sheet_title.index('code') + 1
        res_data_index = sheet_title.index('res_data') + 1

        # 回写
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

                # 接口返回json的data
                res_data = res_json['data']
                res_amount = Decimal(res_data['amount']).quantize(Decimal("0.00"))
                res_rate = Decimal(res_data['loan_rate']).quantize(Decimal("0.000"))

                # 获取数据库中，项目信息
                loan_info = get_loan_info(res_data['id'])

                # 比对预期 和 返回结果
                self.assertEqual(member_id, res_data['member_id'])
                self.assertEqual(json_data['title'], res_data['title'])
                self.assertEqual(json_data['amount'], res_data['amount'])
                self.assertEqual(json_data['loan_rate'], res_data['loan_rate'])
                self.assertEqual(json_data['loan_term'], res_data['loan_term'])
                self.assertEqual(json_data['loan_date_type'], res_data['loan_date_type'])
                self.assertEqual(json_data['bidding_days'], res_data['bidding_days'])

                # 比对数据库信息 和返回信息
                self.assertEqual(loan_info['member_id'], res_data['member_id'])
                self.assertEqual(loan_info['title'], res_data['title'])
                self.assertEqual(Decimal(loan_info['amount']).quantize(Decimal("0.00")), res_amount)
                self.assertEqual(Decimal(loan_info['loan_rate']).quantize(Decimal("0.000")), res_rate)
                self.assertEqual(loan_info['loan_term'], res_data['loan_term'])
                self.assertEqual(loan_info['loan_date_type'], res_data['loan_date_type'])
                self.assertEqual(loan_info['bidding_days'], res_data['bidding_days'])

                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
            finally:
                ex.write(case_id + 1, res_data_index, str(res_json['data']))
