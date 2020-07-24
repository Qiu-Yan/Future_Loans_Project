# coding=gbk
import os
import unittest
from datetime import datetime
from configuration.Path import path as pth
from test_cases.Test_01_Register import TestRegister
from test_cases import Test_02_Login

# 初始化 loader
loader = unittest.TestLoader()

# 初始化 suite
suite = unittest.TestSuite()

# 根据测试用例 Test_class, 收集测试用例
suite_01 = loader.loadTestsFromTestCase(TestRegister)

# 根据测试模块  .py文件  收集测试用例
suite_02 = loader.loadTestsFromModule(Test_02_Login)

# 测试用例集
suite.addTests([suite_01, suite_02])

file_name = datetime.now().strftime("%Y%m%d%H%M%S") + '.txt'
file_path = os.path.join(pth.report_path, file_name)

with open(file_path, mode='w', encoding='utf-8') as f:
    runner = unittest.TextTestRunner(f, verbosity=2)
    f.write(f"""----------------------------------------------------------------------
标 题：前程贷项目
描 述：注册、登录功能
测试员：邱 燕
执行时间：{datetime.now()}
----------------------------------------------------------------------
""")
    runner.run(suite)
