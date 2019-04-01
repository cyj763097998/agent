#/usr/bin/env python
#coding=utf-8
#edit richard  2019/3/14

from . import opman
from flask import render_template, url_for, redirect,flash,session,request,abort,Response,jsonify
from .common import success,error
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
    print version
    if int(version) == 1:
        version = "5.6"
    else:
        version = "5.7"
    master_id = request.form.get('master_id')
    slave_id = request.form.get('slave_id')
    print master_dir
    print master_port
    print slave_dir
    print slave_port
    print version
    print master_id
    print slave_id
    print "---------------"
    return error("实例存在")
    """
    # 判断实例是否存在
    import os
    basedir = master_dir + "/" + master_port
    if os.path.exists(basedir):
        return error('该实例目录已存在')
    if not os.path.exists(master_dir):
        os.system('mkdir -p %s' % (master_dir))
    # 判断端口是否占用
    from opman.utils.network_tools import NetworkTools
    res = NetworkTools.check_process_open(master_port, 'mysqld')
    if res == True:
        return error('该实例端口已占用')

    #message = "实例存在"
    #response = {'code': 400, 'message': message}
    #return error("实例存在")
    """
