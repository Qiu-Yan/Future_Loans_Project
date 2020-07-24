# coding=gbk

import re
# from Future_Loans_Project.handler.ConfigHandler import config
from handler.MySQLHandler import MySQLHandler


class AuditData:
    db = MySQLHandler()
    # 获取3个项目信息
    sql = 'select id from loan where status=1'
    loans = db.fetchmany(query=sql, size=3)
    db.close()
    # for i, loan in enumerate(loans):
    #     config.set('audit', 'loan_' + str(i + 1), str(loan['id']))
    # loan_1 = config.get('audit', 'loan_1')
    # loan_2 = config.get('audit', 'loan_2')
    # loan_3 = config.get('audit', 'loan_3')
    loan_1 = str(loans[0]['id'])
    loan_2 = str(loans[1]['id'])
    loan_3 = str(loans[2]['id'])

    @property
    def wloan_2(self):
        db = MySQLHandler()
        sql = 'select id from loan where status=2'
        loan_id = db.fetchone(query=sql)
        db.close()
        return str(loan_id['id'])

    @property
    def wloan_3(self):
        db = MySQLHandler()
        sql = 'select id from loan where status=3'
        loan_id = db.fetchone(query=sql)
        db.close()
        return str(loan_id['id'])

    @property
    def wloan_4(self):
        db = MySQLHandler()
        sql = 'select id from loan where status=4'
        loan_id = db.fetchone(query=sql)
        db.close()
        return str(loan_id['id'])

    @property
    def wloan_5(self):
        db = MySQLHandler()
        sql = 'select id from loan where status=5'
        loan_id = db.fetchone(query=sql)
        db.close()
        return str(loan_id['id'])


def deal(string):
    ad = AuditData()
    string = str(string)
    pattern = r'#(\w+?)#'
    while re.search(pattern=pattern, string=string):
        key = re.search(pattern=pattern, string=string).group(1)
        string = re.sub(pattern=pattern, repl=getattr(ad, key, ""), string=string)
    return string


if __name__ == "__main__":
    print(deal('{"loan_id":#loan_1#, "approved_or_not":"false"}'))
