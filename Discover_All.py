# coding=gbk

import os
import unittest
from datetime import datetime
from configuration.Path import path as pth
from libs.HTMLTestRunnerNew import HTMLTestRunner

# ��ʼ��
loader = unittest.TestLoader()

# �������������Զ��ռ���������
suite = loader.discover(start_dir=pth.test_path)

# ���Ա�������
file_name = datetime.now().strftime("%Y%m%d%H%M%S") + '.html'
file_path = os.path.join(pth.report_path, file_name)

# ����
with open(file_path, mode='wb') as f:
    runner = HTMLTestRunner(f,
                            title='ǰ�̴���Ŀ',
                            description='ע�ᡢ��¼����ֵ�����֡�Ͷ�ʡ������û��ǳơ�������Ŀ����ȡ�û���Ϣ',
                            tester='����',
                            verbosity=2)
    runner.run(suite)
