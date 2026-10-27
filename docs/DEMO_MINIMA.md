# Demostración local mínima

El objetivo es mostrar el mapa y el recorrido de comunicados usando las funciones
existentes. No se aplican migraciones, altas de usuarios ni cambios de horarios.
La autorización para escribir en la base persistente se solicita antes de iniciar
sesiones reales o publicar: ambos generan registros en MariaDB.

## Preparar una vez

Desde la raíz de `LiceoMap-integracion`, usar el intérprete con las
dependencias ya instaladas. Este ejemplo consulta el entorno antiguo en modo de
solo lectura; no modifica ese proyecto:

```bash
export DEMO_PYTHON="$HOME/Proyectos/LiceoMap/api/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
"$DEMO_PYTHON" scripts/demo_local.py configure --from "$HOME/Proyectos/LiceoMap/api/.env"
"$DEMO_PYTHON" scripts/demo_local.py check-db
```

`configure` crea únicamente `.local/demo.env`, con permisos 600 y CORS limitado a
la web local. No imprime secretos ni sobrescribe una configuración existente.
`check-db` consulta conexión, tablas, migraciones y cantidades de cuentas por rol,
en una transacción de solo lectura. Si indica tablas faltantes, detener el recorrido
real y solicitar autorización para preparar exclusivamente las migraciones necesarias.
Nunca ejecutar el SQL inicial ni crear datos para ocultar un fallo.

## Iniciar

MariaDB es el servicio ya instalado. Si está detenido, iniciarlo manualmente:

```bash
sudo systemctl start mariadb
```

En una terminal, desde la raíz del proyecto:

```bash
PYTHONDONTWRITEBYTECODE=1 "$HOME/Proyectos/LiceoMap/api/.venv/bin/python" scripts/demo_local.py api
```

En otra terminal:

```bash
python3 scripts/demo_local.py web
```

Comprobar y conectar el teléfono por USB, aceptando la autorización de depuración:

```bash
python3 scripts/demo_local.py check
python3 scripts/demo_local.py usb
```

La APK debe estar compilada con `-PliceomapApiBaseUrl=http://127.0.0.1:8000/`.
La API y la web escuchan solo en el notebook. No se necesita una IP de la red,
hosting ni túneles públicos. El modo demostración y el mapa funcionan sin API.

Abrir `http://127.0.0.1:5500/` y pulsar **Acceso administrativo**. Usar una cuenta
existente con rol `dev`, `utp` o `inspectoria`. En Android usar una cuenta existente
con rol `alumno` y matrícula activa. Introducir credenciales únicamente en los
formularios; no guardarlas en esta guía ni compartir capturas de ellas.

## Recorrido de tres minutos

1. **0:00–0:40:** abrir Android e iniciar sesión como estudiante. Mostrar el nombre,
   curso y horario que devuelve la base. Si son datos sintéticos, decirlo.
2. **0:40–1:10:** abrir Mapa, ampliar, desplazar y volver a la vista completa. El
   mapa PNG de respaldo procede del SVG original; no localizar salas sin confirmar.
3. **1:10–2:10:** en la web, entrar como administrador y publicar un título breve,
   contenido, prioridad y el curso al que está matriculado el estudiante. Mantener
   el nombre del curso visible; no afirmar que es un curso personalizado aún no creado.
4. **2:10–2:40:** volver a Anuncios en Android y pulsar **Actualizar anuncios**.
   Mostrar el mismo título y contenido que se guardaron mediante la API.
5. **2:40–3:00:** retirar el comunicado desde la web, actualizar Android y comprobar
   que ya no aparece. No llamar a esta actualización una notificación push.

Antes de presentar, repetir también un comunicado global y otro de un curso distinto:
el global debe aparecer y el del otro curso no. Comprobar que una cuenta de alumno
no puede publicar. Estas comprobaciones deben realizarse solo después de autorizar
las escrituras de demostración, o en una base temporal con datos ficticios.

## Detener y plan B

Detener cada servidor con `Ctrl+C`. Quitar únicamente el enlace USB creado para la demo:

```bash
"$HOME/Android/Sdk/platform-tools/adb" reverse --remove tcp:8000
```

No detener MariaDB si lo usa otro trabajo. No ejecutar `down -v`, `DROP`, seeds ni
reinicializaciones. Si falla la red, reconectar USB y repetir `usb` y `check`. Si
falla MariaDB o faltan tablas/cuentas, mostrar el mapa y la navegación demo y explicar
que el recorrido de datos reales está pendiente. Si falla el visor, abrir el PNG
generado en el notebook como respaldo y decir que no es una prueba del visor Android.

## Estado de verificación

La compilación y la presencia de recursos en la APK se informan por separado del
resultado visual en el teléfono. El código existente contiene login, roles, CRUD y
lectura de comunicados por curso; su existencia no sustituye una prueba de integración.
El resultado concreto de conexión y `/health` debe tomarse de `check-db` y `check`.
No se realizaron escrituras de prueba en la base persistente sin autorización.

### Resultado del ensayo actual

- APK con visor PNG nativo: `BUILD SUCCESSFUL`; siete pruebas de zoom y límites aprobadas.
- Instalación en el Samsung: correcta. Mapa completo y ampliado inspeccionados mediante
  capturas reales; botón de vista completa comprobado. El SVG original permanece intacto.
- Enlace `adb reverse tcp:8000 tcp:8000`: configurado en el teléfono conectado.
- MariaDB `colegio_db`: conexión y consulta en transacción de solo lectura correctas.
- Faltan `auth_sessions` y `anuncios_historial`. Existen las migraciones aditivas
  `database/preoficial_migrations/005_sesiones.sql` y `004_anuncios_historial.sql`,
  pero **no se aplicaron**: requieren respaldo verificable, comprobación de permisos
  y autorización para modificar la base persistente.
- Login real, publicación y sincronización completa: pendientes de esa preparación;
  no presentarlos como un recorrido ya comprobado. `/health` HTTP aún no fue verificado.

Las capturas del ensayo están en `.local/demo-final/phone-map.png` y
`.local/demo-final/phone-map-zoom.png`, fuera del control de versiones.
