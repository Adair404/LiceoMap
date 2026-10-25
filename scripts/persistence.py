"""Snapshot/compare announcement records across a dedicated MariaDB restart."""
import hashlib
import json
import sys
from local_db import connect, LOCAL


def snapshot():
    result = {}
    for db in ('liceomap_preoficial_dev','liceomap_preoficial_test'):
        with connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM anuncios ORDER BY id_anuncio')
                announcements = cur.fetchall()
                cur.execute('SELECT * FROM anuncios_historial ORDER BY id_historial')
                history = cur.fetchall()
                data = json.dumps([announcements,history],default=str,ensure_ascii=False).encode()
                result[db] = {'announcements':len(announcements),'history':len(history),
                              'sha256':hashlib.sha256(data).hexdigest()}
    return result


if __name__ == '__main__':
    data = snapshot()
    path = LOCAL/'persistence.json'
    if sys.argv[1:] == ['before']:
        path.write_text(json.dumps(data,indent=2))
        print('Snapshot de persistencia guardado; sin modificar registros.')
    elif sys.argv[1:] == ['after']:
        assert data == json.loads(path.read_text()), 'Datos distintos después del reinicio'
        print('PASS: anuncios e historial idénticos tras reiniciar MariaDB (dev y test).')
    else:
        raise SystemExit('Uso: persistence.py before|after')
