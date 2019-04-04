#!/bin/bash
port=$1
db=$2
mongo_exe='/usr/local/webserver/percona-mongodb32/bin/mongo'
$mongo_exe 127.0.0.1:$port <<EOF
use admin
db.auth('remote','qSDH@MoS')
use $db
EOF
