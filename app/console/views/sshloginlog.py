#!/bin/evn/python
# -*- coding:utf-8 -*-

import sys
import subprocess
sys.path.append('../')
from utils.sms import Sms
from utils.host import Host

class Sshloginlog(object):

    def __init__(self):
        self.ips=[]#以前登入记录
        self.loginip=''#登入ip
        self.lastlogin = []#登入信息
        self.excludeip=['127.0.0.1','121.43.189.36']#排除ip

    def welcome(self):
        print "欢迎访问258运维平台"
    def test(self):
        self.welcome()
        #init 服务器
        body=  self.get_body()
        # self.initupload_server(body)


        # #判断是否异常ip 和排除ip
        if  self.loginip not in self.ips and self.loginip not in self.excludeip:
            print "您存在异地登入"
            self.lastlogin['status'] = 0
            self.upload_server(self.lastlogin)
            #上报服务器报警
        else:
            self.lastlogin['status'] = 1
            self.upload_server(self.lastlogin)
        # #保存登入记录
    #获取登入日志
    def get_body(self):
        import os
        import hashlib
        m2 = hashlib.md5()
        data_list = []
        p = os.popen("last |awk '{print $1 \"#\" $2 \"#\" $3 \"#\" $4$5$6$7$8$9$10}'")
        i=0
        for body in p:
            if body.startswith("###"):
                continue
            body = body.strip()
            body = body.split("#")
            m2.update(body[2] + body[0] + body[1] + body[3])
            hash = m2.hexdigest()
            if i==0:
                i+=1
                self.loginip = body[2]
                print "当前登入ip:%s" %(body[2])
                self.lastlogin= {'user':body[0],'pts':body[1],'ipaddr':body[2],'online_date':body[3],'hash':hash}
                continue
            data_list.append({'status':1,'user':body[0],'pts':body[1],'ipaddr':body[2],'online_date':body[3],'hash':hash})
            self.ips.append(body[2])
            self.ips.append(body[0])
            i+=1
        return data_list


    #上传数据到服务器
    def initupload_server(self,data):
        from utils.host import Host
        resp = Host().upload('api/save_sshloginlog',data)

    # 上传数据到服务器
    def upload_server(self, data):
        from utils.host import Host
        resp = Host().upload('api/save_current',data)


