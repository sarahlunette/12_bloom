#!/bin/bash

#cat /${PROJECT_DIR}/.env >> /etc/environment

# Store all APP_BLOOM ENV variables to local file accessible to current user to share them with cron task
# Due to the fact that cron process doesn't access to declared ENV vars and doesn't load user profiles
# The entrypoint.sh script stores ENV vars at runtime in the ~/.env file as key=value pairs
# Then the cron line include some command to load these ENV vars from file before launching app.py
# This mecanism allows to give access to the same ENV vars for app.py launch in terminal and launch via cron
env | egrep '^(PYTHONPATH|POSTGRES_.*|SPIRE_TOKEN.*|DATA_FOLDER.*)' > /root/.env

#echo "Starting Rsyslog service"
/etc/init.d/rsyslog restart
#echo "Rsyslog started"

ln -sf /proc/1/fd/1 /var/log/syslog
ln -sf /proc/1/fd/1 /dev/stdout
ln -sf /proc/1/fd/2 /dev/stderr

#source /${PROJECT_DIR}/.env

# execute CMD
echo "$@"
exec "$@"
