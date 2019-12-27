#!/bin/sh
sudo ln -v -f -s $(git rev-parse --show-toplevel)/ppp-freemobile/ /etc/ppp/ && \
sudo ln -v -f -s /etc/ppp/ppp-freemobile/freemobile /etc/ppp/peers/freemobile
