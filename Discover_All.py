# coding=gbk

import os
import unittest
from datetime import datetime
from configuration.Path import path as pth
from libs.HTMLTestRunnerNew import HTMLTestRunner

# 初始化
loader = unittest.TestLoader()

# 根据命名规则，自动收集测试用例
suite = loader.discover(start_dir=pth.test_path)

# 测试报告名称
file_name = datetime.now().strftime("%Y%m%d%H%M%S") + '.html'
file_path = os.path.join(pth.report_path, file_name)

# 运行
with open(file_path, mode='wb') as f:
    runner = HTMLTestRunner(f,
                            title='前程贷项目',
                            description='注册、登录、充值、提现、投资、更新用户昵称、新增项目、获取用户信息',
                            tester='邱燕',
                            verbosity=2)
    runner.run(suite)
