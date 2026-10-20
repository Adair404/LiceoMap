# Guía Oficial de Nomenclatura e IDs Vectoriales (LiceoMap)

Convención técnica entre el plano SVG (Inkscape), el motor de rutas (Dijkstra / A*) y la base de datos `colegio_db`.

---

## 1. Capas Obligatorias en Inkscape (Layers)
* `layer_plano_referencia`: Imagen base del plano arquitectónico.
* `layer_estructura`: Muros, muros perimetrales y pilares.
* `layer_recintos`: Polígonos interactivos de recintos y bloques.
* `layer_nodos`: Grafo de puntos de navegación.
* `layer_aristas`: Conexiones fácticas entre nodos para cálculo de rutas.

---

## 2. IDs de Bloques y Pabellones Oficiales (Letras del Plano)

### Accesos y Perímetros
* `acceso_peatonal_loa` (Entrada peatonal principal por Avenida Loa)
* `acceso_vehicular_loa` (Entrada de vehículos por Avenida Loa)
* `zona_estacionamiento` (Sector estacionamientos Av. Loa)
* `limite_alfredo_thomas` (Límite norte por Calle Alfredo Thomas)

### Bloques de Infraestructura
* `bloque_h`: Portería / Control de acceso principal (Av. Loa)
* `bloque_f`: Pabellón longitudinal oeste (Sector sur)
* `bloque_i`: Pabellón longitudinal oeste (Sector central)
* `bloque_j`: Pabellón longitudinal oeste (Sector norte)
* `bloque_b`: Bloque central de aulas / administración
* `bloque_c`: Bloque este (Sector sur)
* `bloque_d`: Bloque este (Sector central)
* `bloque_e`: Bloque este (Sector norte)
* `bloque_k`: Gimnasio / Multicancha techada principal
* `bloque_l`: Edificación bordeadora norte (Calle Alfredo Thomas)

### Espacios Abiertos y Deportes
* `patio_central`: Patio principal de adoquines/mosaico
* `cancha_gimnasio_k`: Multicancha interior del Bloque K
* `cancha_exterior_este`: Cancha descubierta sector este

---

## 3. Formato de Sub-Recintos y Salas
Para definir las áreas internas dentro de cada bloque, se utiliza el prefijo del bloque seguido del identificador específico:

* **Salas / Aulas:** `sala_[bloque]_[numero]` (Ejemplo: `sala_b_01`, `sala_d_04`)
* **Baños:** `bano_[bloque]_[tipo]` (Ejemplo: `bano_f_damas`, `bano_b_varones`)
* **Oficinas / Especiales:** `oficina_[bloque]_[nombre]` (Ejemplo: `oficina_h_porteria`)

---

## 4. Nomenclatura de Nodos para Rutas (`layer_nodos`)
* **Nodos de Entrada a Bloques:** `node_ent_[id_bloque]` (Ejemplo: `node_ent_bloque_k`, `node_ent_bloque_h`)
* **Nodos de Pasillos/Intersecciones:** `node_pasillo_[bloque]_[numero]` (Ejemplo: `node_pasillo_b_01`)
* **Nodos de Patios y Accesos:** `node_patio_central_[numero]`, `node_acceso_loa`

---

## 5. Jerarquía de Mapa de Dos Niveles (zona → sala)
* **Nivel 1 (mapa general):** cada pabellón/zona es un elemento del SVG general cuyo `id` coincide con `zonas.id_zona` / `zonas.id_svg` en la BD (ej. `bloque_b`).
* **Nivel 2 (detalle):** al expandir una zona, la app carga un SVG de detalle registrado en `zonas_svg_detalle` (zona + piso → `archivo_svg`). Un mismo SVG puede cubrir varias zonas (hoy `zona_central_*.svg` cubre los bloques B, C, D y J).
* **Salas:** la clave estable es `espacios.id_espacio`. `espacios.id_svg` es opcional (NULL) y solo se completa cuando la sala tiene su `id` definitivo en un SVG de detalle; `espacios.id_zona` indica a qué zona pertenece.
* **IDs provisionales:** los ids `sala_provisional_*` de los SVG de detalle actuales no se usan en la BD hasta confirmar el mapeo definitivo.
