# raspbian-remote-sms-3g

## initialize

install a blank raspbian-lite (buster) on a clean sd card

then start locally with :

	sudo dpkg-reconfigure keyboard-configuration
	sudo reboot

then setup systemd-networkd config files to access a network, then :

	sudo systemctl enable systemd-networkd
	sudo systemctl restart systemd-networkd
	sudo systemctl enable ssh
	sudo systemctl restart ssh


## cleanup

mount /tmp and /var/tmp as ram disk

	sudo cat << EOF >> /etc/fstab
	tmpfs

remove all the crap :

	sudo apt-get purge avahi-daemon dphys-swapfile logrotate triggerhappy alsa-utils rsyslog
	sudo rm /var/swap

mount /tmp and /var/tmp as ramdisks :

	cat << EOF | sudo tee -a /etc/fstab
	tmpfs /tmp tmpfs defaults,size=32M 0 0
	tmpfs /var/tmp tmpfs defaults,size=32M 0 0
	EOF

disable unused sytemd services :

	sudo systemctl disable bluetooth.service
	sudo systemctl disable rsync.service
	sudo systemctl disable sshswitch.service
	sudo systemctl disable nfs-client.target
	sudo systemctl disable remote-fs.target
	sudo systemctl disable man-db.timer
	sudo systemctl disable apt-daily-upgrade.timer
	sudo systemctl disable apt-daily.timer


## update

update packages

	sudo apt-get update
	sudo apt-get install git screen vim tcpdump python3-venv ppp wpasupplicant
	sudo apt-get upgrade
	sudo apt-get dist-upgrade
	sudo apt-get autoremove --purge
	sudo apt-get clean


## install

go to the following folders, in order :

- wpa_supplicant
- systemd-networkd
- ppp
- cnc
- cron

for each :

- open and read content of README.txt
- change configs according to your needs
- run INSTALL.sh
