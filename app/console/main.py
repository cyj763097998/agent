#!/bin/evn/python
# -*- coding:utf-8 -*-
import sys

class Main(object):

    @staticmethod
    def run(name=''):
        if name=='sshloginlog':
            from views.sshloginlog import Sshloginlog
            Sshloginlog().test()
        if name=='mysqlog':
            from views.mysqllog import Mysqllog
            msg = sys.argv[2]
            port = sys.argv[3]
            Mysqllog().upload_server(msg,port)
        if name=='webhook':
            from views.webhook import WebHook
            hook_id = sys.argv[2]
            WebHook().upload_server(hook_id)

        if name=='sendsms':
            from views.sms import Sms
            msg = sys.argv[2]
            Sms().upload_server(msg)

        if name=='usersendsms':
            from views.sms import Sms
            msg = sys.argv[2]
            mobile = sys.argv[3]
            Sms().usersendsms(msg,mobile)

if __name__ == '__main__':

    if len(sys.argv)<2:
        print "参数错误"
        exit()
    name = sys.argv[1]
    Main.run(name)
