FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2019-03-26
RUN apt-get update -yqq
RUN apt-get install ldap-utils python3-jinja2 -yqq
COPY templates /templates
ADD install.py /usr/local/bin/install.py
RUN chmod +x /usr/local/bin/install.py
EXPOSE 22 389 636
CMD /usr/local/bin/install.py
