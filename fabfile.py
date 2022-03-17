from invoke import task
from fabric import Connection

@task
def test(c):
    c.run('echo test from invoke')

    fab_c = Connection('localhost')
    # Local no funciona en windows con python > 3.6
    # https://github.com/fabric/fabric/issues/2142
    fab_c.local('echo test from invoke via fabric')