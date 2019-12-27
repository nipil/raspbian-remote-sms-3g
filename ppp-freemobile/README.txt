# install

run INSTALL.sh (which use sudo to install pppd symlinks)

# config

change modem device on first line of options-freemobile file

# test

start with 'sudo pon'
check routing table with 'ip route' default route should go throug ppp0
test real connectivity with 'ping 8.8.8.8'
stop with 'sudo poff'
