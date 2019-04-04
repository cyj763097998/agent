#!/bin/evn python
# -*- coding:utf-8 -*-

from http import Http
import os,time
from host import Host
class Sms(object):
    def sendsms(self,data):
        Host().upload('api/sendsms',data)
        return True


