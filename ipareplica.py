#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import sys

def ip_p(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

def my_ip_server():
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        local_socket.connect(("192.255.255.255", 1))
        my_ipv4 = local_socket.getsockname()[0]
    except:
        my_ipv4 = '127.0.0.1'
    finally:
        local_socket.close()
    return my_ipv4

def empthy_p(a_str):
    if a_str == '':
        return True

def checkroot():
    if not os.geteuid() == 0:
        sys.exit("This script run only with root privileges.")

check_root()

host_name = os.uname()[1]
print "Input the hostname: [%s]" % host_name
capture_host_name = raw_input().lower().strip()

if capture_host_name == "":
    host_name = os.uname()[1]
else:
    host_name = capture_host_name

# IPv4
ip_server_comprobation = True
while ip_server_comprobation:
    ip_server = my_ip_server()
    print "Input the IPv4 of the server: [%s]" % ip_server
    capture_ip_server = raw_input().lower().strip()
    if not empthy_p(capture_ip_server) and ip_p(capture_ip_server):
        ip_server = capture_ip_server
        ip_server_comprobation = False
    if empthy_p(capture_ip_server):
        ip_server = my_ip_server()
        ip_server_comprobation = False

dns_comprobation = True
while dns_comprobation:
    dns1 = raw_input("Input the IPv4 of the FIRST DNS forwarder: ")
    dns2 = raw_input("Input the IPv4 of the SECOND DNS forwarder: ")
    if ip_p(dns1) and ip_p(dns2):
        dns_comprobation = False
    else:
        print "Input a valid IPv4."

f = open("/etc/hosts", "a")
print>>f, ip_server, host_name
f.close()

os.system("firewall-cmd --permanent --add-port={53,80,88,111,389,443,464,636,2049,20048}/tcp")
os.system("firewall-cmd --permanent --add-port={53,88,111,123,464,2049,20048}/udp")
os.system("firewall-cmd --permanent --add-service={http,https,ldap,ldaps,kerberos,dns,ntp,nfs,mountd}")
os.system("firewall-cmd --reload")

os.system("yum -y update")
os.system("yum -y install ipa-server ipa-client ipa-server-dns bind bind-utils bind-dyndb-ldap rng-tools vim")

f = open("/etc/ntp.conf", "a")
print>>f, "restrict", ip_server
f.close()

os.system("systemctl start ntpd")
os.system("systemctl enable ntpd")
os.system("systemctl start rngd")
os.system("systemctl enable rngd")

os.system("ipa-client-install --enable-dns-updates")

cmd = []
cmd = ['ipa-replica-install', '--setup-dns', '--setup-ca', '--setup-reverse', '--forwarder='+dns1, '--forwarder='+dns2]
subprocess.call(cmd)

os.system("sed -i -e \"s/^NSSProtocol.*/NSSProtocol TLSv1\.0,TLSv1\.1/g\" /etc/httpd/conf.d/nss.conf")
os.system("systemctl restart httpd")
