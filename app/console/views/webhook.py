#!/bin/evn/python
# -*- coding:utf-8 -*-

import sys
import subprocess
sys.path.append('../')
from utils.host import Host
class WebHook(object):
    def upload_server(self,hook_id):
        from utils.host import Host
        res = Host().upload('api/webhook', {'hook_id': hook_id})
        print res



