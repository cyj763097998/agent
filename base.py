#!/usr/bin/python
# -*- coding: utf-8 -*- #
import time
import base64
import os
import hashlib
import uuid
import json
import subprocess
import psutil
import config
import stat


#后台执行文件
def nohupExecShell(cmdstring, cwd=None, timeout=None, shell=True):
    import subprocess
    logfile = cwd + "/build.log"
    p = subprocess.Popen(cmdstring + ' > ' + logfile + ' 2>&1',cwd=cwd,stdout=subprocess.PIPE,shell=True)
    print cmdstring + ' > ' + logfile + ' 2>&1'
    result = p.stdout.readlines()
    p.wait()
    return True
def hook(domain,common,webdir):
    git_dir = "%s/%s" % (config.report_dir, domain)
    os.chdir("%s" % (git_dir))
    nohupExecShell('%s %s %s DES' %(common,git_dir,git_dir),git_dir)

    #判断发送结果

"""
读取文件
"""
def readFile(filename):
    try:
        fp = open(filename, 'r')
        fBody = fp.read()
        fp.close()
        return fBody
    except Exception,e:
        print e
        return False

"""
http get请求
"""
def httpGet(url):
    try:
        import urllib2
        response = urllib2.urlopen(url)
        return response.read()
    except Exception, ex:
        return str(ex)

"""
写入日志
"""
def WriteLog(logMsg):
    pass
    # try:
    #     mDate = time.strftime('%Y-%m-%d %X', time.localtime())
    #     mDate = time.strftime('%Y%m%d', time.localtime())
    #     writeFile('access.log',logMsg)
    # except Exception,e:
    #     pass

"""
获取内存信息
"""
def GetMemInfo():
    mem = psutil.virtual_memory()
    memInfo = {'memTotal': mem.total / 1024 / 1024, 'memFree': mem.free / 1024 / 1024,
               'memBuffers': mem.buffers / 1024 / 1024, 'memCached': mem.cached / 1024 / 1024}
    memInfo['memRealUsed'] = memInfo['memTotal'] - memInfo['memFree'] - memInfo['memBuffers'] - memInfo['memCached']
    return memInfo

def writeFile(filename, str,model='a+'):
    try:
        fp = open(filename, model)
        fp.write(str + '\n')
        fp.close()
        return True
    except:
        return False

"""
更新到指定commit版本
"""
def gitresetCommit(branch, domain, gitUrl,commit_id,lineid=10):
    import config
    git_dir = "%s/%s" % (config.report_dir, domain)
    ##先更新
    gitupdateRepo(branch,domain,gitUrl)
    os.chdir("%s" % (git_dir))
    WriteLog(commit_id)
    if commit_id=='自动获取':
        res = gitlastCommit(domain,branch,gitUrl)
        commit_id = str(res[0]['commit'])
        author = str(res[0]['author'])
        comment = str(res[0]['comment'])
        commit_id = commit_id.strip()
        import urllib2
        comment = urllib2.quote(comment)
        author = urllib2.quote(author)
        print httpGet('http://127.0.0.1:258/line/update_line?lineid=%s&commit_id=%s&comment=%s&author=%s&status=0' %(lineid,commit_id,comment,author))
    os.system("/usr/bin/env git reset -q --hard %s" %(commit_id))

"""
更新仓库
"""
def gitupdateRepo(branch,domain,gitUrl):

        git_dir ="%s/%s" %(config.report_dir,domain)
        if os.path.exists(git_dir + "/.git"):
            os.chdir('%s' % (git_dir))
            if branch:
                os.popen('git checkout -q %s' %(branch))
            os.popen('git fetch -p -q --all')
            if branch:
                os.popen('/usr/bin/env git reset -q --hard origin/%s' %(branch))
            else:
                os.popen('/usr/bin/env git reset -q --hard')
        else:
            import time
            os.system("rm -rf %s" %(git_dir))
            os.system("mkdir %s" % (git_dir))
            #time.sleep(1)
            os.chdir('%s' %(git_dir))
            os.system('expect %s/scripts/git/git.expect %s %s' % (config.app_dir,gitUrl,git_dir))

###获取最新提交
def gitlastCommit(domain,branch,giturl,count=2):
    gitdir = "%s/%s" %(config.report_dir,domain)
    gitupdateRepo(branch, domain, giturl)
    os.chdir(gitdir)
    os.system('git fetch -p -q --all')
    ####os.system('/usr/bin/env git reset -q --hard origin/%s' % (branch))
    fp = subprocess.Popen('git log -%s' % (count),shell=True,stdout=subprocess.PIPE)
    lines = fp.stdout.readlines()
    beginTag = False
    commitList=[]
    goodLine = {"commit": "", "author": "", 'date': ""}
    for line in lines:
        if len(line) <= 2:
            continue
        if line.startswith("commit"):
            beginTag = True
            goodLine['commit'] = line[6:].strip('\n')
            continue
        if beginTag:
            if line.startswith("Merge: "):
                goodLine['Merge'] = line[7:].strip('\n')
            elif line.startswith("Author: "):
                goodLine['author'] = line[8:].strip('\n')
            elif line.startswith("Date: "):
                goodLine['date'] = line[6:].strip('\n')
            else:
                import re
                # if re.search(r'Merge.*branch.*', line):
                #     beginTag = False
                #     goodLine = {}
                #     continue
                goodLine['comment'] = line
                beginTag = False
                commitList.append(goodLine)
                goodLine={}
    return commitList




'''
svn 函数
'''
"""
更新到指定commit版本
"""
def svnresetCommit(domain, svnUrl,commit_id,lineid=0):
    svnuser = config.svnuser
    svnpass = config.svnpass
    dir = "%s/%s" % (config.report_dir, domain)
    svnupdateRepo(domain,svnUrl)
    os.chdir("%s" % (dir))
    WriteLog(commit_id)
    if commit_id=='自动获取':
        res = getsvnCommitList(domain,svnUrl,50)
        commit_id = res[0]['commit']
        author = res[0]['author']
        comment = res[0]['comment']
        import urllib2
        comment = urllib2.quote(comment)
        author = urllib2.quote(author)
        print httpGet('http://127.0.0.1:258/line/update_line?lineid=%s&commit_id=%s&comment=%s&author=%s&status=0' %(lineid,commit_id,comment,author))
    os.system("svn up --username '%s' --password '%s' -q --force -r %s" % (svnuser, svnpass, commit_id))


"""
svn更新仓库
"""
def svnupdateRepo(domain,svnurl):
        svn_dir ="%s/%s" %(config.report_dir,domain)
        # import sqlitedb
        # sql = sqlitedb.Sql().dbfile('default')
        # system = sql.table('config').where('id=?', (1,)).find()
        # svnuser =system[6]
        # svnpass = system[7]
        svnuser = config.svnuser
        svnpass = config.svnpass

        if not os.path.exists('/root/.subversion/servers'):
            os.system('mkdir -p /root/.subversion/')
            writeFile('/root/.subversion/servers','[global]\nstore-plaintext-passwords = yes','w+')
        if os.path.exists(svn_dir + "/.svn"):
            os.chdir('%s' % (svn_dir))
            os.system('svn cleanup')
            os.system('svn revert . -q -R')
            os.system('svn up --username "%s" --password "%s" -q' %(svnuser,svnpass))
        else:
            import time
            os.system("rm -rf %s" %(svn_dir))
            os.system("mkdir %s" % (svn_dir))
            os.chdir('%s' %(svn_dir))
            os.system('svn checkout %s --username "%s" --password "%s" . --force -q' %(svnurl,svnuser,svnpass))

"""
同步站点
"""
def rsyncSite(domain,sshport,webdir,gitdir, commit_id,ip,lineid=0):
    gitdir = "%s/%s" % (config.report_dir, domain)
    if os.path.exists("/root/.ssh")== False:
        os.system('mkdir -p /root/.ssh')
    os.system('chown www:www %s -R' %(gitdir))
    os.system("expect %s/scripts/rsync/rsync.expect %s %s %s %s" % (config.app_dir,str(gitdir), str(webdir), str(ip), str(sshport)))
    httpGet('http://127.0.0.1:258/line/update_line?lineid=%s&commit_id=%s&status=1&comment=&author=' % (str(lineid), str(commit_id.strip())))

"""
同步文件站点
"""
def rsync_file(domain,sshport,webdir,gitdir, commit_id,ip,lineid,files):
    gitdir = "%s/%s" % (config.report_dir, domain)
    if os.path.exists("/root/.ssh")== False:
        os.system('mkdir -p /root/.ssh')
    os.system('chown www:www %s -R' %(gitdir))

    files = files.split("||")

    for file in files:
        if not file:
            continue
        webdir=webdir + "/" + file.replace('/home/report/%s' %(domain),'')
        webdir=webdir.replace('//','/').rstrip('/')
        if os.path.isdir(webdir):
            webdir= webdir + '/'
        file=file.replace('//','/').rstrip('/')
        if os.path.isdir(file):
            file=file + '/'
        print("expect %s/scripts/rsync/rsync_files.expect %s %s %s %s >/dev/null 2>&1 &" % (config.app_dir,str(file), str(webdir), str(ip), str(sshport)))

        os.system("expect %s/scripts/rsync/rsync_files.expect %s %s %s %s >/dev/null 2>&1 &" % (config.app_dir,str(file), str(webdir), str(ip), str(sshport)))
    httpGet('http://127.0.0.1:258/line/update_line?lineid=%s&commit_id=%s&status=1&comment=&author=' % (str(lineid), str(commit_id.strip())))



def getsvnCommitList(domain,svnurl,count=50):
    svndir = "%s/%s" %(config.report_dir,domain)
    svnupdateRepo(domain,svnurl)
    os.chdir(svndir)
    fp = subprocess.Popen('svn log -l %s' % (count), shell=True, stdout=subprocess.PIPE)
    lines = fp.stdout.readlines()
    beginTag = False
    commitList = []
    goodLine = {"commit": "", "author": "", 'date': ""}
    for line in lines:
        res = line.split("|")
        if len(res) == 1 and res[0].startswith("-"):
            continue
        if len(res) == 1 and res[0].startswith('\n'):
            continue
        if len(res) == 4:
            beginTag = True
            goodLine['commit'] = res[0]
            goodLine['author'] = res[1]
            goodLine['date'] = res[2]
            continue
        if beginTag:
            try:
                goodLine['comment'] = res[0]
            except Exception,e:
                print e
                goodLine['comment']=''
            commitList.append(goodLine)
            beginTag = False
            goodLine={}
            continue
    if not commitList and goodLine:
        goodLine['comment'] = ''
        commitList.append(goodLine)
    return commitList