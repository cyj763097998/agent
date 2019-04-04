# coding: utf-8
# +-------------------------------------------------------------------
# | 258自动话运维系统
# +-------------------------------------------------------------------
# +-------------------------------------------------------------------
# | Author: 黄云建
# +-------------------------------------------------------------------

import MySQLdb, re
import config

class MysqlModel:
    __DB_PASS = None
    __DB_USER = 'root'
    __DB_PORT = 3306
    __DB_HOST = '127.0.0.1'
    __DB_CONN = None
    __DB_CUR = None
    __DB_ERR = None

    def __init__(self,hostip,port,username,password,sock=''):
        self.__DB_USER = username
        self.__DB_HOST = hostip
        self.__DB_PORT = int(port)
        self.__DB_PASS= password
        self.__DB_SOCK= sock
        self.__Conn()

    # 连接MYSQL数据库
    def __Conn(self):
        try:
            self.__DB_PASS = config.mysql_rootpass
            self.__DB_CONN = MySQLdb.connect(host=self.__DB_HOST, user=self.__DB_USER, passwd=self.__DB_PASS, db='mysql',unix_socket=self.__DB_SOCK)
            self.__DB_CUR = self.__DB_CONN.cursor()
            return True
        except MySQLdb.Error, e:
            self.__DB_ERR = str(e)
            return False

    def execute(self, sql):
        # 执行SQL语句返回受影响行
        if not self.__Conn(): return self.__DB_ERR
        try:
            result = self.__DB_CUR.execute(sql)
            self.__DB_CONN.commit()
            self.__Close()
            return result
        except Exception, ex:
            return "error: " + str(ex)

    def query(self, sql):
        # 执行SQL语句返回数据集
        if not self.__Conn(): return self.__DB_ERR
        try:
            self.__DB_CUR.execute(sql)
            result = self.__DB_CUR.fetchall()
            # 将元组转换成列表
            data = map(list, result)
            self.__Close()
            return data
        except Exception, ex:
            return "error: " + str(ex)

            # 关闭连接

    def __Close(self):
        self.__DB_CUR.close()
        self.__DB_CONN.close()