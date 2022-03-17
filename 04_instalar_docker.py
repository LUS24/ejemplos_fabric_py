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

responder_yes = Responder(
    pattern=r"\[Y/n\]",
    # Se necesita el \n al final para simular ENTER
    response=getenv('PASS')+"\n"
)

print("--------------------------- QUITANDO VERSIONES ANTIGUAS DE DOCKER")

try:
    conn.run(
        command='sudo apt-get remove -y docker docker-engine docker.io containerd runc',
        pty=True, 
        watchers=[responder_sudo, responder_yes]
    )
except Exception as e:
    print(e)

print("--------------------------- ACTUALIZANDO REPOSITORIO DE PAQUETES")
try:
    conn.run(
        command='sudo apt-get update',
        pty=True, 
        watchers=[responder_sudo]
    )
except Exception as e:
    print(e)


print("--------------------------- INSTALANDO DEPENDENCIAS PAQUETES PARA PODER USAR EL REPO MEDIANTE HTTPS")

try:
    conn.run(
        command='sudo apt-get install -y ca-certificates curl gnupg lsb-release',
        pty=True, 
        watchers=[responder_sudo]
    )
except Exception as e:
    print(e)

print("--------------------------- AGREGANDO CLAVE GPG OFICIAL DE DOCKER")


conn.run(
    'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg',
    pty=True, 
    watchers=[responder_sudo]
)


print("--------------------------- AGREGANDO REPOSITORIO DE LA VERSIÓN ESTABLE DE DOCKER")

conn.run(
    'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
    pty=True, 
    watchers=[responder_sudo]
)


print("--------------------------- ACTUALIZANDO REPOSITORIO DE PAQUETES INCLUYENDO REPO NUEVO")

conn.run(
    command='sudo apt-get update',
    pty=True, 
    watchers=[responder_sudo]
)


print("--------------------------- INSTALANDO DOCKER ENGINE")


conn.run(
    command='sudo apt-get install -y docker-ce docker-ce-cli containerd.io',
    pty=True, 
    watchers=[responder_sudo]
)

print("--------------------------- VERIFICANDO INSTALACIÓN")

result = conn.run(
    command='sudo docker run hello-world',
    pty=True, 
    watchers=[responder_sudo]
)

if 'Hello from Docker!' in result.stdout:
    print('Se ha instalado docker exitosamente')