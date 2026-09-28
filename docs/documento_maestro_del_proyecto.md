# Documento Maestro del Proyecto: los_robloxianos

*Plataforma Web y Aplicación Móvil de Orientación Escolar para el Liceo Antonio Varas de la Barra*

## PARTE 1: INFORMACIÓN GENERAL Y ESPECIFICACIÓN TÉCNICA

### 1. Objetivos y Alcance

#### Objetivo General
Desarrollar una aplicación móvil nativa para Android (mediante Android Studio) complementada con un portal web, que permita a los estudiantes del Liceo Bicentenario de Excelencia Antonio Varas de la Barra orientarse espacialmente mediante un mapa vectorial interactivo (.svg), consultar horarios por curso y acceder a comunicados oficiales publicados por la UTP.

#### Objetivos Específicos
1. Diseñar e implementar una interfaz móvil intuitiva en Android Studio (Java) para la navegación e interacción cotidiana.
2. Construir un plano vectorial interactivo del liceo en Inkscape (formato SVG) asignando identificadores lógicos (`id`) a pabellones, salas, patios y dependencias.
3. Implementar un módulo de orientación espacial dinámico con interfaz táctil e intuitiva, combinando posicionamiento GPS en zonas al aire libre con un sistema de rutas por nodos (algoritmo Dijkstra / $A^*$) para navegación asistida en interiores.
4. Implementar un sistema de autenticación por RUT y contraseña con perfiles diferenciados por rol (Estudiante, Docente, UTP/Inspectoría y Desarrollador).
5. Desarrollar un módulo de consulta de horarios de clases y un panel para que los docentes puedan mantener actualizada su asignación de salas.
6. Crear un módulo de anuncios y avisos globales administrado por la UTP para centralizar la comunicación oficial.
7. Diseñar una landing page web para la promoción del proyecto, difusión/administración institucional y descarga de la aplicación.

#### Beneficiarios
* **Estudiantes**: Consulta de ubicación de salas en tiempo real, orientación asistida en el recinto, horarios de clases y noticias del liceo.
* **Docentes**: Consulta de horarios, asignación de salas y canal de avisos.
* **Personal de UTP e Inspectoría**: Administración de usuarios, avisos institucionales y gestión de horarios.
* **Desarrollador / Administrador Técnico**: Perfil con privilegios extendidos para pruebas de sistema, simulación de datos y depuración local.

---

### 2. Especificación Técnica del Mapa SVG y Navegación Dinámica

#### Sistema de Navegación e Interacción con el Mapa
* **Visualización Dinámica:** Renderizado del gráfico vectorial SVG permitiendo encuadre libre (Touch Pan), zoom responsivo y resaltado dinámico de dependencias seleccionadas.
* **Modo de Navegación Mixto (Exterior / Interior):**
  * **Exteriores / Patios (GPS Activo):** En áreas abiertas (canchas, patios, pasillos expuestos), la app utiliza el sensor GPS del dispositivo para ubicar al usuario dentro del marco de coordenadas geográficas del plano.
  * **Interiores / Techos (Navegación por Grafo de Nodos):** En pasillos y zonas cerradas donde la señal satelital decae, el usuario selecciona un punto de partida ("¿Dónde estás?") y un destino. La aplicación calcula la ruta más corta uniendo waypoints (nodos) prefijados en el SVG y superpone una línea vectorial indicadora (`polyline`) junto a instrucciones por hitos visuales.

#### Estándar de Identificadores (IDs) en Inkscape
Para asegurar la comunicación directa entre el código Android en Java y el archivo `.svg`, se establece el siguiente estándar de nombrado en las propiedades de objeto de Inkscape:

| Tipo de Elemento | Convención de `id` | Ejemplo de Uso |
| :--- | :--- | :--- |
| **Salas de Clases** | `sala_[número/nombre]` | `id="sala_10"`, `id="sala_computacion"` |
| **Pabellones** | `pabellon_[letra]` | `id="pabellon_a"`, `id="pabellon_b"` |
| **Zonas Comunes / Patios** | `zona_[nombre]` | `id="zona_patio_central"`, `id="cancha_principal"` |
| **Puntos de Red / Nodos de Ruta** | `node_[número/nombre]` | `id="node_entrada_principal"`, `id="node_pasillo_pabellon_a"` |
| **Administración / UTP** | `admin_[área]` | `id="admin_utp"`, `id="biblioteca"` |

---

#### Estándar de Identificadores (IDs) en Inkscape
* **Documentación Oficial de IDs:** La convención técnica de capas, bloques (`bloque_b`, `bloque_k`, etc.), salas y nodos de navegación está definida de forma centralizada en [`design/standard_ids.md`](../design/standard_ids.md).

---

### 3. Arquitectura de Base de Datos (MariaDB / MySQL)

La persistencia de datos del sistema gestiona la autenticación de perfiles, mapeo vectorial, grilla horaria y comunicaciones institucionales:

* **Esquema y Scripts SQL:** El modelo relacional detallado (tablas `usuarios`, `salas`, `horarios`, `anuncios`, llaves foráneas y datos sintéticos de prueba) se encuentra centralizado en los scripts de la carpeta [`BD/`](../BD/database.sql).

---

### 4. Estructura por Fases del Proyecto

#### FASE 1: MVP (Producto Mínimo Viable - Entrega al 27/10/2026)
* **Aplicación Móvil Android Nativa:** Desarrollo en Java enfocado en alto rendimiento para hardware móvil.
* **Mapa Interactivo SVG:** Renderizado vectorial responsivo, búsqueda de salas y trazado de rutas asistido.
* **Autenticación por RUT:** Inicio de sesión según perfiles (Estudiante, Docente, UTP, Inspectoría, Desarrollador).
* **Módulo de Horarios y Anuncios:** Consulta de bloques de clases y comunicados en tiempo real.
* **Estrategia de Datos Sintéticos (Mock Data):** Carga inicial con scripts `.sql` local para desarrollo e integración continua.

#### FASE 2: Expansión y Madurez (Post-Aprobación Académica)
* **Panel Web de Administración para PC:** Interfaz web en navegador optimizada para carga masiva de horarios (CSV/Excel) y gestión administrativa.
* **Migración a Datos Reales:** Carga formal de la nómina y planificación entregada por el establecimiento.

#### FASE 3: Ecosistema Modular y Comercialización (Largo Plazo)
* **Arquitectura Modular Extensible:** Integración opcional de nuevos servicios (Minuta del Casino, Solicitudes con Convivencia Escolar, Reservas CRA).
* **Distribución Marca Blanca:** Proyección de comercialización para otros establecimientos educativos.

---

### 5. Revisión SMART e Indicadores de Logro

| Indicador | Método de Verificación |
| :--- | :--- |
| La aplicación ejecuta e inicia sesión por RUT en todos los roles configurados. | Pruebas de acceso en APK Android con cuentas de prueba. |
| El mapa SVG resalta la sala seleccionada y traza la ruta correspondiente. | Selección de destinos en el buscador e inspección gráfica del mapa. |
| Consulta de horarios según curso y profesor. | Verificación de grilla horaria en la vista de usuario. |
| Publicación y recepción de anuncios institucionales. | Emisión de comunicado por UTP y validación en app móvil. |

---

### 6. Estrategia de Servidores e Infraestructura (Dev $\rightarrow$ Prod)

1. **Entorno de Desarrollo (Actual):** Laptop personal con Fedora Linux y MariaDB Server local.
2. **Entorno de Producción (Opciones de Despliegue):**
   * **Opción A (Recomendada):** *Oracle Cloud Always Free Tier* (VPS sin costo en la nube).
   * **Opción B:** Servidor local dedicado en infraestructura del liceo.
   * **Opción C:** VPS administrado contratado por el sostenedor.

---

## PARTE 2: ENTORNO PERSONAL DE DESARROLLO (CONFIGURACIÓN LOCAL)

### 1. Hardware y Sistema Operativo
* **Equipo:** Laptop personal con procesador Intel Celeron y 4 GB de memoria RAM.
* **Sistema Operativo:** Fedora Linux.
* **Ajustes de Rendimiento:** Servicios en segundo plano optimizados (`Akonadi`, `Baloo`, `PackageKit` desactivados).

### 2. Stack de Herramientas Instaladas
* **Entorno Móvil:** Android Studio (Java).
* **Editor Secundario:** VS Code con extensiones para Java y MariaDB/MySQL.
* **Diseño Vectorial:** Inkscape.
* **Base de Datos:** MariaDB Server (`mariadb.service` local).
