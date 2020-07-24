# coding=gbk

import unittest
from libs.ddt import ddt, data
from handler.ExcelHandler_one import load_sheet
from handler.ConfigHandler import config
from handler.LogHandler import log
from handler.RequestsHandler import request
from handler.MySQLHandler import MySQLHandler
from helper.helper import old_phone, is_register_1


"""��ȡlogin������"""
sheet = config.get('excel', 'login_sheet')
ex = load_sheet(sheet)
test_data = ex.read()

"""��¼�û���Ϣ"""
mobile_phone = config.get('user', 'mobile_phone')
password = config.get('user', 'password')

# �ж��û���Ϣ�Ƿ���ڣ������ڣ��򴴽�
is_register_1()


@ddt
class TestLogin(unittest.TestCase):
    # login �ӿڵ�ַ
    url = config.get('api', 'base_url') + config.get('api', 'login_url')
    headers = eval(config.get('api', 'headers'))

    # ��־��¼
    log.info(f'{url}, {headers}')

    @classmethod
    def setUpClass(cls):
        cls.db = MySQLHandler()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    @data(*test_data)
    def test_login(self, case_data):
        case_id = case_data['case_id']
        method = case_data['method']
        description = case_data['description']
        dic_data = eval(case_data['data'])
        expected = eval(case_data['expected'])

        # ������������
        if dic_data['mobile_phone'] == 'phone_num':
            dic_data['mobile_phone'] = mobile_phone
        elif dic_data['mobile_phone'] == 'wrong_phone':
            # dic_data['mobile_phone'] = old_phone()
            dic_data['mobile_phone'] = config.get('user', 'old_phone')

        if dic_data['pwd'] == 'password':
            dic_data['pwd'] = password
        elif dic_data['pwd'] == 'wrong_pwd':
            dic_data['pwd'] = password + 'w'

        # ��������
        res_json = request.get_json(method=method, url=self.url, json=dic_data, headers=self.headers)

        # ��־��¼
        log.info(f'{case_id},{method},{description},{dic_data}')
        log.info(f'expected:{expected}')
        log.info(f'result:{res_json}\n')

        # ��ȡ��ͷ
        sheet_title = ex.get_headers()
        result_index = sheet_title.index("result")+1
        msg_index = sheet_title.index('msg')+1
        code_index = sheet_title.index('code')+1
        res_data_index = sheet_title.index('res_data')+1

        # ��д
        ex.write(case_id + 1, msg_index, res_json['msg'])
        ex.write(case_id + 1, code_index, str(res_json['code']))
        ex.write(case_id + 1, res_data_index, str(res_json['data']))

        code = expected['code']
        if code != 0:
            try:
                self.assertEqual(code, res_json['code'])
                self.assertEqual(expected['data'], res_json['data'])
                ex.write(case_id+1, result_index, 'Pass')
            except AssertionError as e:
                ex.write(case_id + 1, result_index, 'Failed')
                raise e
        else:
            try:
                self.assertEqual(code, res_json['code'])

                # ���ݿ���Ϣ �� ������Ϣ�ȶ�
                sql = "select * from member where id=%s;"
                user_info = self.db.fetchone(query=sql, args=[res_json['data']['id'], ])
                self.assertEqual(user_info['leave_amount'], res_json['data']['leave_amount'])
                self.assertEqual(user_info['mobile_phone'], res_json['data']['mobile_phone'])
                self.assertEqual(user_info['reg_name'], res_json['data']['reg_name'])
                self.assertEqual(user_info['type'], res_json['data']['type'])
                self.assertTrue(True, res_json['data']['token_info'])
                ex.write(case_id + 1, result_index, 'Pass')
            except AssertionError as e:
                ex.write(case_id + 1, result_index, 'Failed')
                raise e
