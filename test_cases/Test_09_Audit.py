# coding=gbk

import unittest
from libs.ddt import ddt, data
from handler.ExcelHandler_one import load_sheet
from handler.ConfigHandler import config
from handler.LogHandler import log
from handler.RequestsHandler import HttpSessionHandler
from helper.demo import deal
from helper.helper import login, is_register, get_loan_info

sheet = config.get('excel', 'audit_sheet')
ex = load_sheet(sheet)
test_data = ex.read()

# ��ȡ��ͨ�˺�
user = config.get('user', 'mobile_phone')
password = config.get('user', 'password')
is_register(user, password, typ=1)

# ��ȡ����Ա�˺�
admin = config.get('admin', 'mobile_phone')
pwd = config.get('admin', 'password')
is_register(admin, pwd, typ=0)


@ddt
class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = HttpSessionHandler()
        cls.url = config.get('api', 'base_url') + config.get('api', 'audit_url')
        cls.headers = eval(config.get('api', 'headers'))
        log.info(f'{cls.url}')

    @data(*test_data)
    def test_audit(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        expected = eval(case_data['expected'])

        # �������ݴ���
        ex_data = eval(deal(case_data['data']))
        mark_data = ex_data[0]
        json_data = ex_data[1]

        # ��¼
        if mark_data['type'] == 1:
            # ��ͨ�û���¼
            token_info = login(session=self.session, phone=user, pwd=password)
            self.headers['Authorization'] = token_info['token_type'] + ' ' + token_info['token']
        else:
            # ����Ա��¼
            token_info = login(session=self.session, phone=admin, pwd=pwd)
            self.headers['Authorization'] = token_info['token_type'] + ' ' + token_info['token']
            if mark_data['type'] == 'not_login':
                self.headers.pop('Authorization')

        # ��־��¼
        log.info(f'{self.headers}')
        log.info(f'{case_id},{method},{case_data["description"]},{json_data}')
        log.info(f'expected��{expected}')

        # ��������
        res_json = self.session.get_json(method=method, url=self.url, json=json_data, headers=self.headers)
        log.info(f'result:{res_json}\n')

        # ��ȡexcel_title
        excel_title = ex.get_headers()
        result_index = excel_title.index('result') + 1
        msg_index = excel_title.index('msg') + 1
        res_data_index = excel_title.index('res_data') + 1
        code_index = excel_title.index('code') + 1

        # ��дexcel
        ex.write(case_id + 1, code_index, res_json['code'])
        ex.write(case_id + 1, msg_index, res_json['msg'])

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
            loan_info = get_loan_info(loan_id=json_data['loan_id'])
            log.info(f'loan_info:{loan_info}\n')
            try:
                self.assertEqual(code, res_json['code'])
                self.assertEqual(expected['status'], loan_info['status'])
                self.assertEqual(expected['data'], res_json['data'])
                ex.write(case_id + 1, result_index, "Passed")
            except AssertionError as e:
                ex.write(case_id + 1, result_index, "Failed")
                raise e
            finally:
                ex.write(case_id + 1, res_data_index, str(res_json['data']))

