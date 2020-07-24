# coding=gbk

from helper.helper import get_leave_amount, get_loan_info, change_amount, get_invest_amount
from handler.ConfigHandler import config
from handler.LogHandler import log


def invest_json_data(data):
    if isinstance(data, dict):
        member_id = eval(config.get('user', 'member_id'))
        if data['member_id'] == 'id':
            data['member_id'] = member_id
        elif data['member_id'] == 'other_id':
            data['member_id'] = member_id - 1

        if data['loan_id'] == 'id':
            loan_info = get_loan_info(my=False)
            data['loan_id'] = loan_info['id']
        elif data['loan_id'] == 'my_loan':
            loan_info = get_loan_info()
            data['loan_id'] = loan_info['id']
        elif data['loan_id'] == 'not_start':
            loan_info = get_loan_info(my=False, status=1)
            data['loan_id'] = loan_info['id']
        elif data['loan_id'] == 'full':
            loan_info = get_loan_info(my=False, status=3)
            data['loan_id'] = loan_info['id']

        if data['amount'] == 'over_loan':
            """超过项目可投余额"""
            loan_amount = get_invest_amount(loan_id=data['loan_id'])
            data['amount'] = float(loan_amount) + 100
        elif data['amount'] == 'over_leave':
            """超过账户余额"""
            loan_amount = get_invest_amount(loan_id=data['loan_id'])
            leave_amount = get_leave_amount(data['member_id'])
            if loan_amount <= leave_amount:
                change_amount(member_id, amount=(float(loan_amount)-100))
            data['amount'] = float(loan_amount)
    else:
        log.error('传入的数据不是字典类型！')
    return data
