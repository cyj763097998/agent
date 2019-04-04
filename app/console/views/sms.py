#!/bin/evn/python
# -*- coding:utf-8 -*-

import sys
import subprocess
sys.path.append('../')
from utils.host import Host
class Sms(object):
    def upload_server(self,msg):
        from utils.host import Host
        res = Host().upload('api/sendsms',{'msg':msg})

    def usersendsms(self,msg,mobile):
        from utils.host import Host
        res = Host().upload('api/usersendsms',{'msg':msg,'mobile':mobile})




