#!/usr/bin/env python3
from jinja2 import Template
import os
import subprocess

DOMAIN = os.getenv('DOMAIN', 'acme.org')
PASSWORD = os.getenv('PASSWORD', 'Secret012')
ORGANIZATION = os.getenv('ORGANIZATION', 'Acme Ltd')

def install_slapd(domain=None, password=None, organization=None):
    t = Template(open('/templates/slapd.debconf.jinja2').read())
    with open('/tmp/slapd.debconf', 'w') as f:
        f.write(t.render(
                    domain = domain,
                    password = password,
                    organization = organization))
    proc = subprocess.Popen(['debconf-set-selections', '/tmp/slapd.debconf'], stderr=open(os.devnull, 'w'))
    proc.wait()
    proc = subprocess.Popen(['apt-get', 'install', 'slapd', 'ldap-utils', '-y'], stderr=open(os.devnull, 'w'))
    proc.wait()
    proc = subprocess.Popen(['slapadd', '-v', '-F', '/etc/ldap/slapd.d/', '-l', '/templates/sudo-schema.ldif', '-b', 'cn=config'])
    proc.wait()
    t = Template(open('/templates/dit.ldif.jinja2').read())
    with open('/tmp/dit.ldif', 'w') as f:
        f.write(t.render(
            dc = domain.split('.')[0],
            tld = domain.split('.')[1]
        ))
    proc = subprocess.Popen(['slapadd', '-l', '/tmp/dit.ldif'])
    proc.wait()
    t = Template(open('/templates/fixture.ldif.jinja2').read())
    with open('/tmp/fixture.ldif', 'w') as f:
        f.write(t.render(
                    dc = domain.split('.')[0],
                    tld = domain.split('.')[1]
        ))
    proc = subprocess.Popen(['slapadd', '-l', '/tmp/fixture.ldif'])
    proc.wait()
    proc = subprocess.Popen(['chown', '-R', 'openldap:openldap', '/var/lib/ldap'])
    proc.wait()
    proc = subprocess.Popen(['chmod', '-R', '0600', '/var/lib/ldap/'])
    proc.wait()
    proc = subprocess.Popen(['chmod', '0700', '/var/lib/ldap'])
    proc.wait()
    proc = subprocess.Popen(['chown', '-R', 'openldap:openldap', '/etc/ldap/slapd.d/'])
    proc.wait()
    t = Template(open('/templates/ldap.conf.jinja2').read())
    with open('/etc/ldap/ldap.conf', 'w') as f:
        f.write(t.render(
            dc = domain.split('.')[0],
            tld = domain.split('.')[1]
        ))

def slapd():
    proc = subprocess.Popen(['/usr/sbin/slapd', '-d', '5', '-h', 'ldap:/// ldapi:///', '-g', 'openldap', '-u', 'openldap', '-F', '/etc/ldap/slapd.d'])
    proc.wait()

if __name__ == '__main__':
    if not os.path.isdir('/var/lib/ldap'):
        install_slapd(domain=DOMAIN, password=PASSWORD, organization=ORGANIZATION)
    slapd()
