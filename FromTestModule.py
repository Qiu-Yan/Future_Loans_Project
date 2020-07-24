# coding=gbk
import os
import unittest
from datetime import datetime
from configuration.Path import path as pth
from test_cases.Test_01_Register import TestRegister
from test_cases import Test_02_Login

# ��ʼ�� loader
loader = unittest.TestLoader()

# ��ʼ�� suite
suite = unittest.TestSuite()

# ���ݲ������� Test_class, �ռ���������
suite_01 = loader.loadTestsFromTestCase(TestRegister)

# ���ݲ���ģ��  .py�ļ�  �ռ���������
suite_02 = loader.loadTestsFromModule(Test_02_Login)

# ����������
suite.addTests([suite_01, suite_02])

file_name = datetime.now().strftime("%Y%m%d%H%M%S") + '.txt'
file_path = os.path.join(pth.report_path, file_name)

with open(file_path, mode='w', encoding='utf-8') as f:
    runner = unittest.TextTestRunner(f, verbosity=2)
    f.write(f"""----------------------------------------------------------------------
�� �⣺ǰ�̴���Ŀ
�� ����ע�ᡢ��¼����
����Ա���� ��
ִ��ʱ�䣺{datetime.now()}
----------------------------------------------------------------------
""")
    runner.run(suite)
