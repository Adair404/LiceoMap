"""Coordinate the real Chrome -> API -> MariaDB -> Android test. No credentials printed."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.request
import urllib.error
import atexit
from local_db import ROOT, LOCAL, connect

ADB = Path(os.environ.get('ANDROID_HOME', 'D:/JS')) / 'platform-tools/adb.exe'
PACKAGE = 'com.liceomap.app'
STAGES = set()


class Control(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        self.send_response(200 if self.path.removeprefix('/control/') in STAGES else 404)
        self.send_header('Content-Length','0'); self.end_headers()

    def do_POST(self):
        stage = self.path.removeprefix('/control/')
        if len(stage) > 40 or not stage.replace('-','').isalpha():
            self.send_response(400); self.end_headers(); return
        STAGES.add(stage)
        self.send_response(200); self.send_header('Content-Length','0'); self.end_headers()


def adb(*args, check=True):
    result = subprocess.run([str(ADB),*args], capture_output=True, text=True, encoding='utf-8', errors='replace',timeout=30)
    if check and result.returncode:
        raise RuntimeError('adb failed: ' + result.stderr[-300:])
    return result.stdout


def await_signal(name, process):
    deadline = time.monotonic()+150
    while time.monotonic() < deadline:
        if name in STAGES:
            print('Android:',name,flush=True); return
        if process.poll() is not None:
            raise RuntimeError('Instrumentation ended before '+name+'; see .local/android-sync.log')
        time.sleep(.5)
    raise RuntimeError('Timeout waiting for Android: '+name)


def signal(name):
    STAGES.add(name)


def web_action(action):
    state = json.loads((LOCAL/'sync-state.json').read_text(encoding='utf-8'))
    state['action'] = action
    (LOCAL/'sync-state.json').write_text(json.dumps(state), encoding='utf-8')
    for attempt in range(3):
        result = subprocess.run(['node','web/tests/phase2.cjs','--preoficial','--sync-action'],cwd=ROOT,
                                capture_output=True,text=True,encoding='utf-8',errors='replace')
        with (LOCAL/'web-sync.log').open('a',encoding='utf-8') as log:
            log.write(result.stdout+result.stderr)
        if result.returncode == 0:
            break
        print('Browser startup/action failed; retry',attempt+1,flush=True)
    if result.returncode:
        raise RuntimeError('Browser synchronization failed. See .local/web-sync.log')
    print('Web:',action,'verified',flush=True)


def stop_owned_process(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait(timeout=5)


def start_test_service(script, port, probe):
    log = (LOCAL/(script+'-sync.log')).open('a',encoding='utf-8')
    # Use the actual interpreter: Windows venv redirectors can leave the API child
    # alive when only their launcher is terminated, invalidating an offline test.
    api_env = dict(os.environ)
    api_env['PYTHONPATH'] = str(ROOT/'.venv/Lib/site-packages')
    process = subprocess.Popen([sys._base_executable,'-u',str(ROOT/'scripts'/script),'--test'],
                               cwd=ROOT,stdout=log,stderr=log,env=api_env)
    atexit.register(stop_owned_process,process)
    log.close()
    deadline = time.monotonic()+15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(script+' did not start; inspect .local/'+script+'-sync.log')
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/{probe}',timeout=1) as response:
                if response.status == 200:
                    return process
        except (OSError,urllib.error.URLError):
            time.sleep(.2)
    process.terminate()
    raise RuntimeError('Test service health timeout: '+script)


def start_test_api():
    return start_test_service('run_api.py',8001,'health')


def main():
    if not (ROOT/'android/app/build/generated/source/buildConfig/debug/com/liceomap/app/BuildConfig.java').exists():
        raise RuntimeError('Compile the Android debug APK for the test API first')
    build = (ROOT/'android/app/build/generated/source/buildConfig/debug/com/liceomap/app/BuildConfig.java').read_text()
    if 'http://127.0.0.1:8001/' not in build:
        raise RuntimeError('Refusing to run against a development or production Android API')
    accounts = json.loads((LOCAL/'liceomap_preoficial_test.accounts.json').read_text())
    student = next(a for a in accounts if a['rut']=='20100006-8')
    title = 'Sincronizacion '+str(int(time.time()))
    control = ThreadingHTTPServer(('127.0.0.1',5502),Control)
    threading.Thread(target=control.serve_forever,daemon=True).start()
    (LOCAL/'sync-state.json').write_text(json.dumps({'title':title,'action':'create'}))
    adb('reverse','tcp:8001','tcp:8001')
    adb('reverse','tcp:5502','tcp:5502')
    api_process = start_test_api()
    web_process = start_test_service('run_web.py',5500,'')
    adb('install','-r',str(ROOT/'android/app/build/outputs/apk/debug/app-debug.apk'))
    adb('install','-r',str(ROOT/'android/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk'))
    # No Gradle property, source file, log output, or APK contains these credentials.
    command = [str(ADB),'shell','am','instrument','-w','-e','class',PACKAGE+'.PreoficialSyncTest',
               '-e','preoficial','true','-e','rut',student['rut'],'-e','password',student['password'],
               '-e','title',f'"{title}"',PACKAGE+'.test/androidx.test.runner.AndroidJUnitRunner']
    with (LOCAL/'android-sync.log').open('w',encoding='utf-8') as log:
        process = subprocess.Popen(command,stdout=log,stderr=log)
        try:
            await_signal('waiting-publication',process)
            web_action('create'); signal('published')
            await_signal('seen-publication',process)
            web_action('edit'); signal('edited')
            await_signal('seen-edit',process)
            api_process.terminate(); api_process.wait(timeout=10); signal('offline')
            await_signal('seen-offline',process)
            api_process = start_test_api(); signal('online')
            await_signal('seen-recovery',process)
            web_action('withdraw'); signal('withdrawn')
            await_signal('seen-withdrawal',process)
            with connect('liceomap_preoficial_test') as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE auth_sessions SET expira_en=DATE_SUB(UTC_TIMESTAMP(), INTERVAL 1 SECOND) "
                                "WHERE id_usuario=(SELECT id_usuario FROM usuarios WHERE rut=%s)",(student['rut'],))
            signal('expired'); await_signal('seen-expiry',process); await_signal('complete',process)
            process.wait(timeout=30)
        finally:
            control.shutdown(); control.server_close()
            if api_process.poll() is None:
                api_process.terminate(); api_process.wait(timeout=10)
            stop_owned_process(web_process)
            adb('reverse','--remove','tcp:8001',check=False)
            adb('reverse','--remove','tcp:5502',check=False)
            if process.poll() is None:
                process.terminate()
                adb('shell','am','force-stop',PACKAGE,check=False)
    output = (LOCAL/'android-sync.log').read_text(encoding='utf-8')
    if 'OK (1 test)' not in output or 'FAILURES' in output:
        raise RuntimeError('Android instrumentation failed; inspect .local/android-sync.log')
    print('PASS: WEB -> API -> MariaDB -> Android; refresh, edit, withdrawal, connection recovery, expiration, logout.',flush=True)


if __name__ == '__main__':
    main()
