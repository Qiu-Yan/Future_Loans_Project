# coding=gbk

import pymysql
from pymysql.cursors import DictCursor
from handler.LogHandler import log


class SQLHandler:
    def __init__(self, host, user, password, database, port=0, charset="utf8", cursor_class=DictCursor, **kwargs):
        # ��������
        self.connect = pymysql.connect(host=host,
                                       port=port,
                                       user=user,
                                       password=password,
                                       database=database,
                                       charset=charset,
                                       cursorclass=cursor_class,
                                       **kwargs)
        # ����cursor����
        self.cursor = self.connect.cursor()

    def fetchone(self, query, args=None):
        """��ȡ1������"""
        """
        sql     type:string  "select * from member where id=%s or mobile_phone=%s"
        args    type:list or tuple
                type: dict    %s ==>  %(name)s
        """
        try:
            self.connect.commit()   # ͬ������
            # ִ��SQL���
            self.cursor.execute(query=query, args=args)
            # ��ȡ���
            res = self.cursor.fetchone()
        except Exception as e:
            self.connect.rollback()     # �ع�
            log.error(e)
        else:
            return res

    def fetchall(self, query, args=None):
        """��ȡ��ѯ�������������"""
        try:
            self.connect.commit()
            self.cursor.execute(query=query, args=args)
            res = self.cursor.fetchall()
        except Exception as e:
            self.connect.rollback()
            log.error(e)
        else:
            return res

    def fetchmany(self, query, args=None, size=10):
        """��ȡ���ֲ�ѯ���"""
        try:
            self.connect.commit()
            self.cursor.execute(query=query, args=args)
            res = self.cursor.fetchmany(size)
        except Exception as e:
            self.connect.rollback()
            log.error(e)
        else:
            return res

    def execute(self, query, args=None):
        """ִ�и��²�����sql���"""
        try:
            # ִ�����
            self.cursor.execute(query=query, args=args)
            # �ύ
            self.connect.commit()
        except Exception as e:
            # �������쳣����ع�
            self.connect.rollback()
            log.error(e)

    def close(self):
        """ÿ������ִ����֮�󣬼ǵùرգ� teardown()"""
        """�ر��α�"""
        self.cursor.close()
        """�Ͽ�����"""
        self.connect.close()


class MySQLHandler(SQLHandler):
    """��ʼ��MySQLHandler���ݿ�"""
    def __init__(self, **kwargs):
        super().__init__(host="120.78.128.25",
                         port=3306,
                         user="future",
                         password="123456",
                         database="futureloan",
                         **kwargs)


if __name__ == "__main__":
    db = MySQLHandler()
