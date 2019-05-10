#/usr/bin/env python
#coding=utf-8
#edit richard  2019/3/14

from . import opman
from flask import render_template, url_for, redirect,flash,session,request,abort,Response,jsonify
from .common import success,error
from utils.mysql_host_tools import MysqlHostToools
#from forms import LoginForm,PwdForm,TagForm,AuthForm,RoleForm,AdminForm
#from app.models import Admin,Tag,Auth,Role
#from functools import wraps
#from app import db
#import datetime
@opman.route("/api/create_masterhost",methods=["POST"])
def create_masterhost():
    master_dir = request.form.get('master_dir')
    master_port = request.form.get('master_port')
    slave_dir = request.form.get('slave_dir')
    slave_port = request.form.get('slave_port')
    version = request.form.get('version')
    if int(version) == 1:
        version = "5.6"
    else:
        version = "5.7"
    master_id = request.form.get('master_id')
    slave_id = request.form.get('slave_id')

    # 判断实例是否存在
    import os
    basedir = master_dir + "/" + master_port
    if os.path.exists(basedir):
        return error('该实例目录已存在')
    if not os.path.exists(master_dir):
        os.system('mkdir -p %s' % (master_dir))
    # 判断端口是否占用
    from utils.network_tools import NetworkTools
    res = NetworkTools.check_process_open(master_port, 'mysqld')
    if res == True:
        return error('该实例端口已占用')

    mysqlhost = MysqlHostToools(master_dir, master_port)
    id1 = mysqlhost.create_masterhost(master_port, master_dir, version)
    # 此处通过调用api接口实现
    id2 = mysqlhost.queue_slavehost(master_id, slave_id, slave_dir, slave_port, version)
    data = []
    data.append(id1)
    data.append(id2)
    return success('数据库实例正在部署，请等待...', data)

@opman.route("/api/create_slavehost",methods=["POST"])
def create_slavehost():
    slave_basedir = request.form.get('slave_basedir')
    slave_port = request.form.get('slave_port')
    file = request.form.get('file')
    pos = request.form.get('pos')
    master_ip = request.form.get('master_ip')
    master_port = request.form.get('master_port')
    version = request.form.get('version')
    print version
    MysqlHostToools.create_slavehost(slave_port,slave_basedir,file, pos, master_port,master_ip,version)
    return JsonResponse({'mess': 'Slave实例部署中'})