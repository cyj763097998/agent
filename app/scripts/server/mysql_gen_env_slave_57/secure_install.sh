exec=/usr/local/webserver/mysql-57/bin/mysql
sock=$1
file=$2
pos=$3
master_ip=$4
master_port=$5
basedir=$6
pass=`grep "generated" $basedir/logs/mysql-error.log  |awk -F ": " '{print $2}'`
$exec -S $sock -e "set password for 'root'@'localhost' = password('3vucOcdar8jsta23fQ1b');"
pass=3vucOcdar8jsta23fQ1b
$exec -S $sock -p$pass -e "DELETE FROM mysql.user WHERE user != 'root' OR host != 'localhost';"
$exec -S $sock -p$pass -e "DELETE FROM mysql.db;"
$exec -S $sock -p$pass -e "stop slave;"
$exec -S $sock -p$pass -e "change master to master_host='$master_ip',master_port=$master_port,master_user='replication',master_password='Faw1gt2wtikpuf597Hrw',master_log_file='$file',master_log_pos=$pos;"
$exec -S $sock -p$pass -e "start slave;"
$exec -S $sock -p$pass -e "show slave status\G;"
$exec -S $sock -p$pass -e "grant replication slave, replication client on *.* to 'replication'@'%' identified by 'Faw1gt2wtikpuf597Hrw';"
$exec -S $sock -p$pass -e "grant all on *.* to 'remote'@'%' identified by '13bppv3ovbe0bh5zBggY'  WITH GRANT OPTION;"
$exec -S $sock -p$pass -e "flush privileges;"

