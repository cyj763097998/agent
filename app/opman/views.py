#/usr/bin/env python
#coding=utf-8
#edit richard  2019/3/14

from . import opman
from flask import render_template, url_for, redirect,flash,session,request,abort
#from forms import LoginForm,PwdForm,TagForm,AuthForm,RoleForm,AdminForm
#from app.models import Admin,Tag,Auth,Role
#from functools import wraps
#from app import db
#import datetime
@opman.route("/api/create_masterhost",methods=["POST"])
def create_masterhost():
    master_dir = request.form.get('master_dir')
    master_port = request.form.get('master_port')
    print 11111111111
    print master_dir
    print master_port
    return "create_masterhost"
