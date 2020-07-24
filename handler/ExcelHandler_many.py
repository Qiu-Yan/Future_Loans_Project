# coding=gbk

# pip install openpyxl
import os
from openpyxl import load_workbook
from configuration.Path import path as pth
from handler.LogHandler import log
from handler.ConfigHandler import config


class ExcelHandler:
    """适用于同时操作多个sheet页"""

    def __init__(self, filename):
        self.filename = filename

    def open(self, sheet_name):
        """加载工作簿"""
        try:
            self.wb = load_workbook(self.filename)
            if isinstance(sheet_name, str):
                self.sheet = self.wb[sheet_name]
            else:
                self.sheet = self.wb.worksheets[sheet_name]
        except Exception as e:
            log.error(e)
            raise e

    def get_headers(self, sheet):
        """获取sheet页，表头"""
        self.open(sheet)
        headers = [c.value for c in self.sheet[1]]
        self.wb.close()
        return headers

    def read(self, sheet, end_col=5):
        """读取数据，返回列表嵌套字典"""
        self.open(sheet)
        max_row = self.sheet.max_row
        data = []
        for row in range(2, max_row+1):         # 第二行开始读取
            row_data = {}
            for col in range(1, end_col+1):
                row_data[self.sheet.cell(1, col).value] = self.sheet.cell(row, col).value
            data.append(row_data)
        self.wb.close()
        return data

    def read_to_list(self, sheet, end_col=5):
        """读取数据，返回嵌套列表"""
        self.open(sheet)
        rows_data = list(self.sheet.rows)[1:]       # 获取所有行数据，不包括第一行
        data = []
        for row in rows_data:
            row_data = []
            for cell in row[:end_col]:
                row_data.append(cell.value)
            data.append(row_data)
        self.wb.close()
        return data

    def write(self, sheet, row, col, value):
        """写入数据"""
        self.open(sheet)
        self.sheet.cell(row, col).value = value
        self.save()

    def save(self):
        """保存并关闭"""
        self.wb.save(self.filename)
        self.wb.close()


file_name = config.get('excel', 'filename')
file_path = os.path.join(pth.data_path, file_name)

ex = ExcelHandler(filename=file_path)

if __name__ == '__main__':
    print(ex.write('login', 2, 6, 'xx'))
