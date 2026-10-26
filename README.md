# LiceoMap 🗺️

Plataforma móvil y web de navegación interactiva y gestión de horarios para la comunidad educativa del **Liceo Bicentenario de Excelencia Antonio Varas de la Barra**.

---

Integración preoficial WEB + FastAPI + MariaDB + Android: instalación, arranque,
pruebas y estado verificado en [docs/PREOFICIAL_INTEGRACION.md](docs/PREOFICIAL_INTEGRACION.md).

## 📁 Estructura del Repositorio

* `android/`: Aplicación Kotlin, Jetpack Compose, Material 3 y MVVM.
* `api/`: FastAPI con autenticación, permisos, horarios y anuncios.
* `database/`: Esquema MariaDB y migraciones; bases locales dedicadas de desarrollo y pruebas.
* `design/`: Recursos gráficos, mapa de referencia e insumos vectoriales SVG (Inkscape).
* `docs/`: Documentación oficial, definición de roles (`01-equipo.md`) y documentos del proyecto.
* `web/`: Portal web institucional y visor interactivo (HTML/CSS).

---

## 🚀 Flujo de Trabajo

Para mantener la organización del repositorio, todo el equipo debe seguir estas reglas:

1. **Nunca trabajar directamente sobre la rama `main`.**
2. Crear una rama por cada funcionalidad o tarea nueva desde su *fork*:
   `git checkout -b feature/nombre-de-la-tarea`
3. Probar los cambios localmente antes de hacer commit.
4. Crear un **Pull Request (PR)** hacia la rama principal del proyecto para revisión.

---

## 🛠️ Tecnologías

* **Base de Datos:** MariaDB / MySQL (`colegio_db`).
* **Móvil:** Android Nativo (Java).
* **Cartografía:** SVG vectorial diseñado en Inkscape.
* **Web:** HTML5 / CSS3.

---

## 👥 Equipo de Desarrollo
Consulte el archivo [`docs/01-equipo.md`](docs/01-equipo.md) para conocer la nómina oficial, roles y responsabilidades del equipo.
