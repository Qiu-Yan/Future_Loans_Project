# coding=gbk
import unittest
from decimal import Decimal
from libs.ddt import ddt, data
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.RequestsHandler import HttpSessionHandler
from handler.LogHandler import log
from helper.helper import is_register_1, login_1, get_leave_amount, change_amount


"""��ȡ����"""
sheet = config.get('excel', 'withdraw_sheet')
ex = load_sheet(sheet)
test_case = ex.read()

"""��ȡ�û���Ϣ"""
mobile_phone = config.get('user', 'mobile_phone')
password = config.get('user', 'password')

# �ж��û��Ƿ�ע��
is_register_1()
# ��ȡ��Աid
member_id = eval(config.get('user', 'member_id'))


@ddt
class TestWithdraw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = config.get('api', 'base_url') + config.get('api', 'withdraw_url')
        cls.headers = eval(config.get('api', 'headers'))
        """�˻���ʼ���60��"""
        change_amount(member_id=member_id, amount=510000)
        # ��־��¼
        log.info(cls.url)

    def setUp(self):
        self.session = HttpSessionHandler()
        # ��¼���Ż�token_info
        token_info = login_1(self.session)
        self.headers['Authorization'] = token_info['token_type'] + " " + token_info['token']

        # ��ѯ��ǰ���, �������ڵ���60����Żص�ǰ�������С��60�����ֵ�����������
        # self.before_amount = recharge(self.session, self.headers, member_id)

        # ��־��¼
        # log.info(self.headers)

    @data(*test_case)
    def test_withdraw(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        json_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # ����ǰ���˻����
        before_amount = get_leave_amount(member_id)

        # �������ݴ���
        if json_data['member_id'] == 'id':
            json_data['member_id'] = member_id
        elif json_data['member_id'] == 'wrong_id':
            json_data['member_id'] = member_id - 1

        if json_data['amount'] == 'over_amount':
            amount = before_amount + Decimal(0.01).quantize(Decimal("0.00"))
            json_data['amount'] = float(amount)

        log.info(f'{case_id},{method},{description},{json_data},before_amount:{before_amount}')
        log.info(f'expected:{expected}')

        # ��������
        res_json = self.session.get_json(method=method, url=self.url, json=json_data, headers=self.headers)

        # ��־��¼
        log.info(f'result:{res_json}\n')

        # ��ȡsheet��ͷ
        sheet_title = ex.get_headers()
        result_index = sheet_title.index('result') + 1
        msg_index = sheet_title.index('msg') + 1
        code_index = sheet_title.index('code') + 1
        res_data_index = sheet_title.index('res_data') + 1

        # ��д
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

                # Ԥ�����
                expected_amount = before_amount - Decimal(json_data['amount']).quantize(Decimal("0.00"))

                # ���ݿ�ʵ�����
                leave_amount = get_leave_amount(member_id)

                # ���ֽӿڷ����˻����
                res_amount = Decimal(res_json['data']['leave_amount']).quantize(Decimal("0.00"))

                # ���ݿ����˻���� �� �����˻����ȶ�
                self.assertEqual(leave_amount, res_amount)

                # ���ֺ�Ԥ�����뷵�����ȶ�
                self.assertEqual(expected_amount, res_amount)
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e


