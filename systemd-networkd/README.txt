# config

you'll maybe have to change the device name :
- in section [Match] of '50-wired.network'
- in section [Match] of '60-wifi-test.network'

for infomation, when developping/debugging, i use wifi
so the '60-wifi-test.network' file is only there to autostart
wifi in that use case, where i can verify lan
connectivity and ip masquerading

production use case is using only wired (and ppp of course)

# install

run INSTALL.sh (which use sudo to install ppp config files)
