# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:12:50 2023

@author: Cameron
"""

# Importing all of the required modules.
import subprocess
import pywifi
from pywifi import const
import time
import requests
import json
import psutil

# The start of the program will begin with the below prompt.
print("[Please wait up to 3 minutes for the program to discover your network parameters.] [0/4]\n")

#The message variable is reset to be empty.
message = ""

#The first function, uses the subprocess to discover the 4 specific variables below.
wifi_scan = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
#If not network is found the message below will write to the messages variable.
if "disconnected" in wifi_scan.stdout:
    message += "You are not connected to any network.\n"
#Otherwise the connected SSID is split from the output of the first function and added to the message.
else:
    connected_network = wifi_scan.stdout.split("SSID                   : ")[1].split("\n")[0].strip()
    message += f"You are connected to: {connected_network}\n"

    wifi_scan = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True)
    output_lines = wifi_scan.stdout.split("\n")

#This loops through the output of the function and checks the SSID is th same as the previous connected_network variable
#then prints the security protocol for this SSID.
    for i in range(0, len(output_lines)):
        if "SSID" in output_lines[i]:
            ssid = output_lines[i].split(":")[1].strip()
            security = output_lines[i+2].split(":")[1].strip()
            if ssid == connected_network:
                message += f"Security protocol for {ssid}: {security}\n"

# Determines IP address of current machine on network.
ip_scan = subprocess.run(["ipconfig"], capture_output=True, text=True)
for line in ip_scan.stdout.splitlines():
    if "IPv4 Address" in line:
        ip_address = line.split(":")[1].strip()
#Split the IP from the data and adds to the message.
message += "IP Address: "+ip_address + "\n"

# Performs a port scan using NMAP using the IP obtained previously.
nmap_path = r'C:\Program Files (x86)\Nmap\nmap.exe'
port_scan = subprocess.run([nmap_path, "-sS", ip_address], capture_output=True, text=True)

# Parse NMAP output to get open ports in a list.
open_ports = []
for line in port_scan.stdout.splitlines():
    if "/tcp" in line and "open" in line:
        open_ports.append(line.split("/")[0])

print("Stage 1 Complete...[1/4]")

message += str(open_ports) + '\n'

# For each open port, run service version detection using NMAP.
for port in open_ports:
    service_scan = subprocess.run([nmap_path, "-sV", "-p", port, ip_address], capture_output=True, text=True)
    for line in service_scan.stdout.splitlines():
        if "Service Info:" in line:
            service_info = line.split(":")[1].strip()
            message += f"Port {port} ({service_info})\n"

print("Stage 2 Complete...[2/4]")

# Using the PyWiFi module
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0] # Assuming only one WiFi interface is available
iface.scan() # Scan for available networks
time.sleep(5) # Wait for the scan to complete
results = iface.scan_results() # Store results
desired_ssid = connected_network #Match the connected network to the desired network.
found_desired_network = False

# Search through results of network scan and add the SSID, Signal Strength and Security to the message.
for network in results:
    if network.ssid == desired_ssid:
        if not found_desired_network:
            message += f"SSID: {network.ssid}\n"
            message += f"Signal Strength: {network.signal}\n"
            if isinstance(network.akm, (list, tuple)) and network.akm[0] == const.AKM_TYPE_NONE:
                message += "Security: Open\n"
            elif isinstance(network.akm, (list, tuple)) and network.akm[0] == const.AKM_TYPE_WPA2PSK:
                message += "Security: Private\n"
                if isinstance(network.cipher, (list, tuple)):
                    message += f"Encryption: {network.cipher[0]}\n"
            found_desired_network = True
        else:
            break

print("Stage 3 Complete...[3/4]")

# VPN discovery using PSUtil
adapters = psutil.net_if_stats().keys()
# If the adapter contains VPN in it and is connected it will discover as a active VPN.
for adapter in adapters:
    if "VPN" in adapter:
        message += "VPN: You are on a VPN\n"
        break
else:
    message += "VPN: You are not on a VPN\n"

print("Stage 4 Complete...[4/4]\n")

# Split message into lines
message_lines = message.split('\n')

# Send each line as a separate request
for line in message_lines:
    if line:
        data = {'message': line}
        response = requests.post('http://cameronmuihread.pythonanywhere.com/send_message', json=data, stream=True)
        print(response.text)
        response.raise_for_status()

        for content_chunk in response.iter_content(chunk_size=1024):
            if content_chunk:
                # process the content chunk as needed
                pass
        
print("\nTo see your results please navigate to: http://cameronmuihread.pythonanywhere.com")