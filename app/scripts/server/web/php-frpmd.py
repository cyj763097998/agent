#!/usr/bin/python
#coding: utf-8
# +-------------------------------------------------------------------
# | 258 运维平台
# +-------------------------------------------------------------------
# | Copyright (c) 2018 All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄云建 <22327635@qq.com>
# +-------------------------------------------------------------------


#------------------------------
# php-fpm 启动 停止 重启 控制
#------------------------------

import sys
class Php_fpmd(object):

    php_fpm=''
    def __init__(self,php_fpm):
        self.php_fpm = php_fpm
        self.init()


    def init(self):
        import os
        ##防止重启502
        os.system("rm -f /dev/shm/php-cgi-template.sock")
        res = self.process_exists(self.php_fpm)
        if res:
            print self.ExecShell("%s/init.d.php-fpm reload" %(self.php_fpm))
        else:
            print self.ExecShell("%s/init.d.php-fpm start" % (self.php_fpm))

    def ExecShell(self, cmdstring, cwd=None, timeout=None, shell=True):
        import shlex
        import datetime
        import subprocess
        import time
        if shell:
            cmdstring_list = cmdstring
        else:
            cmdstring_list = shlex.split(cmdstring)
        if timeout:
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while sub.poll() is None:
            time.sleep(0.10000000000000001)
            if timeout:
                if end_time <= datetime.datetime.now():
                    raise Exception('Timeout\xef\xbc\x9a%s' % cmdstring)

        return sub.communicate()

    def process_exists(self, path):
        import psutil
        all_process_name = psutil.pids()
        for pid in all_process_name:
            pro = psutil.Process(pid)
            if pro.exe().find(path) >= 0:
                return True
        return False
if  __name__ == '__main__':
    php_fpm_exe = sys.argv[1]
    php = Php_fpmd(php_fpm_exe)