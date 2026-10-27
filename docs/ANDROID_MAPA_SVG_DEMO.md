# Mapa Android para la presentación

La versión actual usa una **imagen nativa de Compose**, generada sin alterar el SVG.
El PNG de 2760 × 4050 está en `design/android/`; se empaqueta automáticamente en la APK.
El mapa funciona sin Internet, en demo y con sesión iniciada, con pellizco, arrastre,
botones de zoom y vista completa. El desplazamiento queda limitado para no perder
el mapa fuera de pantalla. Las salas individuales siguen sin ubicación vinculada.

Para regenerar el PNG cuando cambie el SVG:

```bash
python3 scripts/render_android_map.py
```

Requiere Inkscape, ya disponible en este equipo. La compilación comprueba la huella
SHA-256 del SVG para impedir que se empaquete un PNG desactualizado.

Los diagnósticos nativos se consultan con:

```bash
"$HOME/Android/Sdk/platform-tools/adb" logcat -s LiceoMapViewer
```

El PNG fue inspeccionado visualmente y se comprobaron sus bytes dentro de la APK.
La APK se instaló en el Samsung: se inspeccionaron capturas del mapa completo y
del mapa ampliado en modo demostración, y se comprobó el botón de vista completa.
La sesión autenticada sigue pendiente de preparar las tablas de sesiones de MariaDB.
Consulta `docs/DEMO_MINIMA.md` para el arranque, instalación y recorrido de presentación.

---

## Referencia conservada del intento anterior con WebView

Los detalles siguientes describen el visor HTTPS anterior. Su código auxiliar se
conserva, pero la pantalla actual ya no depende de WebView para dibujar el mapa.

# Demostración del mapa SVG en Android

La pestaña **Mapa** usa `design/svg/mapa_liceo_concepto.svg` tanto en demostración
como con una sesión autenticada. Se conservan el acceso, los horarios, los anuncios,
el perfil, los temas y la navegación de la aplicación existente.

## Qué incluye

- El SVG original, con su geometría, textos, proporciones y cuadrícula intactos.
- Vista inicial del mapa completo, pellizco para ampliar y arrastre para desplazarse.
- Botones para ampliar, reducir y volver a ver el mapa completo.
- Funcionamiento del visor sin conexión: el mapa y su página están dentro de la APK.
- Mensaje y opción de reintentar si el recurso no puede abrirse.
- Acceso desde «Ver sala en mapa», manteniendo la selección como contexto. No se
  dibujan marcadores de salas ni se asignan posiciones sin una correspondencia validada.

Al abrir de nuevo el visor, girar el teléfono o pulsar «Ver mapa completo», se vuelve
a la vista inicial. La localización individual de salas y las rutas quedan pendientes.

## Implementación

`MapScreen` incorpora una `WebView` mediante `AndroidView`, siguiendo la
[interoperabilidad de Compose documentada por Android](https://developer.android.com/develop/ui/compose/migrate/interoperability-apis/wrap-webview-in-compose).
Se usa el renderizador SVG del sistema para conservar los estilos, patrones,
transformaciones y etiquetas del original. AndroidX `WebViewAssetLoader` sirve el
HTML y SVG desde `https://appassets.androidplatform.net/assets/`, sin solicitudes
a un servidor externo. La CSP permite imágenes del mismo origen y los estilos
incluidos en el HTML. JavaScript, almacenamiento web y acceso a archivos privados
permanecen desactivados. El interceptor solo acepta los dos recursos del mapa y
devuelve un error local para cualquier otra URL, sin recurrir a la red.

El visor activa la carga de imágenes y permite que las solicitudes HTTPS lleguen
al interceptor local, fija `image/svg+xml` para el SVG y evita contenido mixto y
caché obsoleta. Los errores de recursos y HTTP muestran la opción de reintentar;
los mensajes de consola y CSP de la APK debug se registran con la etiqueta
`LiceoMapViewer`. Referencia: [carga local recomendada por Android](https://developer.android.com/develop/ui/views/layout/webapps/load-local-content).

La tarea Gradle `syncSchoolMap` copia el archivo de `design/svg/` sin modificar sus
bytes y lo registra como asset generado mediante la API de variantes de Android.
No hay que mantener una segunda copia del mapa en `src/main/assets` ni ejecutar su
generador Python. Los cambios posteriores en el SVG se incorporan al volver a compilar.

## Compilar

Requisitos del proyecto: JDK 25, SDK Android 37.0 y el Gradle Wrapper incluido.
Gradle selecciona las Build Tools necesarias (36.0.0 en la compilación local).
Se utiliza el SDK existente de Android Studio; no hace falta instalar otro SDK.

Desde `android/`, en Linux:

```bash
ANDROID_HOME="$HOME/Android/Sdk" bash ./gradlew --no-daemon --no-parallel --no-configuration-cache --max-workers=1 '-Dorg.gradle.jvmargs=-Xmx768m -XX:MaxMetaspaceSize=384m -XX:ReservedCodeCacheSize=96m -XX:+UseSerialGC -Dfile.encoding=UTF-8' -Pkotlin.compiler.execution.strategy=in-process -Pandroid.builder.sdkDownload=false :app:assembleDebug :app:compileDebugAndroidTestKotlin
```

En Windows, usar `gradlew.bat` con los mismos argumentos. Android Studio también
puede abrir la carpeta `android/` y compilar la variante `debug`.

APK: `android/app/build/outputs/apk/debug/app-debug.apk`.
Se conserva la URL de API configurada por el proyecto. El límite de heap de Gradle
es 768 MB, con 384 MB de metaspace y un trabajador, sin un proceso Kotlin adicional.
La descarga automática de componentes del SDK está desactivada.
`compileDebugAndroidTestKotlin` comprueba la compilación de las pruebas
instrumentadas; no las ejecuta ni arranca o modifica MariaDB.

## Instalar en el teléfono

Copiar `app-debug.apk` al teléfono, abrirlo con el gestor de archivos y autorizar
la instalación desde esa aplicación cuando Android lo solicite.

Alternativamente, habilitar depuración USB, conectar el teléfono y aceptar la
autorización del PC. Desde la raíz del repositorio, con `adb` en el PATH:

```bash
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
```

Abrir LiceoMap → **Explorar demostración** → **Mapa**. Este recorrido no necesita
API, base de datos, RUT ni contraseña.

Para iniciar sesión real se conserva la configuración de conexión de la aplicación
existente. Introducir las credenciales únicamente en la aplicación. La integración
del mapa no cambia la API, las cuentas ni la configuración de la base de datos.

Si vuelve a fallar la carga, con el teléfono conectado por USB se pueden consultar
los diagnósticos del visor mientras se abre la pestaña Mapa:

```bash
adb logcat -s LiceoMapViewer
```

## Comprobar en un dispositivo

1. Entrar en demostración, abrir **Mapa** y comprobar que aparecen el patio central,
   los bloques y las calles con la misma disposición que el SVG de `design/svg/`.
2. Ampliar con dos dedos y con el botón `+`; arrastrar en ambas direcciones y reducir
   con `−`. Pulsar **Ver mapa completo** y comprobar que se recupera la vista inicial.
3. Abrir una sala desde **Horarios** y volver atrás. Se muestra el mapa general y
   se aclara que la ubicación de esa sala está pendiente de vinculación.
4. Repetir el acceso a **Mapa** después de iniciar sesión con la API existente.
   Verificar también que se puede volver a Inicio, Anuncios y Perfil.
5. En demostración, repetir con el teléfono sin conexión y girar la pantalla.

`SchoolMapFlowTest` cubre los accesos demo y autenticado con repositorios en memoria,
carga del asset, zoom, desplazamiento y restablecimiento. `SchoolMapAssetsTest`
comprueba las respuestas HTTPS locales, los tipos MIME, la identidad de los bytes
empaquetados y el rechazo de URLs ajenas. Se pueden ejecutar junto con el recorrido
original de navegación, en un emulador o dispositivo de pruebas:

```bash
bash ./gradlew --max-workers=1 :app:connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.liceomap.app.SchoolMapAssetsTest,com.liceomap.app.SchoolMapFlowTest,com.liceomap.app.AppFlowTest
```

Estas clases no usan MariaDB ni cuentas reales. No es necesario ejecutar la prueba
`PreoficialSyncTest` para comprobar esta integración del mapa.

## Validación local de la corrección

La compilación de la APK y del código de las pruebas instrumentadas terminó con
`BUILD SUCCESSFUL`, usando el SDK existente en `~/Android/Sdk`, Java 25, Gradle 9.5,
un trabajador y los límites de memoria indicados arriba.
Se verificó la firma de la APK y que incluye el cargador HTTPS, el HTML con la CSP
actualizada y una copia idéntica del SVG original. El SVG y su generador no cambiaron.
Las pruebas instrumentadas no se ejecutaron en un dispositivo desde este entorno;
la comprobación visual final se realiza al instalar la APK corregida en el teléfono.
