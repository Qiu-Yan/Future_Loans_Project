# coding=gbk
import random
from decimal import Decimal
from handler.MySQLHandler import MySQLHandler
from handler.ConfigHandler import config
from handler.RequestsHandler import request
from handler.LogHandler import log


# db = MySQLHandler()


def make_phone_number():
    """生成电话号码"""
    phone = '1' + random.choice(['3', '5', '8']) + random.choice(['1', '2', '3', '5', '6', '7', '8', '9'])
    for i in range(8):
        num = str(random.randint(0, 9))
        phone = phone + num
    return phone


def new_phone():
    """随机生产新号码"""
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
    """数据库中已存在的电话号码"""
    db = MySQLHandler()
    sql = "select mobile_phone from member"
    res = db.fetchone(sql)
    phone = res['mobile_phone']
    db.close()
    return phone

#  ****************************************************************************************


def is_register(mobile_phone, password, typ=0):
    """判断管理员账号是否存在，不存在，则注册"""
    # 获取判断的账号信息
    # mobile_phone = config.get('admin', 'mobile_phone')
    # password = config.get('admin', 'password')

    # 连接数据库，查询数据
    db = MySQLHandler()
    sql = "select * from member where mobile_phone=%s;"
    user_info = db.fetchone(sql, [mobile_phone, ])
    db.close()
    # 若获取结果为空，则创建账户
    section = 'admin' if typ == 0 else 'user'
    if not user_info:
        register_url = config.get('api', 'base_url') + config.get('api', 'register_url')
        headers = eval(config.get('api', 'headers'))
        register_data = {"mobile_phone": mobile_phone, "pwd": password, "type": typ}
        register_json = request.get_json(method='post', url=register_url, json=register_data, headers=headers)
        if register_json['code'] == 0:
            config.set(section, 'member_id', str(register_json['data']['id']))           # 回写配置文件，user id
            log.info(f'用户[{mobile_phone}]注册成功!')
            return True
        log.debug(f'注册失败：{register_json}')
        return False
    config.set(section, 'member_id', str(user_info['id']))   # 回写配置文件，user id
    return None


def is_register_1():
    """判断普通用户账号是否存在，不存在，则注册"""
    # 获取判断的账号信息
    mobile_phone = config.get('user', 'mobile_phone')
    password = config.get('user', 'password')

    # 连接数据库，查询数据
    db = MySQLHandler()
    sql = "select * from member where mobile_phone=%s;"
    user_info = db.fetchone(sql, [mobile_phone, ])
    db.close()
    # 若获取结果为空，则创建账户
    if not user_info:
        register_url = config.get('api', 'base_url') + config.get('api', 'register_url')
        headers = eval(config.get('api', 'headers'))
        register_data = {"mobile_phone": mobile_phone, "pwd": password, "type": 1}
        register_json = request.get_json(method='post', url=register_url, json=register_data, headers=headers)
        if register_json['code'] == 0:
            config.set('user', 'member_id', str(register_json['data']['id']))           # 回写配置文件，user id
            log.info(f'用户[{mobile_phone}]注册成功!')
            return True
        log.debug(f'注册失败：{register_json}')
        return False
    config.set('user', 'member_id', str(user_info['id']))   # 回写配置文件，user id
    return None


def login(session, phone, pwd):
    """登录"""
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
            log.info(f'用户{[mobile_phone]}登录成功！')
            return login_json['data']['token_info']
        else:
            log.info(f'用户{[mobile_phone]}登录失败！')
            return None


def login_1(session):
    """登录"""
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
            log.info(f'用户{[mobile_phone]}登录成功！')
            return login_json['data']['token_info']
        else:
            log.info(f'用户{[mobile_phone]}登录失败！')
            return None


def add_loan():
    """新增并审核项目"""
    add_data = {"member_id": config.get("user", 'member_id'), "title": "小荔枝",
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
        log.info('项目新增成功')
        """项目新增成功，审核项目"""
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
            log.info(f"{add_res['data']['id']}项目审核成功")
            return None
        log.error(f"{add_res['data']['id']}项目审核失败")
        return None
    log.error('新增项目失败')
    return None


# ************************************************************************************************


def get_leave_amount(member_id):
    """查余额"""
    db = MySQLHandler()
    sql = "select * from member where id=%s"
    user_info = db.fetchone(query=sql, args=[member_id, ])
    db.close()
    return Decimal(user_info['leave_amount']).quantize(Decimal("0.00"))


def get_user_info(member_id):
    """查询用户信息"""
    db = MySQLHandler()
    sql = "select * from member where id=%s;"
    user_info = db.fetchone(query=sql, args=[member_id, ])
    db.close()
    return user_info


def get_loan_info(my=True, status=2, loan_id=None):
    """查询项目信息, 项目状态status=(1, 2, 3, 4, 5), 1:审核中 2:竞标中 3:还款中 4:还款完成 5:审核不通过 """
    member_id = config.get('user', 'member_id')
    db = MySQLHandler()
    if loan_id is not None:
        """根据项目id 查询项目信息"""
        sql = "select * from loan where id=%s;"
        loan_info = db.fetchone(query=sql, args=[loan_id, ])
    elif my:
        """查询测试账号下的项目信息"""
        sql = "select * from loan where member_id=%s and status=%s;"
        loan_info = db.fetchone(query=sql, args=[member_id, status])
    else:
        """查询其他用户的项目信息"""
        sql = "select * from loan where member_id!=%s and status=%s;"
        loan_info = db.fetchone(query=sql, args=[member_id, status])
    db.close()
    return loan_info


def get_invest_info(invest_id=None, loan_id=None):
    """查询投资记录"""
    db = MySQLHandler()
    if invest_id is not None:
        """根据投资记录id查询投资信息"""
        sql = 'select * from invest where id=%s;'
        invest_info = db.fetchone(query=sql, args=[invest_id, ])
        db.close()
        return invest_info
    elif loan_id is not None:
        """项目项目id查询 已投金额"""
        sql = 'select amount from invest where loan_id=%s;'
        invested_amount = db.fetchall(query=sql, args=[loan_id, ])
        db.close()
        return invested_amount
    db.close()
    log.error('未传入查询参数！')
    return None


def get_invest_amount(loan_id):
    """获取项目 剩余可投余额"""
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
#     """充值"""
#     # 获取账户余额
#     leave_amount = get_leave_amount(member_id)
#     # 若账户余额 大于等于 60万，则返回余额
#     if leave_amount >= 600000.00:
#         return leave_amount
#     else:
#         # 账户余额 小于60万，则充值，保证账户有60万余额，充值成功，返回余额
#         amount = float(600000 - leave_amount)                     # 差额
#         # 充值接口
#         recharge_url = config.get('api', 'base_url') + config.get('api', 'recharge_url')
#         # 充值参数
#         json_data = {"member_id": member_id, "amount": amount}
#         # 充值
#         recharge_json = session.get_json(method='post', url=recharge_url, json=json_data, headers=headers)
#
#         if recharge_json['code'] == 0:
#             log.info('充值成功！')
#             return Decimal(recharge_json['data'][leave_amount]).quantize(Decimal('0.00'))
#         else:
#             log.error("充值失败！")


def change_amount(member_id, amount):
    """修改账户余额"""
    db = MySQLHandler()
    sql = "update member set leave_amount=%s where id=%s;"
    db.execute(query=sql, args=[amount, member_id])
    db.close()


if __name__ == "__main__":
    add_loan()
    print()
