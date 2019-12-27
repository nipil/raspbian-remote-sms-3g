# config

you'll certainly have to
- change modem device 'modem-3g.options'
- change provider APN in 'modem-3g.apn'
- change PIN info in 'modem-3g.pin'

change other settings according to your use case

and if your provider needs authentication, read ppp manual and update configuration accordingly

# install

run INSTALL.sh (which use sudo to install ppp config files and symlinks)

# test

start with 'sudo pon'
check routing table with 'ip route' default route should go throug ppp0
test real connectivity with 'ping 8.8.8.8'
stop with 'sudo poff'
