param([ValidateSet('Install','Start','Stop','VerifyPersistence')][string]$Action = 'Start')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$localRoot = Join-Path $projectRoot '.local'
$dataPath = Join-Path $localRoot 'mariadb-data'
$toolsPath = Join-Path $localRoot 'tools'
$pythonPath = Join-Path $projectRoot '.venv/Scripts/python.exe'
if ($Action -eq 'VerifyPersistence') {
    & $pythonPath (Join-Path $PSScriptRoot 'persistence.py') before
    if ($LASTEXITCODE -ne 0) { throw 'No se obtuvo snapshot; no se detiene la BD.' }
    & $pythonPath (Join-Path $PSScriptRoot 'stop_db.py')
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo detener la instancia dedicada.' }
    Start-Sleep -Seconds 2
    & $PSCommandPath -Action Start
    Start-Sleep -Seconds 3
    & $pythonPath (Join-Path $PSScriptRoot 'persistence.py') after
    if ($LASTEXITCODE -ne 0) { throw 'Falló comparación de persistencia.' }
    exit 0
}
if ($Action -eq 'Install') {
    if (Test-Path $dataPath) { throw 'Existe el directorio de datos: no se reinicializa.' }
    if (Get-NetTCPConnection -LocalPort 3308 -State Listen -ErrorAction SilentlyContinue) { throw 'Puerto 3308 ocupado.' }
    $archive = Join-Path $toolsPath 'mariadb.zip'
    if (!(Test-Path $archive)) {
        New-Item -ItemType Directory -Force $toolsPath | Out-Null
        Invoke-WebRequest 'https://archive.mariadb.org/mariadb-11.4.13/winx64-packages/mariadb-11.4.13-winx64.zip' -OutFile $archive -UseBasicParsing
    }
    $expectedHash = 'D62986D433EEEBFDE218560B276103831604A61E929E87F1A17F5AEBD80257E2'
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash -ne $expectedHash) { throw 'MariaDB ZIP no coincide con el SHA256 oficial.' }
    Expand-Archive -LiteralPath $archive -DestinationPath $toolsPath -Force
    & $pythonPath (Join-Path $PSScriptRoot 'local_db.py') secrets
    if ($LASTEXITCODE -ne 0) { throw 'Falló generación de configuración' }
    $databaseEnv = Get-Content (Join-Path $localRoot 'database.env') -Raw | ConvertFrom-StringData
    $installer = Join-Path $toolsPath 'mariadb-11.4.13-winx64/bin/mariadb-install-db.exe'
    # Password is generated locally and is never written to the console.
    & $installer "--datadir=$dataPath" "--password=$($databaseEnv.MARIADB_ROOT_PASSWORD)" '--port=3308' '--skip-networking=0' *> (Join-Path $localRoot 'mariadb-install.log')
    if ($LASTEXITCODE -ne 0) { throw 'Falló instalación, revisar .local/mariadb-install.log sin publicar su contenido.' }
}
$serverPath = Join-Path $toolsPath 'mariadb-11.4.13-winx64/bin/mariadbd.exe'
$pidPath = Join-Path $localRoot 'mariadb.pid'
if ($Action -eq 'Stop') {
    # Authenticated shutdown; never kill a process merely because it owns a port.
    & $pythonPath (Join-Path $PSScriptRoot 'stop_db.py')
    exit $LASTEXITCODE
}
if (!(Test-Path (Join-Path $dataPath 'mysql'))) { throw 'Instancia no inicializada. Ejecutar -Action Install.' }
if (Get-NetTCPConnection -LocalPort 3308 -State Listen -ErrorAction SilentlyContinue) { throw 'Puerto 3308 ocupado: verificar antes de arrancar.' }
$serverArgs = @("--defaults-file=`"$(Join-Path $dataPath 'my.ini')`"", '--bind-address=127.0.0.1', '--port=3308', '--default-time-zone=+00:00', "--pid-file=`"$pidPath`"", "--log-error=`"$(Join-Path $localRoot 'mariadb-error.log')`"")
Start-Process -FilePath $serverPath -ArgumentList $serverArgs -WindowStyle Hidden -WorkingDirectory $dataPath
Write-Output 'Arranque solicitado en 127.0.0.1:3308. Datos persistentes en .local/mariadb-data.'
