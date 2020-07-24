# coding=gbk
import random
from decimal import Decimal
from handler.MySQLHandler import MySQLHandler
from handler.ConfigHandler import config
from handler.RequestsHandler import request
from handler.LogHandler import log


# db = MySQLHandler()


def make_phone_number():
    """���ɵ绰����"""
    phone = '1' + random.choice(['3', '5', '8']) + random.choice(['1', '2', '3', '5', '6', '7', '8', '9'])
    for i in range(8):
        num = str(random.randint(0, 9))
        phone = phone + num
    return phone


def new_phone():
    """��������º���"""
    db = MySQLHandler()
    while True:
        phone = make_phone_number()
        sql = "select * from member where mobile_phone=%s;"
        res = db.fetchone(query=sql, args=[phone, ])
        if not res:
            break
    db.close()
    return phone


def old_phone():
    """���ݿ����Ѵ��ڵĵ绰����"""
    db = MySQLHandler()
    sql = "select mobile_phone from member"
    res = db.fetchone(sql)
    phone = res['mobile_phone']
    db.close()
    return phone

#  ****************************************************************************************


def is_register(mobile_phone, password, typ=0):
    """�жϹ���Ա�˺��Ƿ���ڣ������ڣ���ע��"""
    # ��ȡ�жϵ��˺���Ϣ
    # mobile_phone = config.get('admin', 'mobile_phone')
    # password = config.get('admin', 'password')

    # �������ݿ⣬��ѯ����
    db = MySQLHandler()
    sql = "select * from member where mobile_phone=%s;"
    user_info = db.fetchone(sql, [mobile_phone, ])
    db.close()
    # ����ȡ���Ϊ�գ��򴴽��˻�
    section = 'admin' if typ == 0 else 'user'
    if not user_info:
        register_url = config.get('api', 'base_url') + config.get('api', 'register_url')
        headers = eval(config.get('api', 'headers'))
        register_data = {"mobile_phone": mobile_phone, "pwd": password, "type": typ}
        register_json = request.get_json(method='post', url=register_url, json=register_data, headers=headers)
        if register_json['code'] == 0:
            config.set(section, 'member_id', str(register_json['data']['id']))           # ��д�����ļ���user id
            log.info(f'�û�[{mobile_phone}]ע��ɹ�!')
            return True
        log.debug(f'ע��ʧ�ܣ�{register_json}')
        return False
    config.set(section, 'member_id', str(user_info['id']))   # ��д�����ļ���user id
    return None


def is_register_1():
    """�ж���ͨ�û��˺��Ƿ���ڣ������ڣ���ע��"""
    # ��ȡ�жϵ��˺���Ϣ
    mobile_phone = config.get('user', 'mobile_phone')
    password = config.get('user', 'password')

    # �������ݿ⣬��ѯ����
    db = MySQLHandler()
    sql = "select * from member where mobile_phone=%s;"
    user_info = db.fetchone(sql, [mobile_phone, ])
    db.close()
    # ����ȡ���Ϊ�գ��򴴽��˻�
    if not user_info:
        register_url = config.get('api', 'base_url') + config.get('api', 'register_url')
        headers = eval(config.get('api', 'headers'))
        register_data = {"mobile_phone": mobile_phone, "pwd": password, "type": 1}
        register_json = request.get_json(method='post', url=register_url, json=register_data, headers=headers)
        if register_json['code'] == 0:
            config.set('user', 'member_id', str(register_json['data']['id']))           # ��д�����ļ���user id
            log.info(f'�û�[{mobile_phone}]ע��ɹ�!')
            return True
        log.debug(f'ע��ʧ�ܣ�{register_json}')
        return False
    config.set('user', 'member_id', str(user_info['id']))   # ��д�����ļ���user id
    return None


def login(session, phone, pwd):
    """��¼"""
    mobile_phone = phone
    password = pwd

    login_url = config.get('api', 'base_url') + config.get('api', 'login_url')
    headers = eval(config.get('api', 'headers'))
    login_data = {"mobile_phone": mobile_phone, "pwd": password}
    try:
        login_json = session.get_json(method='post', url=login_url, json=login_data, headers=headers)
    except Exception as e:
        log.error(e)
    else:
        if login_json['code'] == 0:
            log.info(f'�û�{[mobile_phone]}��¼�ɹ���')
            return login_json['data']['token_info']
        else:
            log.info(f'�û�{[mobile_phone]}��¼ʧ�ܣ�')
            return None


def login_1(session):
    """��¼"""
    mobile_phone = config.get('user', 'mobile_phone')
    password = config.get('user', 'password')

    login_url = config.get('api', 'base_url') + config.get('api', 'login_url')
    headers = eval(config.get('api', 'headers'))
    login_data = {"mobile_phone": mobile_phone, "pwd": password}
    try:
        login_json = session.get_json(method='post', url=login_url, json=login_data, headers=headers)
    except Exception as e:
        log.error(e)
    else:
        if login_json['code'] == 0:
            log.info(f'�û�{[mobile_phone]}��¼�ɹ���')
            return login_json['data']['token_info']
        else:
            log.info(f'�û�{[mobile_phone]}��¼ʧ�ܣ�')
            return None


def add_loan():
    """�����������Ŀ"""
    add_data = {"member_id": config.get("user", 'member_id'), "title": "С��֦",
            "amount": 3000, "loan_rate": 3.2, "loan_term": 1, "loan_date_type": 1, "bidding_days": 1}
    headers = eval(config.get('api', 'headers'))
    token_info = login_1(session=request)
    token = token_info['token_type'] + ' ' + token_info['token']
    headers['Authorization'] = token
    add_res = request.get_json(method='post',
                               url=config.get('api', 'base_url') + config.get('api', 'add_url'),
                               json=add_data,
                               headers=headers)
    if add_res['code'] == 0:
        log.info('��Ŀ�����ɹ�')
        """��Ŀ�����ɹ��������Ŀ"""
        admin = config.get('admin', 'mobile_phone')
        pwd = config.get('admin', 'password')
        is_register(admin, pwd, typ=0)
        audit_data = {"loan_id": add_res['data']['id'], "approved_or_not": "true"}
        token_info = login(session=request, phone=admin, pwd=pwd)
        headers['Authorization'] = token_info['token_type'] + ' ' + token_info['token']
        audit_res = request.get_json(method='PATCH',
                                     url=config.get('api', 'base_url') + config.get('api', 'audit_url'),
                                     json=audit_data,
                                     headers=headers)
        if audit_res['code'] == 0:
            log.info(f"{add_res['data']['id']}��Ŀ��˳ɹ�")
            return None
        log.error(f"{add_res['data']['id']}��Ŀ���ʧ��")
        return None
    log.error('������Ŀʧ��')
    return None


# ************************************************************************************************


def get_leave_amount(member_id):
    """�����"""
    db = MySQLHandler()
    sql = "select * from member where id=%s"
    user_info = db.fetchone(query=sql, args=[member_id, ])
    db.close()
    return Decimal(user_info['leave_amount']).quantize(Decimal("0.00"))


def get_user_info(member_id):
    """��ѯ�û���Ϣ"""
    db = MySQLHandler()
    sql = "select * from member where id=%s;"
    user_info = db.fetchone(query=sql, args=[member_id, ])
    db.close()
    return user_info


def get_loan_info(my=True, status=2, loan_id=None):
    """��ѯ��Ŀ��Ϣ, ��Ŀ״̬status=(1, 2, 3, 4, 5), 1:����� 2:������ 3:������ 4:������� 5:��˲�ͨ�� """
    member_id = config.get('user', 'member_id')
    db = MySQLHandler()
    if loan_id is not None:
        """������Ŀid ��ѯ��Ŀ��Ϣ"""
        sql = "select * from loan where id=%s;"
        loan_info = db.fetchone(query=sql, args=[loan_id, ])
    elif my:
        """��ѯ�����˺��µ���Ŀ��Ϣ"""
        sql = "select * from loan where member_id=%s and status=%s;"
        loan_info = db.fetchone(query=sql, args=[member_id, status])
    else:
        """��ѯ�����û�����Ŀ��Ϣ"""
        sql = "select * from loan where member_id!=%s and status=%s;"
        loan_info = db.fetchone(query=sql, args=[member_id, status])
    db.close()
    return loan_info


def get_invest_info(invest_id=None, loan_id=None):
    """��ѯͶ�ʼ�¼"""
    db = MySQLHandler()
    if invest_id is not None:
        """����Ͷ�ʼ�¼id��ѯͶ����Ϣ"""
        sql = 'select * from invest where id=%s;'
        invest_info = db.fetchone(query=sql, args=[invest_id, ])
        db.close()
        return invest_info
    elif loan_id is not None:
        """��Ŀ��Ŀid��ѯ ��Ͷ���"""
        sql = 'select amount from invest where loan_id=%s;'
        invested_amount = db.fetchall(query=sql, args=[loan_id, ])
        db.close()
        return invested_amount
    db.close()
    log.error('δ�����ѯ������')
    return None


def get_invest_amount(loan_id):
    """��ȡ��Ŀ ʣ���Ͷ���"""
    invested = get_invest_info(loan_id=loan_id)
    loan_info = get_loan_info(loan_id=loan_id)
    loan_amount = Decimal(loan_info['amount']).quantize(Decimal("0.00"))
    if invested is not None:
        total = 0
        for index in invested:
            total += index['amount']
        amount = Decimal(loan_amount - total).quantize(Decimal("0.00"))
        return amount
    return loan_amount


# def recharge(session, headers, member_id):
#     """��ֵ"""
#     # ��ȡ�˻����
#     leave_amount = get_leave_amount(member_id)
#     # ���˻���� ���ڵ��� 60���򷵻����
#     if leave_amount >= 600000.00:
#         return leave_amount
#     else:
#         # �˻���� С��60�����ֵ����֤�˻���60������ֵ�ɹ����������
#         amount = float(600000 - leave_amount)                     # ���
#         # ��ֵ�ӿ�
#         recharge_url = config.get('api', 'base_url') + config.get('api', 'recharge_url')
#         # ��ֵ����
#         json_data = {"member_id": member_id, "amount": amount}
#         # ��ֵ
#         recharge_json = session.get_json(method='post', url=recharge_url, json=json_data, headers=headers)
#
#         if recharge_json['code'] == 0:
#             log.info('��ֵ�ɹ���')
#             return Decimal(recharge_json['data'][leave_amount]).quantize(Decimal('0.00'))
#         else:
#             log.error("��ֵʧ�ܣ�")


def change_amount(member_id, amount):
    """�޸��˻����"""
    db = MySQLHandler()
    sql = "update member set leave_amount=%s where id=%s;"
    db.execute(query=sql, args=[amount, member_id])
    db.close()


if __name__ == "__main__":
    add_loan()
    print()
