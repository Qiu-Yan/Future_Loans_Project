# coding=gbk

import unittest
from decimal import Decimal
from libs.ddt import ddt, data
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.RequestsHandler import HttpSessionHandler
from handler.LogHandler import log
from helper.helper import is_register_1, login_1, \
    get_invest_info, get_leave_amount, change_amount, get_loan_info, add_loan
from helper.exchange_data import invest_json_data


"""获取测试数据"""
sheet = config.get('excel', 'invest_sheet')
ex = load_sheet(sheet)
test_case = ex.read()

is_register_1()
# 获取member_id
member_id = eval(config.get('user', 'member_id'))


@ddt
class TestInvest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = HttpSessionHandler()
        cls.url = config.get('api', 'base_url') + config.get('api', 'invest_url')
        cls.headers = eval(config.get('api', 'headers'))
        log.info(f'url:{cls.url}')

        change_amount(member_id, amount=2500)
        if get_loan_info() is None:
            add_loan()

    def setUp(self):
        token_info = login_1(session=self.session)
        token = token_info['token_type'] + ' ' + token_info['token']
        self.headers['Authorization'] = token

    @data(*test_case)
    def test_invest(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # 特殊数据处理
        json_data = invest_json_data(json_data)
        if json_data['member_id'] == 'not_login':
            json_data['member_id'] = member_id
            self.headers.pop('Authorization')

        # 投资前的账户余额
        before_amount = get_leave_amount(member_id)

        log.info(f'headers:{self.headers}')
        log.info(f'{case_id},{method},{description},{json_data},before_amount:{before_amount}')
        log.info(f'expected:{expected}')

        # 发送请求
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
                invest_id = res_json['data']['id']
                invest_info = get_invest_info(invest_id)

                # 预期结果 与 返回信息 对比
                self.assertEqual(json_data['member_id'], res_json['data']['member_id'])
                self.assertEqual(json_data['loan_id'], res_json['data']['loan_id'])
                self.assertEqual(json_data['amount'], res_json['data']['amount'])

                # 数据库 与 返回信息对比
                self.assertEqual(invest_info['member_id'], res_json['data']['member_id'])
                self.assertEqual(invest_info['loan_id'], res_json['data']['loan_id'])
                self.assertEqual(invest_info['amount'], Decimal(res_json['data']['amount']))

                # 投资成功，账号余额减少
                leave_amount = get_leave_amount(member_id)
                after_amount = before_amount - Decimal(json_data['amount']).quantize(Decimal("0.00"))
                log.info(f'expected_leave_amount:{after_amount}, leave_amount:{leave_amount}')
                self.assertEqual(after_amount, leave_amount)
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
            finally:
                ex.write(case_id + 1, res_data_index, str(res_json['data']))
