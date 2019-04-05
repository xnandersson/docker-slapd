import docker
import ldap
import pytest
import time 


@pytest.fixture
def slapd(tmpdir):
  environment = {
	'DOMAIN': 'openforce.org',
	'PASSWORD': 'Secret007!',
	'ORGANIZATION': 'Openforce AB',
  }
  ports = {
	'389': 389,
  }
  client = docker.from_env()
  c = None
  if not client.containers.list(all, filters={'name': 'slapd'}):
    c = client.containers.run('xnandersson/slapd', command='run.py', ports=ports, name='slapd', environment=environment, detach=True)
    time.sleep(10)
  else:
    c = client.containers.get('slapd')
    c.start()
    time.sleep(2)
  yield
  c.kill()
  c.remove()
