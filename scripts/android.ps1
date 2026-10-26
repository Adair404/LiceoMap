param(
    [ValidateSet('Build','Unit','Sync','Design','Release','Inspect','RunLocal')][string]$Action = 'Build',
    [string]$Sdk = 'D:\JS',
    [string]$Java = 'C:\Program Files\Android\Android Studio\jbr'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (!(Test-Path (Join-Path $Sdk 'platform-tools/adb.exe'))) { throw 'Indicar -Sdk con el Android SDK existente.' }
if (!(Test-Path (Join-Path $Java 'bin/java.exe'))) { throw 'Indicar -Java con JDK 25.' }
$env:JAVA_HOME = $Java
$env:ANDROID_HOME = $Sdk
# Java on Windows reads argument files using the native system charset. A mapped
# drive avoids the accented username in Gradle-generated classpath argument files.
$userPath = [Environment]::GetFolderPath('UserProfile')
if ($userPath -match '[^\x00-\x7F]') {
    if (!(Test-Path 'L:\')) { subst.exe L: $userPath }
    if (!(Test-Path 'L:\Desktop\LiceoMap-2.0\scripts\android.ps1')) { throw 'L: ocupado por otra ruta. Elegir una letra libre en este script.' }
    $projectRoot = 'L:\Desktop\LiceoMap-2.0'
    $env:GRADLE_USER_HOME = 'L:\.gradle'
} else { $env:GRADLE_USER_HOME = Join-Path $userPath '.gradle' }
Push-Location (Join-Path $projectRoot 'android')
try {
    $commonArgs = @('--no-configuration-cache','--max-workers=2')
    switch ($Action) {
        'Build' { & .\gradlew.bat @commonArgs assembleDebug }
        'RunLocal' {
            & .\gradlew.bat @commonArgs assembleDebug '-PliceomapApiBaseUrl=http://127.0.0.1:8000/'
            if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar la APK de desarrollo local.' }
            & (Join-Path $Sdk 'platform-tools/adb.exe') reverse tcp:8000 tcp:8000
            if ($LASTEXITCODE -ne 0) { throw 'No se pudo establecer adb reverse.' }
            & (Join-Path $Sdk 'platform-tools/adb.exe') install -r (Join-Path $projectRoot 'android/app/build/outputs/apk/debug/app-debug.apk')
            if ($LASTEXITCODE -ne 0) { throw 'No se pudo instalar la APK.' }
            & (Join-Path $Sdk 'platform-tools/adb.exe') shell am start -n com.liceomap.app/.MainActivity
        }
        'Unit' { & .\gradlew.bat @commonArgs testDebugUnitTest }
        'Release' { & .\gradlew.bat @commonArgs assembleRelease }
        'Inspect' {
            & (Join-Path $Sdk 'platform-tools/adb.exe') shell run-as com.liceomap.app ls files
            & (Join-Path $Sdk 'platform-tools/adb.exe') shell uiautomator dump /sdcard/liceomap-test-ui.xml
            & (Join-Path $Sdk 'platform-tools/adb.exe') pull /sdcard/liceomap-test-ui.xml (Join-Path $projectRoot '.local/android-ui.xml')
        }
        'Design' { & .\gradlew.bat @commonArgs connectedDebugAndroidTest '-Pandroid.testInstrumentationRunnerArguments.notClass=com.liceomap.app.PreoficialSyncTest' }
        'Sync' {
            $webListener = Get-NetTCPConnection -LocalPort 5500 -State Listen -ErrorAction SilentlyContinue
            if ($webListener) {
                $webProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($webListener.OwningProcess)"
                if ($webProcess.CommandLine -notmatch 'scripts[\\/]run_web\.py.*--test') { throw 'Cerrar la web de desarrollo antes de Sync; no se detiene otro servidor.' }
                $ownedWebProcess = [System.Diagnostics.Process]::GetProcessById([int]$webProcess.ProcessId)
                $ownedWebProcess.Kill(); $ownedWebProcess.WaitForExit(10000) | Out-Null
            }
            $testListener = Get-NetTCPConnection -LocalPort 8001 -State Listen -ErrorAction SilentlyContinue
            if ($testListener) {
                $testProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($testListener.OwningProcess)"
                if ($testProcess.CommandLine -notmatch 'scripts[\\/]run_api\.py.*--test') { throw 'Puerto 8001 ocupado por otro proceso; no se detiene.' }
                $ownedTestProcess = [System.Diagnostics.Process]::GetProcessById([int]$testProcess.ProcessId)
                $ownedTestProcess.Kill()
                $ownedTestProcess.WaitForExit(10000) | Out-Null
            }
            & .\gradlew.bat @commonArgs assembleDebug assembleDebugAndroidTest '-PliceomapApiBaseUrl=http://127.0.0.1:8001/'
            if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar la APK para la API test' }
            & (Join-Path $projectRoot '.venv/Scripts/python.exe') (Join-Path $PSScriptRoot 'verify_sync.py')
        }
    }
    if ($LASTEXITCODE -ne 0) { throw "Falló la verificación Android: $Action" }
} finally { Pop-Location }
