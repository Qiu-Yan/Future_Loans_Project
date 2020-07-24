# coding=gbk

import unittest
from libs.ddt import ddt, data
from decimal import Decimal
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.LogHandler import log
from handler.RequestsHandler import HttpSessionHandler
from helper.helper import is_register_1, login_1, get_leave_amount


"""读取测试数据"""
sheet = config.get('excel', 'recharge_sheet')
ex = load_sheet(sheet)
test_data = ex.read()

"""获取用户信息"""
mobile_phone = config.get('user', 'mobile_phone')
password = config.get('user', 'password')

# 判断用户是否存在，若不存在，则创建，并回写配置文件 user_id, 若存在，也回写 user_id
is_register_1()
# 获取 user id
member_id = eval(config.get('user', 'member_id'))



@ddt
class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 获取 配置文件中的请求地址url，请求头headers
        cls.url = config.get('api', 'base_url') + config.get('api', 'recharge_url')
        cls.headers = eval(config.get('api', 'headers'))
        log.info(cls.url)

    def setUp(self):
        # 初始化session
        self.session = HttpSessionHandler()
        # 登录账号，获取token_info
        token_info = login_1(self.session)
        token = token_info['token_type'] + ' ' + token_info['token']
        # 完善请求头
        self.headers['Authorization'] = token
        log.info(self.headers)

    @data(*test_data)
    def test_recharge(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # 对特殊数据进行处理
        if json_data['member_id'] == 'id':
            json_data['member_id'] = member_id
        elif json_data['member_id'] == 'wrong_id':
            json_data['member_id'] = member_id - 1

        # 获取账户充值前，数据库中存储的账户余额
        before_amount = get_leave_amount(member_id)

        # 日志记录
        log.info(f'{case_id},{method},{description},{json_data},before_amount:{before_amount}')
        log.info(f'expected:{expected}')

        # 发起请求
        res_json = self.session.get_json(method=method, url=self.url, json=json_data, headers=self.headers)

        # 日志记录
        log.info(f'result:{res_json}\n')

        # 获取sheet 表头
        sheet_title = ex.get_headers()
        result_index = sheet_title.index('result')+1
        code_index = sheet_title.index('code')+1
        msg_index = sheet_title.index('msg')+1
        res_data_index = sheet_title.index('res_data')+1

        # 回写数据
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
                ex.write(case_id+1, result_index, "Failed")
                raise e
        else:
            try:
                self.assertEqual(code, res_json['code'])

                # 预期充值成功后的账户余额
                expected_amount = before_amount + Decimal(json_data['amount']).quantize(Decimal("0.00"))

                # 获取充值成功后，数据库中存储的账户余额
                leave_amount = get_leave_amount(member_id)

                res_leave_amount = Decimal(res_json['data']['leave_amount']).quantize(Decimal("0.00"))

                # 比对数据库账户余额，与 返回账户余额
                self.assertEqual(leave_amount, res_leave_amount)
                self.assertEqual(expected_amount, res_leave_amount)
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
