# coding=gbk

# import os
import unittest
from libs.ddt import ddt, data
from handler.ExcelHandler_one import load_sheet
from handler.ConfigHandler import config
from handler.LogHandler import log
from handler.RequestsHandler import request
from handler.MySQLHandler import MySQLHandler
from helper.helper import new_phone, old_phone

# ��ȡ��������
sheet = config.get('excel', 'register_sheet')
ex = load_sheet(sheet)
test_data = ex.read()


@ddt
class TestRegister(unittest.TestCase):
    # ��ȡ�ӿڵ�ַ
    url = config.get('api', 'base_url') + config.get('api', 'register_url')

    # ��ȡheaders
    headers = eval(config.get('api', 'headers'))

    # ��¼��־
    log.info(f'url:{url}, headers:{headers}')

    @classmethod
    def setUpClass(cls):
        cls.db = MySQLHandler()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    @data(*test_data)
    def test_register(self, case_data):
        # ��ȡ���󷽷�
        method = case_data['method']
        # ��ȡjson����
        json_data = eval(case_data['data'])

        # �������ݴ���
        if json_data['mobile_phone'] == 'new_phone':
            json_data['mobile_phone'] = new_phone()
        elif json_data['mobile_phone'] == 'old_phone':
            # json_data['mobile_phone'] = old_phone()           # ���ַ�ʽ��ѡһ
            json_data['mobile_phone'] = config.get('user', 'old_phone')

        # ��������, ���ص���dict����
        res_json = request.get_json(method=method, url=self.url, json=json_data, headers=self.headers)

        # expected
        expected = eval(case_data['expected'])
        code = expected['code']

        # ��־��¼
        case_id = case_data['case_id']
        description = case_data['description']
        log.info(f"{case_id},{method},{description},{json_data}")
        log.info(f"expected:{expected}")
        log.info(f"result:{res_json}\n")

        sheet_title = ex.get_headers()
        ex.write(case_id+1, sheet_title.index('msg')+1, res_json['msg'])
        ex.write(case_id+1, sheet_title.index('code')+1, str(res_json['code']))
        ex.write(case_id+1, sheet_title.index('res_data')+1, str(res_json['data']))

        if code != 0:
            try:
                self.assertEqual(code, res_json['code'])
                self.assertEqual(expected['data'], res_json['data'])
                ex.write(case_id+1, sheet_title.index('result')+1, 'Pass')
            except AssertionError as e:
                ex.write(case_id+1, sheet_title.index('result')+1, 'Failed')
                raise e
        else:
            try:
                self.assertEqual(code, res_json['code'])
                # ��д�������ļ�
                config.set('user', 'old_phone', json_data['mobile_phone'])

                # �ȶ�Ԥ�ڽ������ ������Ϣ
                self.assertEqual(expected['data']['reg_name'], res_json['data']['reg_name'])
                self.assertEqual(json_data['mobile_phone'], res_json['data']['mobile_phone'])

                # �ȶ�Ԥ�ڽ������ ���ݿ�ֵ
                sql = "select * from member where id=%s;"
                user_info = self.db.fetchone(query=sql, args=[res_json['data']['id'], ])

                log.info(f'user_info:{user_info}\n')

                self.assertEqual(expected['data']['reg_name'], user_info['reg_name'])
                self.assertEqual(json_data['mobile_phone'], user_info['mobile_phone'])
                self.assertEqual(expected['data']['type'], user_info['type'])
                self.assertEqual(expected['data']['leave_amount'], user_info['leave_amount'])
                ex.write(case_id+1, sheet_title.index('result')+1, 'Pass')
            except AssertionError as e:
                ex.write(case_id+1, sheet_title.index('result')+1, 'Failed')
                raise e

