#!/bin/bash -
PATH=/usr/local/webserver/percona/bin:/usr/local/webserver/nginx/sbin/:/usr/local/webserver/php/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
#===============================================================================
#
#          FILE: gen.sh
# 
#         USAGE: ./gen.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: xaobo_l (), xiaobol9527@gmail.com
#  ORGANIZATION: none
#       CREATED: 06/01/2015 21:46
#      REVISION:  ---
#===============================================================================


set -o nounset
set -o errexit

cd $(dirname $0)



mysql_install_dir=/usr/local/webserver/percona
base_dir=$2
port=$1

if [ -d "$base_dir/$port" ]; then
        echo "the file exist!"
        exit 1
fi
bash ./gen_mysql_dir.sh $mysql_install_dir $base_dir $port
$mysql_install_dir/scripts/mysql_install_db --basedir=$mysql_install_dir --defaults-file=$base_dir/$port/my.cnf
$base_dir/$port/mysqld start
sleep 5
/usr/bin/python /data0/scripts/devops/agent/app/console/main.py mysqlog "数据库主实例 $port $base_dir 部署成功" $port
bash ./secure_install.sh $base_dir/$port/mysql.sock
/usr/bin/python /data0/scripts/devops/agent/app/console/main.py mysqlog "配置数据库主实例的安全配置 $port $base_dir 配置成功" $port
