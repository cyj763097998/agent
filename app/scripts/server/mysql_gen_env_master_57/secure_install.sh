exec=/usr/local/webserver/mysql-57/bin/mysql
sock=$1
basedir=$2
pass=3vucOcdar8jsta23fQ1b
$exec -S $sock -e "set password for 'root'@'localhost' = password('3vucOcdar8jsta23fQ1b');"
$exec -S $sock -p$pass -e "DELETE FROM mysql.user WHERE user != 'root' OR host != 'localhost';"
$exec -S $sock -p$pass -e "DELETE FROM mysql.db;"
$exec -S $sock -p$pass -e "grant all on *.* to 'remote'@'%' identified by '13bppv3ovbe0bh5zBggY'  WITH GRANT OPTION;"
$exec -S $sock -p$pass -e "grant replication slave, replication client on *.* to 'replication'@'%' identified by 'Faw1gt2wtikpuf597Hrw'"
$exec -S $sock -p$pass -e "flush privileges;"