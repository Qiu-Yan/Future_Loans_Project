# coding=gbk

import pymysql
from pymysql.cursors import DictCursor
from handler.LogHandler import log


class SQLHandler:
    def __init__(self, host, user, password, database, port=0, charset="utf8", cursor_class=DictCursor, **kwargs):
        # 建立连接
        self.connect = pymysql.connect(host=host,
                                       port=port,
                                       user=user,
                                       password=password,
                                       database=database,
                                       charset=charset,
                                       cursorclass=cursor_class,
                                       **kwargs)
        # 创建cursor对象
        self.cursor = self.connect.cursor()

    def fetchone(self, query, args=None):
        """获取1条数据"""
        """
        sql     type:string  "select * from member where id=%s or mobile_phone=%s"
        args    type:list or tuple
                type: dict    %s ==>  %(name)s
        """
        try:
            self.connect.commit()   # 同步数据
            # 执行SQL语句
            self.cursor.execute(query=query, args=args)
            # 获取结果
            res = self.cursor.fetchone()
        except Exception as e:
            self.connect.rollback()     # 回滚
            log.error(e)
        else:
            return res

    def fetchall(self, query, args=None):
        """获取查询结果的所有数据"""
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
        """获取部分查询结果"""
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
        """执行更新操作的sql语句"""
        try:
            # 执行语句
            self.cursor.execute(query=query, args=args)
            # 提交
            self.connect.commit()
        except Exception as e:
            # 若发送异常，则回滚
            self.connect.rollback()
            log.error(e)

    def close(self):
        """每次用例执行完之后，记得关闭， teardown()"""
        """关闭游标"""
        self.cursor.close()
        """断开连接"""
        self.connect.close()


class MySQLHandler(SQLHandler):
    """初始化MySQLHandler数据库"""
    def __init__(self, **kwargs):
        super().__init__(host="120.78.128.25",
                         port=3306,
                         user="future",
                         password="123456",
                         database="futureloan",
                         **kwargs)


if __name__ == "__main__":
    db = MySQLHandler()
