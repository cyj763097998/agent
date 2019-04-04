#!/bin/bash
port=$1
username=$2
password=$3
db=$4
mongo_exe='/usr/local/webserver/percona-mongodb32/bin/mongo'
$mongo_exe 127.0.0.1:$port <<EOF
use admin
db.auth('remote','qSDH@MoS')
use $db
db.createUser({user: "$username",pwd: "$password",roles: [{ role: "dbOwner",db: "$db"}]})
EOF
