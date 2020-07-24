# coding=gbk

import unittest
from libs.ddt import ddt, data
from decimal import Decimal
from handler.ConfigHandler import config
from handler.ExcelHandler_one import load_sheet
from handler.LogHandler import log
from handler.RequestsHandler import HttpSessionHandler
from helper.helper import is_register_1, login_1, get_user_info

"""��ȡ��������"""
sheet = config.get('excel', 'info_sheet')
ex = load_sheet(sheet)
test_case = ex.read()

# �ж��û��Ƿ�ע��
is_register_1()
# ��ȡ�û�member_id
member_id = config.get('user', 'member_id')


@ddt
class TestInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = config.get('api', 'base_url')
        cls.headers = eval(config.get('api', 'headers'))
        cls.headers.pop('Content-Type')

        cls.session = HttpSessionHandler()

    def setUp(self):
        # ��¼ ��ȡtoken
        token_info = login_1(self.session)
        token = token_info['token_type'] + " " + token_info['token']
        self.headers['Authorization'] = token

    @data(*test_case)
    def test_info(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        id_data = case_data['id']
        expected = eval(case_data['expected'])

        # info_url �ӿڵ�ַƴ�ӣ�/member/{member_id}/info
        if id_data == 'member_id':
            info_url = '/member/' + member_id + '/info'
        elif id_data == 'other_id':
            other_id = int(member_id) - 1
            info_url = '/member/' + str(other_id) + '/info'
        elif id_data == 'not_id':
            info_url = '/member/' + member_id + 's/info'
        elif id_data == 'None':
            info_url = '/member//info'
        else:
            info_url = f'/member/{id_data}/info'

        # �����Ľӿڵ�ַ
        url = self.base_url + info_url

        # ��־��¼
        log.info(f'{case_id},{method},{description},{url},{self.headers}')
        log.info(f'expected:{expected}')

        # ��������
        res_json = self.session.get_json(method=method, url=url, headers=self.headers)
        log.info(f'result:{res_json}\n')

        # ��ȡsheet��ͷ
        sheet_title = ex.get_headers()
        result_index = sheet_title.index('result') + 1
        msg_index = sheet_title.index('msg') + 1
        code_index = sheet_title.index('code') + 1
        res_data_index = sheet_title.index('res_data') + 1

        # ��д
        ex.write(case_id + 1, msg_index, res_json['msg'])
        ex.write(case_id + 1, code_index, res_json['code'])
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

                # ��ȡ���ݿ����û���Ϣ
                user_info = get_user_info(member_id)
                self.assertEqual(user_info['mobile_phone'], res_json['data']['mobile_phone'])
                self.assertEqual(user_info['reg_name'], res_json['data']['reg_name'])
                self.assertEqual(user_info['type'], res_json['data']['type'])

                # �ȶ�ע��ʱ��
                reg_time = (user_info['reg_time']).strftime("%Y-%m-%d %H:%M:%S.0")
                self.assertEqual(reg_time, res_json['data']['reg_time'])

                # �ȶ� �˻����
                leave_amount = Decimal(user_info['leave_amount']).quantize(Decimal("0.00"))
                res_amount = Decimal(res_json['data']['leave_amount']).quantize(Decimal("0.00"))
                self.assertEqual(leave_amount, res_amount)
                ex.write(case_id + 1, result_index, "Pass")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
