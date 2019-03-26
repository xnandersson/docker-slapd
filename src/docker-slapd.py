#!/usr/bin/env python
import docker
import os
import shutil
import uuid

BUILD_DIR = '/tmp/{uuid}/'.format(uuid=uuid.uuid4().hex)

def mkdir_build_dir():
    try:
        os.mkdir(BUILD_DIR)
    except FileExistsError as e:
        pass

def copy_files_to_build_dir():
    shutil.copy('slapd.debconf.jinja2', os.path.join(BUILD_DIR, 'slapd.debconf.jinja2'))
    shutil.copy('slapd.debconf.jinja2', os.path.join(BUILD_DIR, 'slapd.debconf.jinja2'))
    shutil.copy('sudo.ldif', os.path.join(BUILD_DIR, 'sudo.ldif'))

def create_dockerfile():
    with open(os.path.join(BUILD_DIR, 'Dockerfile'), 'w') as f:
        f.write("""FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2019-03-26
RUN apt-get update -yqq
RUN apt-get install python3-jinja2 -yqq
ADD slapd.debconf.jinja2 /tmp/slapd.debconf.jinja2
ADD install.py /usr/local/bin/install.py
RUN chmod +x /usr/local/bin/install.py
EXPOSE 22 389 636
CMD /bin/bash""")

if __name__ == '__main__':
    mkdir_build_dir()
    copy_files_to_build_dir()
    create_dockerfile()
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    client.images.build(path=BUILD_DIR, tag='xnandersson/slapd', rm=True, pull=True)
