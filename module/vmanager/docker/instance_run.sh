#!/bin/bash

# start python web
cd /service/vfc/nfvo/driver/vnfm/svnfm/certus/vmanager
chmod +x run.sh
./run.sh

# start mysqld
# /etc/init.d/mysql start

while [ ! -f logs/runtime_driver.log ]; do
    sleep 1
done
tail -F logs/runtime_driver.log