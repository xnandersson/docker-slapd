===========
LDAP Server
===========

Abstract
--------

Creates a Docker Image, preloaded with slapd

.. code:: bash

  $ docker run \
    --name slapd \
    --rm \
    -ti \
    -e DOMAIN=openforce.org \
    -e PASSWORD=Secret007! \
    -e ORGANIZATION="Openforce AB"\
    -p 389:389 \
    xnandersson/slapd /usr/local/bin/install.py


Prerequisites
-------------

.. code:: bash
    
  $ sudo apt-get install docker.io ldap-utils
  $ sudo usermod -a -G docker $(whoami) 
  $ su - $USER
  $ docker pull ubuntu:latest


Docker Build Option
-------------------

.. code:: bash

  $ docker build . -t xnandersson/slapd


Python Build Option
-------------------

.. code:: bash

  $ python3 -m venv ~/venv3/docker-slapd
  $ source ~/venv3/docker-slapd/bin/activate
  $ pip install -r requirements.txt
  $ python src/docker-slapd.py
  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ pytest

Testing
-------

.. code:: bash

  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ ldapsearch
