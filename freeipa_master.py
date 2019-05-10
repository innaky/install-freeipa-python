#!/usr/bin/python

import os
import string
import socket
import subprocess
import sys

# help func
def checkroot():
    if not os.geteuid() == 0:
        sys.exit("This script run only with root privileges.")

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

def ip_p(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

def long_ranges(a_lst):
    if len(a_lst) == 3:
        return True

def netmask_comprobation(a_lst):
    if a_lst[1] == "netmask":
        return True

def ip_comprobation(a_lst):
    if ip_p(a_lst[0]) and ip_p(a_lst[2]):
        return True

def space_p(a_str):
    if a_str.strip() != "":
        return True

def empthy_p(a_str):
    if a_str == '':
        return True

def add_ipv4_hosts(ip_input):
    f = open("/etc/hosts", "a")
    print>>f, ip_input, host_name
    f.close()

def set_hostname(new_hostname):
    cmd = ['hostnamectl', 'set-hostname', new_hostname]
    subprocess.call(cmd)

def list_netdevices():
    command = "ip a | awk '{print$2,$4}' | awk '{print$1}' | sed 's/forever//g' | grep -v "'".*::.+*"'""
    subprocess.call(command, shell=True)

def modify_net(ipv4, netmask, gateway, dns1):
    cmd = ['sed', '-i', '/etc/sysconfig/netwok-scripts/']

def check_netfile(file_name):
    basepath = '/etc/sysconfig/network-scripts/ifcfg-'
    truepath = basepath + file_name
    boolean = os.path.isfile(truepath)
    return boolean

def modify_net_interface(interface_name, ipv4, gateway, mask):
    basepath = '/etc/sysconfig/network-scripts/ifcfg-'
    truepath = basepath + interface_name
    delip = "sed -i '/IPADDR/d' %s > /dev/null 2>&1" % truepath
    subprocess.call(delip, shell=True)
    delgateway = "sed -i '/GATEWAY/d' %s > /dev/null 2>&1" % truepath
    subprocess.call(delgateway, shell=True)
    delmask = "sed -i '/PREFIX/d' %s > /dev/null 2>&1" % truepath
    subprocess.call(delmask, shell=True)
    ip_concat = "IPADDR=\"" + ipv4 + "\""
    gw_concat = "GATEWAY=\"" + gateway + "\""
    mask_concat = "PREFIX=\"" + mask + "\""
    input_ip = "echo %s >> %s > /dev/null 2>&1" % (ip_concat, truepath)
    subprocess.call(input_ip, shell=True)
    f = open(truepath, "a")
    print>>f, ip_concat
    print>>f, gw_concat
    print>>f, mask_concat
    f.close()
    restart = ['systemctl', 'restart', 'network.service']
    subprocess.call(restart)

def reverse_zone(ipv4):
    split = ipv4.split(".")[:-1]
    split.reverse()
    zone_rev = split[0] + "." + split[1] + "." + split[2] + "." + "in-addr.arpa."
    return zone_rev

#
## main
#

checkroot()

print("##################### Warning! ##################\n")
print("Run this script only in a new installation of CentOS 7.\n")

# hostname
host_name = os.uname()[1]
print "Input the hostname: [%s]" % host_name
capture_host_name = raw_input().lower().strip()

if capture_host_name == "":
    host_name = os.uname()[1]
else:
    set_hostname(capture_host_name)
    host_name = os.uname()[1]

#
## net
#

# ipv4
ip_server_comprobation = True
while ip_server_comprobation:
    ip_server = my_ip_server()
    print "Input the IPv4 of the server: [%s]" % ip_server
    capture_ip_server = raw_input().lower().strip()
    if not empthy_p(capture_ip_server) and ip_p(capture_ip_server):
        print("########## Important ########\n")
        print("If you change the IPv4 you will lost the connection\n")
        print("##############################\n")
        print("Red configuration.\n")
        print("Your nics: \n")
        list_netdevices()
        capture_device = raw_input("Input the network device name: ").lower().strip()
        check_net_device = True
        while check_net_device:
            if check_netfile(capture_device) and capture_device != "lo":
                check_net_device = False
            else:
                print("This device not exist and you cant select the loopback, please select one of the list.\n")
                list_netdevices()
                capture_device = raw_input("Input the network device name: ").lower().strip()
        ip_gateway = raw_input("Input the IPv4 of the gateway: ").lower().strip()
        check_gateway = True
        while check_gateway:
            if ip_p(ip_gateway):
                check_gateway = False
            else:
                print("The IPv4 of the gateway is invalid, please input a valid IPv4: ")
                ip_gateway = raw_input("Input the IPv4 of the gateway: ").lower().strip()
        check_mask = True
        mask = raw_input("Input the IPv4 mask: ")
        modify_net_interface(capture_device, capture_ip_server, ip_gateway, mask)
        add_ipv4_hosts(capture_ip_server)
        reversee = reverse_zone(capture_ip_server)
        ip_server_comprobation = False
    if empthy_p(capture_ip_server):
        ip_server = my_ip_server()
        add_ipv4_hosts(ip_server)
        reversee = reverse_zone(ip_server)
        ip_server_comprobation = False

# Domain
domain_name = raw_input("Input the domain name: ").lower().strip()

# REALM
realm = domain_name.upper().strip()

# IPv4 segment
comprobation = True
while comprobation:
    print "\nEnter the segment that will listen to this service.(ntp), \nex: 192.168.122.0 netmask 255.255.255.0"
    rang_listen = raw_input().lower().strip().split()
    if long_ranges(rang_listen) and netmask_comprobation(rang_listen) and ip_comprobation(rang_listen):
        comprobation = False
rangos_str = rang_listen[0] + ' ' + rang_listen[1] + ' ' + rang_listen[2]

# pass
pass_comprobation = True
while pass_comprobation:
    password = raw_input("Input the password of the service: ")
    if space_p(password):
        pass_comprobation = False
    else:
        print "You cant use an empty password\n"

# local DNS
dns_comprobation = True
while dns_comprobation:
    dns_forward = raw_input("Input your IPv4 of the local DNS: ")
    if ip_p(dns_forward):
        dns_comprobation = False
    else:
        print "Input a valid IPv4.\n"

zone_hrs = subprocess.Popen("timedatectl | grep \"Time zone\"", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
print "Your timezone is: %s" % zone_hrs

os.system("yum -y update")
os.system("yum -y upgrade")

# firewall
os.system("firewall-cmd --permanent --add-port={53,80,88,111,389,443,464,636,2049,20048}/tcp")
os.system("firewall-cmd --permanent --add-port={53,88,111,123,464,2049,20048}/udp")
os.system("firewall-cmd --permanent --add-service={http,https,ldap,ldaps,kerberos,dns,ntp,nfs,mountd}")
os.system("firewall-cmd --reload")

# packages
os.system("yum -y update")
os.system("yum -y install ipa-server ipa-server-dns bind bind-utils bind-dyndb-ldap rng-tools vim")

# NTP conf
f = open("/etc/ntp.conf", "a")
print>>f, "restrict", rangos_str
f.close()
os.system("systemctl start ntpd")
os.system("systemctl enable ntpd")

# rngd conf
os.system("systemctl start rngd")
os.system("systemctl enable rngd")

cmd = []
cmd = ['ipa-server-install', '--ds-password='+password, '--admin-password='+password, '--domain='+domain_name, '--realm='+realm, '--hostname='+host_name, '--setup-dns', '--auto-reverse', '--forwarder='+dns_forward]
subprocess.call(cmd)

os.system("sed -i -e \"s/^NSSProtocol.*/NSSProtocol TLSv1\.0,TLSv1\.1/g\" /etc/httpd/conf.d/nss.conf")
os.system("systemctl restart httpd")

f = open("/etc/resolv.conf", "w")
print>>f, "search", domain_name
print>>f, "nameserver", ip_server
f.close()

os.system('echo %s | kinit admin > /dev/null 2>&1' % password)
os.system("ipa dnsconfig-mod --allow-sync-ptr=TRUE")

server_reverse = "ipa dnszone-mod %s --allow-sync-ptr=TRUE" % reversee
subprocess.call(server_reverse, shell=True)
