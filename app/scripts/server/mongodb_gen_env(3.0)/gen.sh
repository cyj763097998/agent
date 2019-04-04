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
# mongod.conf, Percona Server for MongoDB
# for documentation of all options, see:
#   http://docs.mongo.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: $BASEDIR/data
  journal:
    enabled: true
#  engine: mmapv1
  engine: PerconaFT
#  engine: rocksdb
#  engine: wiredTiger
#  directoryPerDB: true

# Storage engine various options
#  mmapv1:
#  wiredTiger:
  PerconaFT:

    collectionOptions:
      compression: quicklz
      fanout: 128
      readPageSize: 16384

    indexOptions:
      compression: quicklz
      fanout: 128
      readPageSize: 16384

    engineOptions:
      cacheSize: 10737418240

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: $BASEDIR/logs/mongodb.log
  component:
    query:
      verbosity: 1

processManagement:
  fork: true
  pidFilePath: $BASEDIR/mongod.pid

# network interfaces
net:
  port: $PORT
  bindIp: 0.0.0.0
  maxIncomingConnections: 65536
  unixDomainSocket:
    enabled: true
    pathPrefix: $BASEDIR

#security:
  #keyFile: $BASEDIR/mongod-keyfile
  #authorization: enabled

operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp

#replication:

#sharding:

## Enterprise-Only Options:

#auditLog:

#snmp:
EOF
}

gen_dir
chmod +x secure.sh
./secure.sh $PORT


