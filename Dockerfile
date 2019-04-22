FROM ubuntu:latest
MAINTAINER Niklas Andersson <niklas.andersson@openforce.se>
ENV UPDATED_ON 2019-03-26
RUN apt-get update -yqq
RUN apt-get install ldap-utils python3-jinja2 -yqq
RUN apt-get install --download-only slapd -yqq
COPY src/templates /templates
ADD src/run.py /usr/local/bin/run.py
RUN chmod +x /usr/local/bin/run.py
EXPOSE 22 389 636
CMD /usr/local/bin/run.py
