#!/bin/bash
set -o nounset
set -o errexit

PORT=$1
BASEDIR=$2
DATADIR=${BASEDIR}/data
LOGDIR=${BASEDIR}/logs
SCRIPTS_DIR=`dirname $0`


function gen_dir(){
if [ -e $BASEDIR ]
then
 echo "The $PORT instance is exist!"
else
 cp -r ${SCRIPTS_DIR}/99999.demo  $BASEDIR
 sed -i "18,18 s#mongod.conf#`echo $BASEDIR`\/mongod.conf#g" ${BASEDIR}/mongod
 gen_config
 chown mongod.mongod $BASEDIR -R
fi
}

function gen_config(){
cat >>${BASEDIR}/mongod.conf <<EOF 
### GENERAL ###
bind_ip = 0.0.0.0
port    = $PORT
pidfilepath      = ${BASEDIR}/mongod.pid
unixSocketPrefix = $BASEDIR
fork             = true

### DATA STORAGE ###
dbpath          = $DATADIR
directoryperdb  = true
journal = true

### LOG ###
oplogSize = 1024
# QUERY LOG #
logpath         = ${LOGDIR}/mongodb.log
logappend       = true

# SLOWLOG #
profile          = 0 
#slowms  = 1000

### LIMITS ###
maxConns        = 20000

### SAFETY ###
#auth = true
#noauth = true

### REPLICATION ###
#replSet                = repl
#master           = true
slave           = true
source          = 0.0.0.0:0
autoresync      = true
keyFile 	= $/keyfile
EOF
}

gen_dir
chmod +x secure.sh
./secure.sh $PORT $BASEDIR


