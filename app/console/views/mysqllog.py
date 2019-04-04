#!/bin/evn/python
# -*- coding:utf-8 -*-

import sys
import subprocess
sys.path.append('../')
from utils.sms import Sms
from utils.host import Host
class Mysqllog(object):
    # 上传数据到服务器
    def upload_server(self, msg,port):
        print "dfsfdsf"
        from utils.host import Host
        resp = Host().upload('api/save_mysqlog',{'msg':msg,'port':port})
        print resp


