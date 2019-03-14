#/usr/bin/env python
#coding=utf-8
#edit richard  2019/3/14

from flask import  Flask,render_template
#from flask_sqlalchemy import SQLAlchemy
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

app =  Flask(__name__)
app.debug = True

from app.opman import opman  as opman_blueprint

app.register_blueprint(opman_blueprint)


