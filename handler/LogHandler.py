# coding=gbk

import os
import logging
from datetime import datetime
from handler.ConfigHandler import config
from configuration.Path import path as pth


class LogHandler:
    """����
    NOTSET          0��
    DEBUG           10��
    INFO            20��
    WARNING         30��
    ERROR           40��
    CRITICAL        50��
    """
    def __init__(self, name=None, level='DEBUG', filename='', handler_level='DEBUG', encoding='utf-8'):
        """��ʼ����־�ռ���"""
        self.logger = logging.getLogger(name)
        """������־�ռ�������"""
        self.logger.setLevel(level=level)

        """��ʼ��������output"""
        if filename == '':
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(filename=filename, mode='a', encoding=encoding)
        """���ô���������"""
        handler.setLevel(handler_level)
        """�ռ��� ��� ������"""
        self.logger.addHandler(handler)

        """�����ʽ"""
        fmt_str = "[%(levelname)s]%(asctime)s-%(filename)s-%(lineno)d: %(message)s"
        # "%(asctime)s-%(name)s-%(filename)s-%(lineno)d-%(levelname)s: %(message)s"
        """��ʼ����ʽ��"""
        fmt = logging.Formatter(fmt_str)
        """���������������ʽ"""
        handler.setFormatter(fmt)


"""��ȡ�����ļ�����Ӧֵ"""
logger_name = config.get('Logger', 'name')
logger_level = config.get('Logger', 'level')
hdr_level = config.get('Logger', 'hdr_level')

"""log�ļ�����"""
log_name = "log_" + datetime.now().strftime("%Y%m%d") + ".txt"
"""log�ļ�·��"""
file_name = os.path.join(pth.log_path, log_name)

"""��ʼ����־�ռ���"""
logger = LogHandler(name=logger_name,
                    level=logger_level,
                    filename=file_name,
                    handler_level=hdr_level)

"""log.info()"""
log = logger.logger


# if __name__ == '__main__':
#     log.error('log-testing')
