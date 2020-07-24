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

# 读取测试数据
sheet = config.get('excel', 'register_sheet')
ex = load_sheet(sheet)
test_data = ex.read()


@ddt
class TestRegister(unittest.TestCase):
    # 获取接口地址
    url = config.get('api', 'base_url') + config.get('api', 'register_url')

    # 获取headers
    headers = eval(config.get('api', 'headers'))

    # 记录日志
    log.info(f'url:{url}, headers:{headers}')

    @classmethod
    def setUpClass(cls):
        cls.db = MySQLHandler()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    @data(*test_data)
    def test_register(self, case_data):
        # 获取请求方法
        method = case_data['method']
        # 获取json参数
        json_data = eval(case_data['data'])

        # 特殊数据处理
        if json_data['mobile_phone'] == 'new_phone':
            json_data['mobile_phone'] = new_phone()
        elif json_data['mobile_phone'] == 'old_phone':
            # json_data['mobile_phone'] = old_phone()           # 两种方式二选一
            json_data['mobile_phone'] = config.get('user', 'old_phone')

        # 发起请求, 返回的是dict类型
        res_json = request.get_json(method=method, url=self.url, json=json_data, headers=self.headers)

        # expected
        expected = eval(case_data['expected'])
        code = expected['code']

        # 日志记录
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
                # 回写到配置文件
                config.set('user', 'old_phone', json_data['mobile_phone'])

                # 比对预期结果，与 返回信息
                self.assertEqual(expected['data']['reg_name'], res_json['data']['reg_name'])
                self.assertEqual(json_data['mobile_phone'], res_json['data']['mobile_phone'])

                # 比对预期结果，与 数据库值
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

