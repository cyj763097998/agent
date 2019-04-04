# -*- coding:utf-8 -*-
import config
import os
from .sqlitedb import Sql
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class MysqlHostToools(object):
    master_basedir=''#master数据库目录
    master_port=''#master数据库端口
    master_unix=''
    master_ip=''
    slave_ip = ''
    slave_basedir=''
    salve_port=''
    version=''
    master_script={
        '5.6':'%sscripts/server/mysql_gen_env_master' %(config.app_dir),
        '5.7':'%sscripts/server/mysql_gen_env_master_57' %(config.app_dir)
    }
    slave_script = {
        '5.6': '%sscripts/server/mysql_gen_env_slave' % (config.app_dir),
        '5.7': '%sscripts/server/mysql_gen_env_slave_57' % (config.app_dir)
    }
    def __init__(self,basedir,port):
        pass

    #创建master主机实例
    def create_masterhost(self,master_port,master_basedir,version):
        self.master_port = master_port
        self.master_basedir = master_basedir
        self.version = version
        self.master_unix = "%s/%s/mysql.sock" %(self.master_basedir,self.master_port)
        cmd='./gen.sh %s %s' %(self.master_port,self.master_basedir)
        pwd = self.master_script[self.version]
	#unicode 转码成utf-8
	cmd = cmd.encode('utf-8')
	task = '部署Master Mysql实例 %s/%s' % (self.master_basedir, self.master_port)
	task = task.encode('utf-8')
        #创建队列
        sql = Sql().dbfile("default")
        insert_data = (
           task, 'execshell', 0, time.time(), cmd, '',self.master_script[self.version])
        id = Sql().table('tasks').add('name,type,status,addtime,execstr,value,dir', insert_data)
        return id
    # 入队列slave主机实例
    def queue_slavehost(self,master_ip,slave_ip,slave_basedir,salve_port,version):
        #1 获取本实例 file pos
        #2 请求接口 实验部署 Slave mysql 实例
        #接口实现 http post请求队列 todo
        self.master_ip =master_ip
        self.slave_ip = slave_ip
        self.slave_basedir = slave_basedir
        self.salve_port= salve_port
        self.version = version
        cmd = 'python send_slave.py %s %s %s %s %s %s' % (self.master_unix, self.master_ip,self.master_port,self.slave_ip,self.slave_basedir,self.salve_port)
        pwd = self.master_script[self.version]
        #unicode 转码成utf-8
        cmd = cmd.encode('utf-8')
        task = '部署Master Mysql实例 %s/%s' % (self.master_basedir, self.master_port)
        task = task.encode('utf-8')
        # 创建队列
        sql = Sql().dbfile("default")
        insert_data = (
            task, 'execshell', 0, time.time(), cmd, '',self.master_script[self.version])
        id = Sql().table('tasks').add('name,type,status,addtime,execstr,value,dir', insert_data)
        return id
        pass

    # 创建Slave主机实例
    @staticmethod
    def create_slavehost(slave_port,slave_basedir,file,pos,master_port,master_ip,version):
        version
        cmd = './gen.sh %s %s %s %s %s %s' % (slave_port,slave_basedir,file,pos,master_ip,master_port)
        #unicode 转码成utf-8
        cmd = cmd.encode('utf-8')
        task = '部署Slave Mysql实例 %s/%s' % (slave_basedir,slave_port)
        task = task.encode('utf-8')
        # 创建队列
        slave_script = {
            '5.6': '%sscripts/server/mysql_gen_env_slave' % (config.app_dir),
            '5.7': '%sscripts/server/mysql_gen_env_slave_57' % (config.app_dir)
        }
        sql = Sql().dbfile("default")
        insert_data = (
            task, 'execshell', 0, time.time(), cmd, '',slave_script[version])
        id = Sql().table('tasks').add('name,type,status,addtime,execstr,value,dir', insert_data)
        return id
