# pip install qrcode

import os
import platform
import sys
import qrcode
import re

if os.getuid() != 0:
	print('\n    Need to be root, sorry.\n')
	sys.exit()

if platform.system() == 'Linux':
	ssid = str(os.popen("iwconfig wlan0").read())
	ssid = re.search('ESSID:"(.*)"', ssid)

	if ssid == None:
		print('\n    Need to be connect to Wireless Network.\n')
		sys.exit()

	ssid = str(ssid.group(1))
	hidden = str(os.popen("egrep 'hidden=' /etc/NetworkManager/system-connections/" + ssid).read())
	if hidden.find('true') != -1:
		hidden = 'True'
	else:
		hidden = 'False'
	key = str(os.popen("egrep 'key-mgmt=' /etc/NetworkManager/system-connections/" + ssid).read())
	if key.find('wpa') != -1:
		key = 'WPA'
	elif key.find('ieee8021x') != -1 or key.find('none') != -1:
		key = 'WEP'
	else:
		key = 'nopass'
	psk = str(os.popen("egrep 'psk=' /etc/NetworkManager/system-connections/" + ssid).read())
	psk = psk[4:-1]
else:
	sys.exit()
qr_text = 'WIFI:S:'+ssid+';T:'+key+';P:'+psk+';H:'+hidden+';;'
qr = qrcode.QRCode()
qr.add_data(qr_text)
qr.print_ascii()
print('    Wi-Fi Name: '+ssid+'\n')