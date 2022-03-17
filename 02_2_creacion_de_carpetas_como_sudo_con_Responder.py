# Docs:
# https://docs.fabfile.org/en/2.6/getting-started.html#superuser-privileges-via-auto-response
# https://docs.pyinvoke.org/en/latest/concepts/watchers.html#autoresponding

from invoke import Responder
from fabric import Connection
from dotenv import load_dotenv
from os import getenv
from re import escape

load_dotenv()

NOMBRE_CARPETA_PRUEBA = 'prueba_mkdir_root'

conn = Connection(host=getenv('HOST'), user=getenv('USER'), connect_kwargs={'password': getenv('PASS')})

print("Probando creación y eliminación de directorios en carpeta de root usando sudo")

responder_sudo = Responder(
    pattern=r"\[sudo\] password",
    # Se necesita el \n al final para simular ENTER
    response=getenv('PASS')+"\n"
)

conn.run(f'sudo mkdir -p /{NOMBRE_CARPETA_PRUEBA}', pty=True, watchers=[responder_sudo])

if NOMBRE_CARPETA_PRUEBA in conn.run('ls /', hide=True).stdout:
    print("Carpeta creada exitosamente")


conn.run(f'sudo rm -r /{NOMBRE_CARPETA_PRUEBA}', pty=True, watchers=[responder_sudo])

if not NOMBRE_CARPETA_PRUEBA in conn.run('ls /', hide=True).stdout:
    print("Carpeta eliminada exitosamente")

conn.close()