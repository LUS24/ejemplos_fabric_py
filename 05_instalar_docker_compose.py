# Instalar docker de acuerdo a
# https://docs.docker.com/engine/install/ubuntu/

from invoke import Responder
from fabric import Connection
from dotenv import load_dotenv
from os import getenv

load_dotenv()

conn = Connection(
    host=getenv('HOST'),
    user=getenv('USER'),
    connect_kwargs= {'password': getenv('PASS')},
    )

responder_sudo = Responder(
    pattern=r"\[sudo\] password",
    # Se necesita el \n al final para simular ENTER
    response=getenv('PASS')+"\n"
)

print("--------------------------- DESCARGANDO EL EJECUTABLE DE DOCKER COMPOSE")

# Para usar imagenes alpine se necesitan más dependencias
# Ver detalle en https://docs.docker.com/compose/install/#install-compose-on-linux-systems

DOCKER_COMPOSE_VERSION = "1.29.2"

conn.run(
    command=f'sudo curl -L "https://github.com/docker/compose/releases/download/{DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose',
    pty=True, 
    watchers=[responder_sudo]
)


print("--------------------------- APLICANDO PERMISOS DE EJECUCIÓN")


conn.run(
    command='sudo chmod +x /usr/local/bin/docker-compose',
    pty=True, 
    watchers=[responder_sudo]
)


print("--------------------------- VERIFICANDO INSTALACIÓN")

result = conn.run(
    command='docker-compose --version',
    pty=True, 
    watchers=[responder_sudo]
)

if f'docker-compose version {DOCKER_COMPOSE_VERSION}' in result.stdout:
    print('Se ha instalado docker exitosamente')