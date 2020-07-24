# coding=gbk

import os
import logging
from datetime import datetime
from handler.ConfigHandler import config
from configuration.Path import path as pth


class LogHandler:
    """级别
    NOTSET          0级
    DEBUG           10级
    INFO            20级
    WARNING         30级
    ERROR           40级
    CRITICAL        50级
    """
    def __init__(self, name=None, level='DEBUG', filename='', handler_level='DEBUG', encoding='utf-8'):
        """初始化日志收集器"""
        self.logger = logging.getLogger(name)
        """设置日志收集器级别"""
        self.logger.setLevel(level=level)

        """初始化处理器output"""
        if filename == '':
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(filename=filename, mode='a', encoding=encoding)
        """设置处理器级别"""
        handler.setLevel(handler_level)
        """收集器 添加 处理器"""
        self.logger.addHandler(handler)

        """输出格式"""
        fmt_str = "[%(levelname)s]%(asctime)s-%(filename)s-%(lineno)d: %(message)s"
        # "%(asctime)s-%(name)s-%(filename)s-%(lineno)d-%(levelname)s: %(message)s"
        """初始化格式器"""
        fmt = logging.Formatter(fmt_str)
        """处理器设置输出格式"""
        handler.setFormatter(fmt)


"""读取配置文件中相应值"""
logger_name = config.get('Logger', 'name')
logger_level = config.get('Logger', 'level')
hdr_level = config.get('Logger', 'hdr_level')

"""log文件名称"""
log_name = "log_" + datetime.now().strftime("%Y%m%d") + ".txt"
"""log文件路径"""
file_name = os.path.join(pth.log_path, log_name)

"""初始化日志收集器"""
logger = LogHandler(name=logger_name,
                    level=logger_level,
                    filename=file_name,
                    handler_level=hdr_level)

"""log.info()"""
log = logger.logger


# if __name__ == '__main__':
#     log.error('log-testing')
