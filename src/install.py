#!/usr/bin/env python3
from jinja2 import Template
import os
import subprocess

DOMAIN = os.getenv('DOMAIN', 'acme.org')
PASSWORD = os.getenv('PASSWORD', 'Secret012')
ORGANIZATION = os.getenv('ORGANIZATION', 'Acme Ltd')

def install_slapd(domain=None, password=None, organization=None):
    t = Template(open('/tmp/slapd.debconf.jinja2').read())
    with open('/tmp/slapd.debconf', 'w') as f:
        f.write(t.render(
                    domain = domain,
                    password = password,
                    organization = organization))
    proc = subprocess.Popen(['debconf-set-selections', '/tmp/slapd.debconf'], stderr=open(os.devnull, 'w'))
    proc.wait()
    proc = subprocess.Popen(['apt-get', 'install', 'slapd', 'ldap-utils', '-y'], stderr=open(os.devnull, 'w'))
    proc.wait()
    proc = subprocess.Popen(['slapadd', '-v', '-F', '/etc/ldap/slapd.d/', '-l', '/tmp/sudo.ldif', '-b', 'cn=config'])
    proc.wait()
    t = Template(open('/tmp/domain.ldif.jinja2').read())
    with open('/tmp/domain.ldif', 'w') as f:
        f.write(t.render(
            dc = domain.split('.')[0],
            tld = domain.split('.')[1]
        ))
    proc = subprocess.Popen(['slapadd', '-l', '/tmp/domain.ldif'])
    proc.wait()
    t = Template(open('/tmp/nandersson.ldif.jinja2').read())
    with open('/tmp/nandersson.ldif', 'w') as f:
        f.write(t.render(
                    dc = domain.split('.')[0],
                    tld = domain.split('.')[1]
        ))
    proc = subprocess.Popen(['slapadd', '-l', '/tmp/nandersson.ldif'])
    proc.wait()
    proc = subprocess.Popen(['chown', '-R', 'openldap:openldap', '/var/lib/ldap'])
    proc.wait()
    proc = subprocess.Popen(['chmod', '-R', '0600', '/var/lib/ldap/'])
    proc.wait()
    proc = subprocess.Popen(['chmod', '0700', '/var/lib/ldap'])
    proc.wait()
    proc = subprocess.Popen(['chown', '-R', 'openldap:openldap', '/etc/ldap/slapd.d/'])
    proc.wait()
    t = Template(open('/tmp/ldap.conf.jinja2').read())
    with open('/etc/ldap/ldap.conf', 'w') as f:
        f.write(t.render(
            dc = domain.split('.')[0],
            tld = domain.split('.')[1]
        ))

def slapd():
#proc = subprocess.Popen(["/usr/sbin/slapd", "-d", "5", "-h", "'ldap:/// ldapi:///'", "-g", "openldap", "-u", "openldap", "-F", "/etc/ldap/slapd.d"])
    proc = subprocess.Popen(['/usr/sbin/slapd', '-d', '5', '-h', 'ldap:/// ldapi:///', '-g', 'openldap', '-u', 'openldap', '-F', '/etc/ldap/slapd.d'])
    proc.wait()

if __name__ == '__main__':
    install_slapd(domain=DOMAIN, password=PASSWORD, organization=ORGANIZATION)
    slapd()
