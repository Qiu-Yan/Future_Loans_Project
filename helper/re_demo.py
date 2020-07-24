# coding=gbk

import re
from handler.ConfigHandler import config
# from Future_Loans_Project.handler.LogHandler import log
from helper.helper import get_loan_info, get_invest_amount, get_leave_amount, change_amount

data = {"member_id": "9876", "my_loan": "876"}


# 方法一，不灵活
def data_deal(string):
    pattern = r'#(.+?)#'
    res = re.search(pattern=pattern, string=string)
    if res is not None:
        key = res.group(1)
        new_str = re.sub(pattern=pattern, repl=data[key], string=string, count=1)
        return data_deal(new_str)
    return string


# 方法二， 通过类实现
class RepData:
    member_id = config.get('user', 'member_id')
    other_id = str(eval(member_id) - 1)

    @property
    def loan_id(self):
        loan_info = get_loan_info(my=False)
        config.set('loan', 'loan_id', str(loan_info['id']))
        return str(loan_info['id'])

    @property
    def my_loan(self):
        loan_info = get_loan_info()
        return str(loan_info['id'])

    @property
    def not_start(self):
        loan_info = get_loan_info(my=False, status=1)
        return str(loan_info['id'])

    @property
    def full_loan(self):
        loan_info = get_loan_info(my=False, status=3)
        return str(loan_info['id'])

    @property
    def over_loan(self):
        """超过项目可投余额"""
        loan_amount = get_invest_amount(loan_id=config.get('loan', 'loan_id'))
        return str(float(loan_amount) + 100)

    @property
    def over_leave(self):
        """超过账户余额"""
        loan_amount = get_invest_amount(loan_id=config.get('loan', 'loan_id'))
        leave_amount = get_leave_amount(self.member_id)
        if loan_amount <= leave_amount:
            change_amount(self.member_id, amount=(float(loan_amount) - 100))
        return str(float(loan_amount))


def deal(string):
    string = str(string)
    rep_data = RepData()
    pattern = '#(.+?)#'
    while re.search(pattern, string):
        key = re.search(pattern, string).group(1)
        string = re.sub(pattern=pattern, repl=getattr(rep_data, key, ''), string=string, count=1)
    return string


if __name__ == '__main__':
    from Future_Loans_Project.handler.ExcelHandler_one import ExcelHandler

    ex = ExcelHandler('./cases_data.xlsx', 'test_property')
    test_data = ex.read(end_col=2)
    for case_data in test_data:
        data = deal(case_data['data'])
        print(data)

