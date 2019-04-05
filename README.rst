===========
LDAP Server
===========

Abstract
--------

Creates a Docker Image, preloaded with slapd

Build
-----

.. code:: bash

  $ sudo docker build -t xnandersson/slapd .

Run: Defaults, delete on exit
------------------------------------------------

.. code:: bash

  $ sudo docker run \
    --name slapd \
    --rm \
    -d \
    -e DOMAIN=openforce.org \
    -e PASSWORD=Secret007! \
    -e ORGANIZATION="Openforce AB"\
    -p 389:389 \
    xnandersson/slapd


Run: Customized templates
------------------------------------------------------------

.. code:: bash

  $ sudo docker run \
    --name slapd \
    --rm \
    -d \
    -e DOMAIN=openforce.org \
    -e PASSWORD=Secret007! \
    -e ORGANIZATION="Openforce AB"\
    -p 389:389 \
    -v /home/${USER}/Github/xnandersson/docker-slapd/src/templates:/templates \
    xnandersson/slapd 

Package Dependencies
--------------------

.. code:: bash
    
  $ sudo apt-get install docker.io python3-venv python3-dev devscripts libldap2-dev libsasl2-dev ldap-utils -y
  $ sudo usermod -a -G docker $(whoami) 
  $ su - $USER
  $ docker pull ubuntu:latest

Pytest
------

.. code:: bash

  $ python3 -m venv ~/venv3/docker-slapd
  $ source ~/venv3/docker-slapd/bin/activate
  $ pip install -r requirements.txt
  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ pytest tests/

LDAP Search
-----------

.. code:: bash

  $ echo URL ldap://127.0.0.1 > ~/.ldaprc
  $ echo BASE DC=openforce,DC=org >> ~/.ldaprc
  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ ldapsearch -x -w Secret007! -D "cn=admin,dc=openforce,dc=org"
  $ ldapsearch -x -w secret -D "uid=nandersson,ou=Users,dc=openforce,dc=org"
