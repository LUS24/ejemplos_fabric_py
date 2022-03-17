# Docs:
# https://www.fabfile.org/
# https://docs.fabfile.org/


from fabric import Connection
from dotenv import load_dotenv

from os import getenv

load_dotenv()

connection_string = '@'.join([getenv('USER'), getenv('HOST')])

conn = Connection(host=connection_string, connect_kwargs={'password': getenv('PASS')})
# Otra opción
# conn = Connection(host=getenv('HOST'), user=getenv('USER'), connect_kwargs={'password': getenv('PASS')})

result = conn.run('uname -s')

print(result.ok)
print(result.command)
print(result.connection)
print(result.connection.host)

conn.close()
