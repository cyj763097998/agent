#!/bin/evn python
# -*- coding:utf-8 -*-

from http import Http
import os,time
class Host(object):
    #init 配置
    def __init__(self):
        carr = self.config()
        self.domain = carr['domain']
        self.username=carr['username']
        self.port = carr['port']
        self.password = carr['password']
        self.access_tokenfile = 'access_token.json'
    def config(self):
        return {'domain':'devops.258.com',
                'username':'admin',
                'password':'xJn5U1lXEEhhkgsV',
                'port':258
                }

    #获取 access_token
    def get_token(self):
        token = self.login()
        return token
        # if not os.path.exists(self.access_tokenfile):
        #     self.login()

    # 登入主机
    def login(self):
        from http import Http
        import json
        data = {'username': self.username, 'password': self.password}
        headers = {'content-type': 'application/json'}
        try:
            data = Http.post('http://%s:%s/api/token/' % (self.config()['domain'],self.config()['port']), data, headers)
            if data.status_code == 400:
                return False
            data = json.loads(data.text)
            return data['token']
        except Exception, e:
            return False
    #上传数据到服务器
    def upload(self,url,data):
        import json
        data = json.dumps(data)
        ip = Http.get("http://ip.6655.com/ip.aspx",datas={},heads={'content-type': 'application/json'})
        ip = ip.text
        headers = {'content-type': 'application/json', 'ip': '%s' %(ip),'Authorization': '258JWTAUTH %s' % (self.get_token())}
        try:
            import json
            data = Http.post('http://%s:%s/%s' % (self.config()['domain'],self.config()['port'],url), data, headers)
            print "dfds"
            print data.text
            data = json.loads(data.text)
            print data
            if data['code']==400:
                return "上报数据失败"
            return True
        except Exception, e:
            print e
            return False
        # # Http.post()
    def get_ip(self):
        response = Http.get("http://ip.6655.com/ip.aspx")
        return response.text
    def write(self,filename,body,model="w+"):
        try:
            f = open(filename, model)
            f.write(body)
            f.close()
        except Exception,e:
            return False

    def read(self,filename,model="r"):
        try:
            f = open(filename, model)
            body = f.read()
            f.close()
            return body
        except Exception,e:
            return False



