#!/usr/bin/env python
 # -*- coding:utf-8 -*-
import requests
import json

class Http(object):

     @staticmethod
     def get(url,datas={},heads={'content-type': 'application/json'}):
         response =requests.get(url)
         return response

     @staticmethod
     def post(url,datas={},heads={'content-type': 'application/json'}):
         datas = json.dumps(datas)
         response = requests.post(url, data=datas, headers=heads)
         return response
