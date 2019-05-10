#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
请求 Salve  创建实例子 配置主从
'''
import sys
import os
sys.path.append('/data0/scripts/devops/agent/')
import requests
from mysqldb import MysqlModel
import config
import sys
def httppost(url,datas):
    response = requests.post(url, data=datas)
    return response
master_unix=sys.argv[1]
master_ip=sys.argv[2]
master_port=sys.argv[3]
slave_ip=sys.argv[4]
slave_basedir=sys.argv[5]
slave_port =sys.argv[6]
try:
    data = MysqlModel('localhost', master_port, 'root', config.mysql_rootpass, master_unix).query('show master status')
    file = data[0][0]
    pos = data[0][1]
except Exception,e:
    os.system('python /data0/scripts/devops/agent/app/console/main.py mysqlog "配置数据库主从失败 master:%s slave:%s"' % (master_port, slave_port))
    exit()
url="http://%s:9999/api/create_slavehost/" %(slave_ip)
res = httppost(url,{'version':'5.6','slave_port':slave_port,'master_ip':master_ip,'master_port':master_port,'slave_basedir':slave_basedir,'slave_port':slave_port,'file':file,'pos':pos,'master_port':master_port})
os.system('/usr/bin/python /data0/scripts/devops/agent/console/main.py mysqlog "配置数据库主信息成功,正在安装部署从数据库 master:%s slave:%s pos:%s" %s' %(master_port,slave_port,pos,master_port))
