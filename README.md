# FreeIPA Python
This scripts install freeipa on CentOS 7 and one replica.

It's important connection between CentOS 7 systems.

# Usage (freeipa_master)
Install Centos 7 base

```bash
git clone https://github.com/innaky/install-freeipa-python.git
chmod +x freeipa_master.py
./freeipa_master.py
```

# Usage (ipareplica.py)
cd install-freeipa-python
chmod +x ipareplica.py
./ipareplica.py
```

# What is FreeIPA?
FreeIPA is an integrated security information management solution
combining Linux (Fedora), 389 Directory Server, MIT Kerberos, NTP,
DNS, Dogtag (Certificate System). It consists of a web interface
and command-line administration tools.

FreeIPA is an integrated Identity and Authentication solution
for Linux/UNIX networked environments. A FreeIPA server provides
centralized authentication, authorization and account information
by storing data about user, groups, hosts and other objects
necessary to manage the security aspects of a network of computers.

FreeIPA is built on top of well known Open Source components and standard
protocols with a very strong focus on ease of management and automation
of installation and configuration tasks.

Multiple FreeIPA servers can easily be configured in a FreeIPA
Domain in order to provide redundancy and scalability. The 389 Directory
Server is the main data store and provides a full multi-master LDAPv3
directory infrastructure. Single-Sign-on authentication is provided
via the MIT Kerberos KDC. Authentication capabilities are augmented by an
integrated Certificate Authority based on the Dogtag project.
Optionally Domain Names can be managed using the integrated ISC Bind server.

Security aspects related to access control, delegation of administration
tasks and other network administration tasks can be fully centralized
and managed via the Web UI or the ipa Command Line tool.
(https://www.freeipa.org/page/About).

# License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)