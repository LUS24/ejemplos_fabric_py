# Para subir y bajar archivos usar get y put
# Para carpetas se requiere otra librería adicional
# https://fabric-patchwork.readthedocs.io/en/latest/api/transfers.html#patchwork.transfers.rsync
# https://stackoverflow.com/a/54667814/6177246


from fabric import Connection
from dotenv import load_dotenv
from os import getenv, listdir, remove
from os.path import join as local_join
from posixpath import join as linux_join


load_dotenv()


DIRECTORIO_IMAGENES_A_SUBIR = 'archivos_de_prueba_a_enviar'
DIRECTORIO_DESCARGAS = 'archivos_de_prueba_recibidos'

conn = Connection(
    host=getenv('HOST'),
    user=getenv('USER'),
    connect_kwargs= {'password': getenv('PASS')},
    )

SERVER_WD = conn.run('pwd' ).stdout.replace('\n', '')
DIRECTORIO_IMAGENES_SERVER = linux_join(SERVER_WD, 'imagenes_subidas')

# Subir imágenes una a una

conn.run(f'mkdir -p {DIRECTORIO_IMAGENES_SERVER}')

if DIRECTORIO_IMAGENES_SERVER in conn.run('ls').stdout:
    print('Directorio creado exitosamente')

[
    conn.put(
        local=local_join(DIRECTORIO_IMAGENES_A_SUBIR, nombre_archivo),
        remote=linux_join(DIRECTORIO_IMAGENES_SERVER, nombre_archivo)
    )
    for nombre_archivo in listdir(DIRECTORIO_IMAGENES_A_SUBIR)
]

nombres_imagenes_en_server = conn.run(f'ls {DIRECTORIO_IMAGENES_SERVER}', hide=True).stdout.split('\n')
nombres_imagenes_en_server.remove('')

if set(nombres_imagenes_en_server) == set(listdir(DIRECTORIO_IMAGENES_A_SUBIR)):
    print("Todos los archivos se cargaron correcamente")

# Descargar archivos desde servidor

[
    conn.get(
        local=local_join(DIRECTORIO_DESCARGAS, nombre_archivo),
        remote=linux_join(DIRECTORIO_IMAGENES_SERVER, nombre_archivo),
    )
    for nombre_archivo in nombres_imagenes_en_server
]


if set(nombres_imagenes_en_server) == set(listdir(DIRECTORIO_DESCARGAS)):
    print("Todos los archivos se descargaron correcamente")

# Limpieza

conn.run(f'rm -r {DIRECTORIO_IMAGENES_SERVER}')

[remove(local_join(DIRECTORIO_DESCARGAS, nombre_archivo)) for nombre_archivo in listdir(DIRECTORIO_DESCARGAS)]

if not listdir(DIRECTORIO_DESCARGAS) and DIRECTORIO_IMAGENES_SERVER not in conn.run('ls').stdout:
    print('Entornos limpios en servidor y local')

conn.close()
