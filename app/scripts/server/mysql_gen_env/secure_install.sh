

sock=$1
mysql -S $sock -e "drop database test;"
mysql -S $sock -e "DELETE FROM mysql.user WHERE user != 'root' OR host != 'localhost';"
mysql -S $sock -e "DELETE FROM mysql.db;"
mysql -S $sock -e "grant all on *.* to 'remote'@'%' identified by '13bppv3ovbe0bh5zBggY'  WITH GRANT OPTION;"
mysql -S $sock -e "set password for 'root'@'localhost' = password('3vucOcdar8jsta23fQ1b');"
mysql -S $sock -e "flush privileges;"
