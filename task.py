#!/usr/bin/evn python
# !-*- coding:utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import time
import psutil
from base import readFile, httpGet, WriteLog, GetMemInfo
import sqlitedb
import subprocess

pre = 0
timeoutCount = 0
sql = sqlitedb.Sql().dbfile('system')
sql_default = sqlitedb.Sql().dbfile('default')


def ExecShell(cmdstring, cwd=None, timeout=None, shell=True):
    global logPath
    import shlex
    import datetime
    import subprocess
    import time
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    sub = subprocess.Popen(cmdstring + ' > ' + logPath + ' 2>&1', cwd=cwd, stdin=subprocess.PIPE, shell=shell,
                           bufsize=4096)
    while sub.poll() is None:
        time.sleep(0.10000000000000001)

    return sub.returncode


def WriteLogs(logMsg):
    fp = open(logPath, 'w+')
    fp.write(logMsg)
    fp.close()


# 任务队列
def startTask():
    global isTask
    import time
    import config
    try:
        while True:
            try:
                if True:
                    taskArr = sql_default.table('tasks').where("status=?", ('0',)).field(
                        'id,name,type,execstr,dir').order("id asc").select()
                    for value in taskArr:
                        start = int(time.time())
                        if not sql_default.table('tasks').where("id=?", (value['id'],)).count(): continue;
                        if value['type'] == 'execshell':
                            print "执行完毕"
                            print value['execstr']
                            print time.strftime('%Y-%m-%d %h:%i:%s', time.localtime(time.time()))
                            print value['dir']
                            os.chdir(value['dir'])
                            cmstr = "%s >> %slogs/run_%s" % (value['execstr'], config.app_dir, value['id'])
                            os.system(cmstr)
                        end = int(time.time())
                        sql_default.table('tasks').where("id=?", (value['id'],)).save('status,end', ('1', end))
                        addtime = int(time.time())
                        day = 30
                        deltime = addtime - day * 86400
                        sql_default.table('tasks').where('addtime<?', (deltime,)).delete()
                        # if(sql.table('tasks').where("status=?",('0')).count() < 1): os.system('rm -f ' + isTask);
            except Exception, e:
                print "出错了"
                print e
                pass
            time.sleep(2)
    except:
        time.sleep(60);
        startTask();


def systemTask():
    import psutil
    global sql
    filename = 'data/control.conf'
    cpuIo = cpu = {}
    cpuCount = psutil.cpu_count()
    used = count = 0
    network_up = network_down = diskio_1 = diskio_2 = networkInfo = cpuInfo = diskInfo = None
    while True:
        day = 30
        tmp = {}
        post_login()
        p = subprocess.Popen('uptime', stdout=subprocess.PIPE)
        uptime = p.stdout.readline()
        p.wait()
        # 获取进程数
        process_num = len(psutil.pids())
        ##获取tcp ip 链接信息
        netstats = psutil.net_connections()
        networkList = {'tcp': 0, 'udp': 0}
        for netstat in netstats:
            if netstat.type == 1:
                networkList['tcp'] = networkList['tcp'] + 1
            else:
                networkList['udp'] = networkList['udp'] + 1

        # 获取内存信息
        meminfo = GetMemInfo()

        # cputimes信息
        cputime = psutil.cpu_times_percent(interval=1, percpu=False)

        pos = uptime.index('e:')
        loadstat = uptime[pos + 3:].split(',')

        status_list = ["LISTEN", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "LAST_ACK", "SYN_SENT"]
        status_temp = []
        net_connections = psutil.net_connections()
        for key in net_connections:
            status_temp.append(key.status)

        tmp['used'] = psutil.cpu_percent(interval=1)
        if not cpuInfo:
            tmp['mem'] = GetMemUsed()
            cpuInfo = tmp
        if cpuInfo['used'] < tmp['used']:
            tmp['mem'] = GetMemUsed()
            cpuInfo = tmp
        networkIo = psutil.net_io_counters()[:4]
        if not network_up:
            network_up = networkIo[0]
            network_down = networkIo[1]
            oldtime = time.time()
        tmp = {}
        ntime = int(time.time())
        tmp['upTotal'] = networkIo[0]
        tmp['downTotal'] = networkIo[1]
        tmp['up'] = round(float((networkIo[0] - network_up) / 1024) / (ntime - oldtime), 2)
        tmp['down'] = round(float((networkIo[1] - network_down) / 1024) / (ntime - oldtime), 2)
        tmp['downPackets'] = networkIo[3]
        tmp['upPackets'] = networkIo[2]
        network_up = networkIo[0]
        network_down = networkIo[1]
        oldtime = ntime
        if not networkInfo:
            networkInfo = tmp
        if tmp['up'] + tmp['down'] > networkInfo['up'] + networkInfo['down']:
            networkInfo = tmp
        if os.path.exists('/proc/diskstats'):
            diskio_2 = psutil.disk_io_counters()
            if not diskio_1:
                diskio_1 = diskio_2
            tmp = {}
            tmp['read_count'] = diskio_2.read_count - diskio_1.read_count
            tmp['write_count'] = diskio_2.write_count - diskio_1.write_count
            tmp['read_bytes'] = diskio_2.read_bytes - diskio_1.read_bytes
            tmp['write_bytes'] = diskio_2.write_bytes - diskio_1.write_bytes
            tmp['read_time'] = diskio_2.read_time - diskio_1.read_time
            tmp['write_time'] = diskio_2.write_time - diskio_1.write_time
            if not diskInfo:
                diskInfo = tmp
            else:
                diskInfo['read_count'] += tmp['read_count']
                diskInfo['write_count'] += tmp['write_count']
                diskInfo['read_bytes'] += tmp['read_bytes']
                diskInfo['write_bytes'] += tmp['write_bytes']
                diskInfo['read_time'] += tmp['read_time']
                diskInfo['write_time'] += tmp['write_time']
            diskio_1 = diskio_2
        if count >= 12:
            try:
                addtime = int(time.time())
                deltime = addtime - day * 86400
                data = (
                    # cpuInfo['used']/psutil.cpu_count(logical=False), cpuInfo['mem'], addtime)
                    cpuInfo['used']/psutil.cpu_count(logical=False), cpuInfo['mem'], addtime)

                sql.table('cpuio').add('pro,mem,addtime', data)
                sql.table('cpuio').where('addtime<?', (deltime,)).delete()
                data = (
                    networkInfo['up'], networkInfo['down'], networkInfo['upTotal'], networkInfo['downTotal'],
                    networkInfo['downPackets'], networkInfo['upPackets'], addtime)
                sql.table('network').add('up,down,total_up,total_down,down_packets,up_packets,addtime', data)
                sql.table('network').where('addtime<?', (deltime,)).delete()



                loadstatdata = (loadstat[0], loadstat[1], loadstat[2], addtime)
                sql.table('loadstat').add('five,fifteen,one,addtime', loadstatdata)
                sql.table('loadstat').where('addtime<?', (deltime,)).delete()

                net_status = {}
                for status in status_list:
                    net_status[status] = status_temp.count(status)

                net_status_data = (
                net_status['LISTEN'], net_status['ESTABLISHED'], net_status['TIME_WAIT'], net_status['CLOSE_WAIT'],
                net_status['LAST_ACK'], net_status['SYN_SENT'], addtime)
                sql.table('tcpconn').add('LISTEN,ESTABLISHED,TIME_WAIT,CLOSE_WAIT,LAST_ACK,SYN_SENT,addtime',
                                         net_status_data)
                sql.table('tcpconn').where('addtime<?', (deltime,)).delete()

                ##保存内存信息
                mem_data = (
                    meminfo['memTotal'], meminfo['memBuffers'], meminfo['memRealUsed'], addtime)
                sql.table('mem').add('memTotal,memBuffers,memRealUsed,addtime', mem_data)
                sql.table('mem').where('addtime<?', (deltime,)).delete()

                ##保存进程数
                pro_data = (
                    process_num, addtime)
                sql.table('process').add('process_number,addtime', pro_data)
                sql.table('process').where('addtime<?', (deltime,)).delete()

                ##保存tcp udp信息
                netstat_data = (networkList['tcp'], networkList['udp'], addtime)
                sql.table('tcpudp').add('tcp,udp,addtime', netstat_data)
                sql.table('tcpudp').where('addtime<?', (deltime,)).delete()

                ##保存cputimes信息
                cputimes_data = (cputime.user, cputime.nice, cputime.system, cputime.idle, cputime.iowait, addtime)
                sql.table('cputime').add('user,nice,system,idle,aiowait,addtime', cputimes_data)
                sql.table('cputime').where('addtime<?', (deltime,)).delete()
                # 进程监控
                mon_port()
                mon_proinfo()
                mon_netinter()
                # 清理数据

                if os.path.exists('/proc/diskstats'):
                    data = (
                        diskInfo['read_count'], diskInfo['write_count'], diskInfo['read_bytes'],
                        diskInfo['write_bytes'], diskInfo['read_time'], diskInfo['write_time'], addtime)
                    sql.table('diskio').add(
                        'read_count,write_count,read_bytes,write_bytes,read_time,write_time,addtime', data)
                    sql.table('diskio').where('addtime<?', (deltime,)).delete()
                cpuInfo = None
                networkInfo = None
                diskInfo = None
                count = 0
            except Exception, e:
                print e
                pass
        del tmp
        time.sleep(5)
        count += 1

    return


#进程监控
def mon_proinfo():
    ip =httpGet("http://ip.6655.com/ip.aspx")
    addtime = int(time.time())
    deltime = addtime - 30 * 86400
    proinfo = sql.table('prokey').field("id,prokey,addtime,value,status,sendsms").where("status=?", ('1',)).select()
    for pro in proinfo:
        up_id = pro['id']
        print up_id
        pro = pro['prokey']
        if not pro:
            continue
        cmd='ps -ef |grep "%s" |grep -v grep' %(pro)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
        body = p.stdout.readlines()
        p.wait()
        #进程不存在报警短信
        value='进程正常'
        if not body:
            value='进程不存在'
            #30分钟前是否发送过判断是否发送过
            issendsms = sql.table('prokey').field('sendsms').where("addtime>=? and prokey=? and status=? and sendsms=?", (addtime-1800,pro,1,0)).find()
            if issendsms:
                save_data = (pro, addtime, '进程不存在', 1, 1)
                sql.table('prokey').where("id=?",(up_id,)).save('prokey,addtime,value,status,sendsms', save_data)
                print "发送短信"
                os.system("python /data0/scripts/devops/agent/console/main.py sendsms '%s'>/dev/null 2>&1" % (
                            "自动运维平台监控到您的服务器 进程监控 服务器ip:%s 进程:%s" % (ip, pro)))

        else:
            save_data = (pro, addtime,'进程正常',0)
            sql.table('prokey').where("id=?",(up_id,)).save('prokey,addtime,value,sendsms', save_data)
            # if count==0:
            #     os.system("python /data0/scripts/devops/agent/console/main.py sendsms '%s'>/dev/null 2>&1" %("自动运维平台监控到您的服务器 进程监控 服务器ip:%s 进程:%s" %(ip,pro)))
        #保存监控信息
        # save_data = (pro, addtime, value,)
        # sql.table('prokey').add('prokey,addtime,value',save_data)
#抓取网络接口信息
def mon_netinter():
    addtime = int(time.time())
    deltime = addtime - 30 * 86400
    # 获取网卡流量
    nowtime = int(time.time())
    net_interface = psutil.net_io_counters(pernic=True)
    save_data=()
    for eth in net_interface:
        if eth == 'lo':
            continue
        info = sql.table('net_interface').where("name=?", (eth,)).order('id desc').find()

        net_inter_bytes_sent = net_interface[eth].bytes_sent
        net_inter_bytes_recv = net_interface[eth].bytes_recv
        net_inter_packets_sent = net_interface[eth].packets_sent
        net_inter_packets_recv = net_interface[eth].packets_recv
        if not info:
            info = psutil.net_io_counters(pernic=True)
            oldnet_inter_bytes_sent = info[eth].bytes_sent
            oldnet_inter_bytes_recv = info[eth].bytes_recv
            net_inter_packets_sent = info[eth].packets_sent
            net_inter_packets_recv = info[eth].packets_recv
            oldtime = int(time.time())
            time.sleep(5)
        else:
            oldnet_inter_bytes_sent = info[1]
            oldnet_inter_bytes_recv = info[2]
            oldnet_inter_packets_sent = info[3]
            oldnet_inter_packets_recv = info[4]
            oldtime = int(info[6])
        net_inter_bytes_sent = net_interface[eth].bytes_sent
        net_inter_bytes_recv = net_interface[eth].bytes_recv
        nowtime = int(time.time())
        sent = round(float((int(net_inter_bytes_sent) - int(oldnet_inter_bytes_sent)) / 1024) / (int(nowtime) - int(oldtime)), 2)
        recv = round(float((int(net_inter_bytes_recv) - int(oldnet_inter_bytes_recv)) / 1024) / (int(nowtime) - int(oldtime)), 2)
        if sent < 0:
            sent=0
        if recv < 0:
            recv=0


        save_data = (
            net_inter_bytes_sent,net_inter_bytes_recv,net_inter_packets_sent,
            net_inter_packets_recv,nowtime,sent,recv,eth)
        sql.table('net_interface').add('bytes_sent,bytes_recv,packets_sent,packets_recv,addtime,sent,recv,name', save_data)
        sql.table('net_interface').where('addtime<?', (deltime,)).delete()





    pass
# 监控端口信息
def mon_port():
    ip = httpGet("http://ip.6655.com/ip.aspx")
    portarr = sql.table('port').field('id,port').where("status=?", (1,)).select()
    addtime = int(time.time())
    deltime = addtime - 30 * 86400
    tmp = {}
    if portarr:
        net_connections = psutil.net_connections()
        for port in portarr:
            upid = port['id']
            port = port['port']
            if int(port)==0 or not port:
                continue
            valid = False
            for key in net_connections:
                if key.status == 'LISTEN' and int(key.laddr[1]) == int(port):
                    valid = True
                    pid = key.pid
                    p = psutil.Process(pid)
                    cputimes = p.cpu_times()
                    tmp['port'] = key.laddr[1]

                    # 计算cpu使用率
                    if cputimes.user > 1:
                        tmp['cpu'] = p.cpu_percent(interval=1)
                    else:
                        tmp['cpu'] = 0.0
                    # 计算进程内存占用率
                    tmp['mem'] = round(p.memory_percent(), 3)
                    tmp['name'] = p.name()
            value = '端口正常'
            if valid==False:
                value = '端口异常'
                # 30分钟前是否发送过判断是否发送过
                issendsms = sql.table('port').field('id').where('id=? and status=? and sendsms=?',(upid,1,0)).find()

                # 保存异常数据
                addtime = time.time()
                if issendsms:
                    data = (
                        value,1)
                    sql.table('port').where("id=?",(upid,)).save('value,sendsms', data)
                    print "发送短信2"
                    os.system("python /data0/scripts/devops/agent/console/main.py sendsms '%s'>/dev/null 2>&1" % (
                                "自动运维平台监控到您的服务器 端口监控 服务器ip:%s 端口:%s" % (ip, int(port))))
            else:
                #保存数据
                addtime = time.time()
                data = (
                    tmp['port'], tmp['cpu'], tmp['mem'], tmp['name'], addtime,value)
                sql.table('port').where('id=?',(upid,)).save('port,cpu,mem,name,addtime,value', data)

# 上传登入信息
def post_login():
    import os
    os.system("python /data0/scripts/devops/agent/console/main.py sshloginlog >/dev/null 2>&1")

    pass


def GetMemUsed():
    import psutil
    mem = psutil.virtual_memory()
    memInfo = {'memTotal': mem.total / 1024 / 1024, 'memFree': mem.free / 1024 / 1024,
               'memBuffers': mem.buffers / 1024 / 1024, 'memCached': mem.cached / 1024 / 1024}
    tmp = memInfo['memTotal'] - memInfo['memFree'] - memInfo['memBuffers'] - memInfo['memCached']
    tmp1 = memInfo['memTotal'] / 100
    return tmp / tmp1


if __name__ == '__main__':
    import threading
    threads = []
    t = threading.Thread(target=systemTask)
    t.start()
    startTask()
