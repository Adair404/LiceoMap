from local_db import connect

connection = connect()
try:
    with connection.cursor() as cursor:
        cursor.execute('SHUTDOWN')
    print('Instancia dedicada detenida limpiamente.')
finally:
    connection.close()
