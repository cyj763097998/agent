#!/bin/evn/python
# -*- coding:utf-8 -*-

def readfile(filename,model="r"):
    f=open(filename,model)
    return f.read()

def ExecShell(cmdstring, cwd=None, timeout=None, shell=True):
    global logPath
    import shlex
    import datetime
    import subprocess
    import time
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    sub = subprocess.Popen(cmdstring, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096)
    while sub.poll() is None:
        time.sleep(0.10000000000000001)

    return sub.returncode