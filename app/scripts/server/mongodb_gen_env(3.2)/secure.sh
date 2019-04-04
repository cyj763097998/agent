port=$1
basedir=$2
exe='/usr/local/webserver/percona-mongodb32/bin/mongo'
$basedir/mongod start
$exe 127.0.0.1:$1 <<EOF
use admin
db.createUser({user: "remote",pwd: "qSDH@MoS",roles: [ { role: "root", db: "admin" } ]});
EOF
$basedir/mongod stop
config=$basedir/mongod.conf
sed -i 's/^.*security.*/security:/g' $config
sed -i 's/^.*authorization.*/   authorization: enabled/g' $config
$basedir/mongod start
