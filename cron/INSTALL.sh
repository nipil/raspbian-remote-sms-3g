#!/bin/sh

NAME=raspbian-remote-sms-3g-cron.sh
TARGET=/usr/local/bin

INSTALL_DIR=$(git rev-parse --show-toplevel)

sudo rm -f ${TARGET}/${NAME} && \
sed "s#INSTALL_SCRIPT_WILL_REPLACE_BY_GIT_REPO_BASE_DIR#${INSTALL_DIR}#" cron.sh | sudo tee ${TARGET}/${NAME} >/dev/null && \
sudo chmod +x ${TARGET}/${NAME} && \
crontab crontab.txt
