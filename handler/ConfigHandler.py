# coding=gbk

import os
from configparser import ConfigParser
from configuration.Path import path as pth
# from Future_Loans_Project.handler.LogHandler import log


class ConfigHandler:
    def __init__(self, filename, encoding='utf-8'):
        self.filename = filename
        self.encoding = encoding
        self.config = ConfigParser()
        self.config.read(self.filename, self.encoding)

    def get(self, section, option):
        """获取option值"""
        if self.has_section(section) and self.has_option(section, option):
            return self.config.get(section, option)
        # log.error(f"section:'{section}' or option:'{option}' not exist!")
        return None

    def set(self, section, option, value):
        """设置option值"""
        if self.has_section:
            self.config.set(section, option, value)
            self.save()
        # else:
            # log.error(f"section:'{section}'is not exist!")

    def add_section(self, section):
        """新增section"""
        if not self.has_section(section):
            self.config.add_section(section)
            self.save()
        # else:
        #     log.error(f"section:'{section}'has been existed!")

    def has_section(self, section):
        """判断section是否存在"""
        return self.config.has_section(section)

    def has_option(self, section, option):
        """判断option是否存在"""
        return self.config.has_option(section, option)

    def save(self):
        """保存"""
        with open(self.filename, mode='w', encoding=self.encoding) as f:
            self.config.write(f)


"""配置文件路径"""
config_file_path = os.path.join(pth.config_path, 'setting.ini')
"""初始化"""
config = ConfigHandler(config_file_path)


# if __name__ == '__main__':
#     url = config.get('excel', 'sheet1')
#     print(url)
