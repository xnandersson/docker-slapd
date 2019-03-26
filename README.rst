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
    
  $ sudo apt-get install docker.io
  $ sudo usermod -a -G docker nandersson
  $ docker pull ubuntu:latest

Install
-------

.. code:: bash

  $ python3 -m venv ~/venv3/docker-slapd
  $ source ~/venv3/docker-slapd/bin/activate
  $ pip install -r requirements.txt
  $ python src/docker-slapd.py
  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ pytest
