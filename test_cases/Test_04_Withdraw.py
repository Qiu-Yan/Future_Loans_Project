# coding=gbk
import unittest
from decimal import Decimal
from libs.ddt import ddt, data
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.RequestsHandler import HttpSessionHandler
from handler.LogHandler import log
from helper.helper import is_register_1, login_1, get_leave_amount, change_amount


"""读取数据"""
sheet = config.get('excel', 'withdraw_sheet')
ex = load_sheet(sheet)
test_case = ex.read()

"""获取用户信息"""
mobile_phone = config.get('user', 'mobile_phone')
password = config.get('user', 'password')

# 判断用户是否注册
is_register_1()
# 获取会员id
member_id = eval(config.get('user', 'member_id'))


@ddt
class TestWithdraw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = config.get('api', 'base_url') + config.get('api', 'withdraw_url')
        cls.headers = eval(config.get('api', 'headers'))
        """账户初始余额60万"""
        change_amount(member_id=member_id, amount=510000)
        # 日志记录
        log.info(cls.url)

    def setUp(self):
        self.session = HttpSessionHandler()
        # 登录并放回token_info
        token_info = login_1(self.session)
        self.headers['Authorization'] = token_info['token_type'] + " " + token_info['token']

        # 查询当前余额, 若余额大于等于60万，则放回当前余额；若余额小于60万，则充值，并返回余额
        # self.before_amount = recharge(self.session, self.headers, member_id)

        # 日志记录
        # log.info(self.headers)

    @data(*test_case)
    def test_withdraw(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # 提现前，账户余额
        before_amount = get_leave_amount(member_id)

        # 特殊数据处理
        if json_data['member_id'] == 'id':
            json_data['member_id'] = member_id
        elif json_data['member_id'] == 'wrong_id':
            json_data['member_id'] = member_id - 1

        if json_data['amount'] == 'over_amount':
            amount = before_amount + Decimal(0.01).quantize(Decimal("0.00"))
            json_data['amount'] = float(amount)

        log.info(f'{case_id},{method},{description},{json_data},before_amount:{before_amount}')
        log.info(f'expected:{expected}')

        # 发起请求
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
        ex.write(case_id+1, msg_index, res_json['msg'])
        ex.write(case_id+1, code_index, str(res_json['code']))
        ex.write(case_id+1, res_data_index, str(res_json['data']))

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

                # 预期余额
                expected_amount = before_amount - Decimal(json_data['amount']).quantize(Decimal("0.00"))

                # 数据库实际余额
                leave_amount = get_leave_amount(member_id)

                # 提现接口返回账户余额
                res_amount = Decimal(res_json['data']['leave_amount']).quantize(Decimal("0.00"))

                # 数据库中账户余额 与 返回账户余额比对
                self.assertEqual(leave_amount, res_amount)

                # 提现后预期余额，与返回余额比对
                self.assertEqual(expected_amount, res_amount)
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e


