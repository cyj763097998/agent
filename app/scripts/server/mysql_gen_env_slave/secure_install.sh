exec=/usr/local/webserver/percona/bin/mysql
sock=$1
file=$2
pos=$3
master_ip=$4
master_port=$5
$exec -S $sock -e "drop database test;"
$exec -S $sock -e "DELETE FROM mysql.user WHERE user != 'root' OR host != 'localhost';"
$exec -S $sock -e "DELETE FROM mysql.db;"
$exec -S $sock -e "stop slave;"
$exec -S $sock -e "change master to master_host='$master_ip',master_port=$master_port,master_user='replication',master_password='Faw1gt2wtikpuf597Hrw',master_log_file='$file',master_log_pos=$pos;"
$exec -S $sock -e "start slave;"
$exec -S $sock -e "show slave status\G;"
$exec -S $sock -e "grant replication slave, replication client on *.* to 'replication'@'%' identified by 'Faw1gt2wtikpuf597Hrw'"
$exec -S $sock -e "grant all on *.* to 'remote'@'%' identified by '13bppv3ovbe0bh5zBggY'  WITH GRANT OPTION;"
$exec -S $sock -e "set password for 'root'@'localhost' = password('3vucOcdar8jsta23fQ1b');"
$exec -S $sock -e "flush privileges;"


