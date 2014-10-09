from fabric.api import *

@task
def multiecho(sayit,count):
  for i in range(0,int(count)):
    local("echo %s" % sayit)


@task
def host_and_date():
  local("hostname")
  local("date")
