import pytest
import ldap

def test_slapd(slapd):
    con = ldap.initialize('ldap://127.0.0.1')
    con.protocol_version = ldap.VERSION3
    con.simple_bind_s('cn=admin,dc=openforce,dc=org', 'Secret007!')
    dn = 'cn=admin,dc=openforce,dc=org'
    attr_name = 'cn'
    attr_val = 'admin'
    assert con.compare_s(dn, attr_name, attr_val) == True
