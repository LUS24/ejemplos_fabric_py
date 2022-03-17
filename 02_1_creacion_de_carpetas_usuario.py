from fabric import Connection
from dotenv import load_dotenv

from os import getenv

load_dotenv()

connection_string = '@'.join([getenv('USER'), getenv('HOST')])

conn = Connection(host=connection_string, connect_kwargs={'password': getenv('PASS')})
# Si lleva un puerto se puede hacer Connection(host='web1', user='deploy', port=2202)
# O Connection('deploy@web1:2202')

print("Probando creación y eliminación de directorios en carpeta de usuario")

# Crea el directorio si no existe
if conn.run('mkdir -p prueba_mkdir_fabric').ok:
    print("Todo ok")

# Lista todos los directorios y busca si está presente el creado previamente
if 'prueba_mkdir_fabric' in conn.run('ls').stdout:
    print('Directorio creado exitosamente')

# Borra el directorio y todo su contenido
conn.run('rm -r prueba_mkdir_fabric')

if not 'prueba_mkdir_fabric' in conn.run('ls').stdout:
    print('Directorio borrado exitosamente')

conn.close()
