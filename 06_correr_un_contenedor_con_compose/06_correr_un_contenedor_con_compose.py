from invoke import Responder
from fabric import Connection
from dotenv import load_dotenv
from os import getenv
from os.path import join
from subprocess import PIPE, Popen
import requests

load_dotenv()

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

sudo_responder = Responder(
    pattern=r'\[sudo\] password',
    response=getenv('PASS')+'\n'
)

conn = Connection(host=getenv('HOST'), user=getenv('USER'), connect_kwargs={'password':getenv('PASS')})

conn.put(join('06_correr_un_contenedor_con_compose', 'docker-compose.yml'))
conn.run('sudo docker-compose up --detach', pty=True,  watchers=[sudo_responder])

try:
    response = requests.get('http://' + getenv('HOST'))
    if 'nginx' in response.text:
        print('NGINX montado exitosamente')
except Exception as e:
    print(e)
finally:
    conn.run('sudo docker-compose stop', pty=True,  watchers=[sudo_responder])
    conn.close()