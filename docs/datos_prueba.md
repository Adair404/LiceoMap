> Referencia histórica importada de origin/main. Las credenciales de ejemplo
> ya no son válidas en las bases locales integradas. Consultar
> [PREOFICIAL_INTEGRACION.md](PREOFICIAL_INTEGRACION.md) para el arranque actual.
> Las cuentas locales usan contraseñas aleatorias en `.local/*.accounts.json`,
> archivos privados ignorados por Git. La cuenta local `20100008-4` está inactiva
> para verificar el rechazo de acceso. No reejecutar el generador ni las migraciones
> históricas 001–003 sobre bases existentes para recuperar estas contraseñas.

# Datos de prueba (sintéticos)

Generados por `database/tools/generar_datos_prueba.py` (migración `003`). **Ninguno corresponde a personas reales.**
Las contraseñas son por rol y solo sirven en desarrollo. El RUT se puede escribir con o sin puntos.

| Rol | Contraseña |
|---|---|
| dev | `Dev2026!` |
| utp | `Utp2026!` |
| inspectoria | `Insp2026!` |
| profesor | `Prof2026!` |
| alumno | `Alum2026!` |

## Cursos

| Curso | Sala base | Profesor jefe | Alumnos |
|---|---|---|---|
| 1F | A_32 | Juan Carlos | 30 |
| 1G | A_33 | Carolina Pizarro Ibáñez | 30 |
| 2A | A_23 | Ana Fuentes | 30 |
| 2B | A_24 | Felipe Araya Sandoval | 30 |

## Personal

| RUT | Nombre | Rol | Materias |
|---|---|---|---|
| 20100001-7 | Daniel Creador | dev | — |
| 20100002-5 | Marta Rojas | utp | — |
| 20100003-3 | Pablo Soto | inspectoria | — |
| 20100004-1 | Juan Carlos | profesor | Matemáticas, Orientación 1F |
| 20100005-K | Ana Fuentes | profesor | Lenguaje, Orientación 2A |
| 13456789-9 | Héctor Carrasco Lagos | utp | — |
| 14234567-6 | Rosa Valenzuela Mena | inspectoria | — |
| 12876543-3 | Roberto Muñoz Parra | profesor | Historia |
| 15345678-K | Carolina Pizarro Ibáñez | profesor | Inglés, Orientación 1G |
| 13987654-7 | Felipe Araya Sandoval | profesor | Ciencias Naturales, Orientación 2B |
| 14765432-4 | Patricia Leiva Rivas | profesor | Educación Física |
| 12654321-2 | Sergio Contreras Toro | profesor | Electrónica, Computación |

## Alumnos

### 1F

| N° | RUT | Nombre |
|---|---|---|
| 1 | 20100006-8 | Jorge Badani |
| 2 | 23836685-2 | Fernanda Reyes Bravo |
| 3 | 23883594-1 | Rodrigo Contreras Fuentes |
| 4 | 23814750-6 | Vicente Leiva Pizarro |
| 5 | 23302657-3 | Ignacio Carrasco Hernández |
| 6 | 23601193-3 | Bastián Soto Silva |
| 7 | 23814102-8 | Javiera Carrasco González |
| 8 | 23716512-8 | Esteban Reyes Araya |
| 9 | 23694625-8 | Daniela Tapia Tapia |
| 10 | 23380027-9 | Gonzalo Bravo Jara |
| 11 | 23884529-7 | Ángel Gutiérrez Soto |
| 12 | 23779668-3 | Lucas Vásquez Vásquez |
| 13 | 23624008-8 | Francisca Aguilera Medina |
| 14 | 23681201-4 | Valentina Medina Campos |
| 15 | 23718144-1 | Tomás Riquelme Soto |
| 16 | 23422104-3 | Ignacio Pizarro Cáceres |
| 17 | 23814883-9 | Martín Bravo Ortiz |
| 18 | 23740366-5 | Benjamín Molina Torres |
| 19 | 23843148-4 | Felipe Álvarez Bravo |
| 20 | 23435265-2 | Valentina Leiva Fuentes |
| 21 | 23407559-4 | Isidora Medina Molina |
| 22 | 23792873-3 | Alonso Navarro Riquelme |
| 23 | 23427940-8 | Francisca Álvarez Fuentes |
| 24 | 23792207-7 | Álvaro Salazar Vera |
| 25 | 23886988-9 | Alonso Valenzuela Torres |
| 26 | 23874775-9 | Benjamín Godoy Castillo |
| 27 | 23802155-3 | Rodrigo Bravo Salazar |
| 28 | 23608673-9 | Benjamín Riquelme López |
| 29 | 23457122-2 | Camila González Rojas |
| 30 | 23848288-7 | Rodrigo Ortiz Vera |

### 1G

| N° | RUT | Nombre |
|---|---|---|
| 1 | 23572745-5 | Cristóbal Campos López |
| 2 | 23836102-8 | Cristian Cáceres Vera |
| 3 | 23335253-5 | Cristóbal Riquelme Pizarro |
| 4 | 23403152-K | Trinidad Reyes Vera |
| 5 | 23840198-4 | Joaquín Salazar Medina |
| 6 | 23746459-1 | Daniela Carrasco Rodríguez |
| 7 | 23579409-8 | Ángel Álvarez Pérez |
| 8 | 23504038-7 | Cristóbal Campos Contreras |
| 9 | 23771224-2 | Gonzalo Figueroa Sepúlveda |
| 10 | 23773149-2 | Sofía Soto González |
| 11 | 23508448-1 | Ignacio Valenzuela Soto |
| 12 | 23346828-2 | Emilia Silva Navarro |
| 13 | 23674604-6 | Lucas Espinoza Godoy |
| 14 | 23815887-7 | Francisca González Reyes |
| 15 | 23533756-8 | Cristian Martínez Valenzuela |
| 16 | 23829238-7 | Sebastián Guzmán Martínez |
| 17 | 23467899-K | Trinidad Soto Figueroa |
| 18 | 23832364-9 | Constanza Guzmán Castillo |
| 19 | 23845291-0 | Vicente Cortés Sepúlveda |
| 20 | 23411289-9 | Renata Cortés González |
| 21 | 23663874-K | Matías Pérez Díaz |
| 22 | 23326824-0 | Rodrigo Tapia Muñoz |
| 23 | 23618422-6 | Maximiliano Álvarez Reyes |
| 24 | 23821739-3 | Joaquín Reyes Silva |
| 25 | 23479027-7 | Tomás Leiva Navarro |
| 26 | 23517040-K | Francisca Guzmán Molina |
| 27 | 23781104-6 | Martín Navarro Gutiérrez |
| 28 | 23372884-5 | Gabriel Fuentes Orellana |
| 29 | 23504990-2 | Diego Núñez Rojas |
| 30 | 23871229-7 | Rodrigo Rodríguez Rojas |

### 2A

| N° | RUT | Nombre |
|---|---|---|
| 1 | 20100007-6 | Camila Vega |
| 2 | 20100008-4 | Diego Torres |
| 3 | 22697687-6 | Isidora Carrasco Aguilera |
| 4 | 22521464-6 | Sebastián Medina Orellana |
| 5 | 22729348-9 | Constanza Aguilera Molina |
| 6 | 22695040-0 | Nicolás Martínez Morales |
| 7 | 23058902-K | Matías Espinoza Riquelme |
| 8 | 22819720-3 | Vicente Soto Cortés |
| 9 | 22776240-3 | Florencia Tapia Rodríguez |
| 10 | 22801644-6 | Tomás Cáceres Figueroa |
| 11 | 23044562-1 | Tomás Rodríguez Reyes |
| 12 | 23052863-2 | Sebastián Carrasco Silva |
| 13 | 22724742-8 | Nicolás Espinoza Contreras |
| 14 | 22976172-2 | Agustina González Soto |
| 15 | 23071536-K | Rodrigo Gutiérrez Figueroa |
| 16 | 22869046-5 | Franco Rodríguez Muñoz |
| 17 | 23064531-0 | Amanda Tapia Pizarro |
| 18 | 22794096-4 | Josefa Silva Navarro |
| 19 | 23097515-9 | Diego Leiva Araya |
| 20 | 23082729-K | Trinidad Leiva Espinoza |
| 21 | 22601114-5 | Constanza Contreras Torres |
| 22 | 22563361-4 | Martín Morales Contreras |
| 23 | 22611484-K | Ignacia Rodríguez Aguilera |
| 24 | 22567019-6 | Maximiliano Reyes Espinoza |
| 25 | 22773529-5 | Trinidad Reyes Morales |
| 26 | 22931638-9 | Daniela Pérez González |
| 27 | 22560095-3 | Daniela Figueroa González |
| 28 | 22824973-4 | Javiera Hernández Muñoz |
| 29 | 23088438-2 | Fernanda Contreras Orellana |
| 30 | 22978197-9 | Felipe Tapia Reyes |

### 2B

| N° | RUT | Nombre |
|---|---|---|
| 1 | 22539857-7 | Gabriel Jara Aguilera |
| 2 | 22726110-2 | Benjamín Reyes Ortiz |
| 3 | 22625242-8 | Gabriel Vera Riquelme |
| 4 | 22763798-6 | Esteban Campos Bravo |
| 5 | 22560430-4 | Matías Vásquez Tapia |
| 6 | 22524812-5 | Gonzalo Medina Riquelme |
| 7 | 22803621-8 | Trinidad Salazar Gutiérrez |
| 8 | 22936875-3 | Ángel Silva Castillo |
| 9 | 23068492-8 | Rocío Guzmán Muñoz |
| 10 | 22558872-4 | Bárbara López Pizarro |
| 11 | 22628644-6 | Ángel Silva Morales |
| 12 | 23047968-2 | Fernanda Rojas Martínez |
| 13 | 22816922-6 | Ignacia Ortiz Aguilera |
| 14 | 22632432-1 | Valentina Riquelme Guzmán |
| 15 | 22895504-3 | Ignacia Figueroa Cortés |
| 16 | 22730230-5 | Emilia Figueroa Godoy |
| 17 | 22529797-5 | Constanza Rodríguez Valenzuela |
| 18 | 23081852-5 | Franco Medina Valenzuela |
| 19 | 22739343-2 | Benjamín Torres Sepúlveda |
| 20 | 23067436-1 | Valentina Muñoz Espinoza |
| 21 | 22830033-0 | Sebastián Figueroa Torres |
| 22 | 22593791-5 | Constanza Jara Guzmán |
| 23 | 23039017-7 | Florencia Pizarro Rojas |
| 24 | 23045730-1 | Daniela Gutiérrez Jara |
| 25 | 22511963-5 | Gonzalo Reyes Díaz |
| 26 | 22561128-9 | Álvaro Hernández Álvarez |
| 27 | 22658174-K | Agustina Orellana Bravo |
| 28 | 22877415-4 | Gonzalo Núñez Medina |
| 29 | 22860382-1 | Agustina Pizarro Espinoza |
| 30 | 22981577-6 | Renata Campos Tapia |
