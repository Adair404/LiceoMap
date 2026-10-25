"""Development runner. Access logs are disabled to avoid logging personal URLs."""
from pathlib import Path
import sys
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'api'))
if __name__ == '__main__':
    testing = '--test' in sys.argv
    if testing:
        import os
        from local_db import settings
        cfg = settings()
        os.environ.update(DB_HOST='127.0.0.1', DB_PORT='3308', DB_NAME='liceomap_preoficial_test',
                          DB_USER='liceomap_test', DB_PASSWORD=cfg['APP_PASSWORD'], JWT_SECRET=cfg['JWT_SECRET'])
    uvicorn.run('app.main:app', host='127.0.0.1', port=8001 if testing else 8000, access_log=False)
