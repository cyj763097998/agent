#!/bin/bash - 
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
bash ./secure_install.sh $base_dir/$port/mysql.sock
