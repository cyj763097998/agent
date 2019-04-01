# -*- coding:utf-8 -*-

class NetworkTools(object):

    @staticmethod
    def GetNetWorkList():
        import psutil
        netstats = psutil.net_connections()
        networkList = []
        for netstat in netstats:
            tmp = {}
            if netstat.type == 1:
                tmp['type'] = 'tcp'
            else:
                tmp['type'] = 'udp'
            tmp['family'] = netstat.family
            tmp['laddr'] = netstat.laddr
            tmp['raddr'] = netstat.raddr
            tmp['status'] = netstat.status
            p = psutil.Process(netstat.pid)
            tmp['process'] = p.name()
            tmp['pid'] = netstat.pid
            networkList.append(tmp)
            del p
            del tmp
        networkList = sorted(networkList, key=lambda x: x['status'], reverse=True)
        return networkList



    '''
    检测进程是否存在的指定端口是否占用
    '''
    @staticmethod
    def check_process_open(port,keyword):
        import psutil
        netstats = psutil.net_connections()
        networkList = []
        for netstat in netstats:
            if netstat.status=='LISTEN':
                p = psutil.Process(netstat.pid)
                name = p.name()
                res = name.find(keyword)
                if res>=0:
                    #找到进程
                    s_port = netstat.laddr[1]
                    if int(s_port) == int(port):
                        print s_port
                        print "进程 端口存在"
                        return True
        print "dsfdf"
        return False


    '''
    进程 的开放端口
    '''
    @staticmethod
    def process_openport(keyword):
        import psutil
        print keyword
        data_list=[]
        netstats = psutil.net_connections()
        networkList = []
        for netstat in netstats:
            if netstat.status == 'LISTEN':
                p = psutil.Process(netstat.pid)
                name = p.name()
                res = name.startswith(keyword)
                if res == True:
                    data_list.append(netstat.laddr[1])
        data={}
        if not data_list:
            data['max'] = 28018
            data['list'] = []
        else:
            data['max'] = int(max(data_list))+1
            data['list'] = data_list
        return data
