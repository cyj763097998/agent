#!/bin/bash - 
#===============================================================================
#
#          FILE: gen_mysql_dir.sh
# 
#         USAGE: ./gen_mysql_dir.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: xaobo_l (), xiaobol9527@gmail.com
#  ORGANIZATION: none
#       CREATED: 10/12/2014 21:46
#      REVISION:  ---
#===============================================================================


set -o nounset
set -o errexit

cd $(dirname $0)


mysql_install_dir=$1
dir=$2
port=$3
default_dir=default_file
base_dir=$dir/$port



if [ -d $base_dir ]; then
	echo "the file exist!"
	exit 1
fi


mkdir $base_dir
mkdir $base_dir/data
mkdir $base_dir/logs/
mkdir $base_dir/logs/binlog
mkdir $base_dir/logs/relaylog

chown mysql:mysql $base_dir -R

cp $default_dir/mysqld $base_dir
cp $default_dir/my.cnf $base_dir


perl -pe "s#__DATADIR__#$base_dir/data#" -i $base_dir/mysqld
perl -pe "s#__DEFAULT_FILE__#$base_dir/my.cnf#" -i $base_dir/mysqld
perl -pe "s#__MYSQL_INSTALL_DIR__#$mysql_install_dir#" -i $base_dir/mysqld

preip=`curl -s ip.6655.com/ip.aspx |awk -F '.' '{print $4}'`
perl -pe "s#__BASE_DIR__#$base_dir#" -i $base_dir/my.cnf
perl -pe "s#189__BASE_PORT__#$preip$port#" -i $base_dir/my.cnf
perl -pe "s#__BASE_PORT__#$port#" -i $base_dir/my.cnf
perl -pe "s#__MYSQL_INSTALL_DIR__#$mysql_install_dir#" -i $base_dir/my.cnf
