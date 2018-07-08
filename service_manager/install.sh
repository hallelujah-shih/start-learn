#!/bin/bash

WORKDIR=`pwd`

cd /opt
wget https://cr.yp.to/daemontools/daemontools-0.76.tar.gz
tar xzvf daemontools-0.76.tar.gz

# 打patch
echo gcc -O2 -include /usr/include/errno.h > admin/daemontools-0.76/src/conf-cc
cd admin/daemontools-0.76/
package/install

cp $WORKDIR/daemontools.service /usr/lib/systemd/system/daemontools.service

systemctl enable daemontools
systemctl start daemontools
