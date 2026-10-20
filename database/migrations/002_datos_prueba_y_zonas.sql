-- =========================================================
-- Migración 002: datos de prueba (mock) válidos y zonas del mapa
-- Solo datos sintéticos. Las contraseñas de prueba están en docs/api.md.
-- Requiere la migración 001.
-- =========================================================
USE colegio_db;

-- 1. Usuarios: RUT con dígito verificador válido (formato 12345678-9, sin puntos)
--    y hashes bcrypt reales. Se conservan los id 1-4 porque otras tablas los referencian.
UPDATE usuarios SET rut = '20100001-7', nombre = 'Daniel', apellido = 'Creador',
    password_hash = '$2b$10$AK.EMs9bF4BS5CiZokDlCu2YtA6FgbKOQSvcnEOo7b38.V2eZSY5i' WHERE id_usuario = 1;
UPDATE usuarios SET rut = '20100002-5', nombre = 'Marta', apellido = 'Rojas',
    password_hash = '$2b$10$ttZZdSs0MUI08SUqonDBf.vkG3NQ5yG8PGQ96j7S5K/G5a8Y9.kbi' WHERE id_usuario = 2;
UPDATE usuarios SET rut = '20100004-1', nombre = 'Juan', apellido = 'Carlos',
    password_hash = '$2b$10$iHntfRNoYKIKWgCceqv04.HrK4XMlJc3eI94Gb2.sxzpLxDaLrEo.' WHERE id_usuario = 3;
UPDATE usuarios SET rut = '20100006-8', nombre = 'Jorge', apellido = 'Badani',
    password_hash = '$2b$10$GbmfO1/IP0eqccw44mcHdexEALZO8I0YG6R6xbSZsUUmFc/gji87q' WHERE id_usuario = 4;

INSERT INTO usuarios (rut, password_hash, nombre, apellido, id_rol)
SELECT v.rut, v.hash, v.nombre, v.apellido, r.id_rol
FROM (
    SELECT '20100003-3' AS rut, '$2b$10$yohhNkbsTZST0wWBxnB4weoISg/U2niKabtLG2wIvXwylX7iSZ7.C' AS hash, 'Pablo' AS nombre, 'Soto' AS apellido, 'inspectoria' AS rol
    UNION ALL SELECT '20100005-K', '$2b$10$xQ2Ai/Hwz.4FRaJQjZvzl.cy/WPstcXyDxvXyHtK8Yk/KzDJpT3pu', 'Ana', 'Fuentes', 'profesor'
    UNION ALL SELECT '20100007-6', '$2b$10$OOo7PczdVK7/cHA3n6Jj0O.DPRFH3jSTahx1ID/4nVBh4JFUArsri', 'Camila', 'Vega', 'alumno'
    UNION ALL SELECT '20100008-4', '$2b$10$c3YWgPNBhJdwfQSwMyLYB.DL802f4YFCBHlceM5.nv8HsWNuUOGVe', 'Diego', 'Torres', 'alumno'
) v
JOIN roles r ON r.nombre = v.rol;

ALTER TABLE usuarios
    ADD CONSTRAINT chk_usuarios_rut_formato CHECK (rut REGEXP '^[0-9]{7,8}-[0-9K]$');

-- 2. Zonas del mapa general (IDs según design/standard_ids.md y mapa_liceo_concepto.svg)
INSERT INTO zonas (id_zona, nombre, tipo, id_svg) VALUES
    ('acceso_peatonal_loa', 'Acceso peatonal Av. Loa', 'ACCESO', 'acceso_peatonal_loa'),
    ('zona_estacionamiento', 'Estacionamientos', 'OTRO', 'zona_estacionamiento'),
    ('bloque_h', 'Portería / Control de acceso', 'BLOQUE', 'bloque_h'),
    ('bloque_f', 'Pabellón F', 'BLOQUE', 'bloque_f'),
    ('bloque_i', 'Pabellón I', 'BLOQUE', 'bloque_i'),
    ('bloque_j', 'Pabellón J', 'BLOQUE', 'bloque_j'),
    ('bloque_b', 'Bloque B', 'BLOQUE', 'bloque_b'),
    ('bloque_c', 'Bloque C', 'BLOQUE', 'bloque_c'),
    ('bloque_d', 'Bloque D', 'BLOQUE', 'bloque_d'),
    ('bloque_e', 'Bloque E', 'BLOQUE', 'bloque_e'),
    ('bloque_k', 'Gimnasio / Multicancha techada', 'DEPORTE', 'bloque_k'),
    ('bloque_l', 'Bloque L', 'BLOQUE', 'bloque_l'),
    ('patio_central', 'Patio central', 'PATIO', 'patio_central'),
    ('cancha_gimnasio_k', 'Multicancha interior (Bloque K)', 'DEPORTE', 'cancha_gimnasio_k');

-- 3. SVG de detalle disponibles hoy (zona central: sectores B, C, D y J, dos pisos)
INSERT INTO zonas_svg_detalle (id_zona, piso, archivo_svg)
SELECT z.id_zona, p.piso, p.archivo
FROM zonas z
JOIN (
    SELECT 1 AS piso, 'zona_central_planta_baja.svg' AS archivo
    UNION ALL SELECT 2, 'zona_central_segundo_piso.svg'
) p
WHERE z.id_zona IN ('bloque_b', 'bloque_c', 'bloque_d', 'bloque_j');

-- 4. Espacios -> zona. El pabellón A (Dirección/UTP) queda sin zona hasta confirmar
--    a qué sector del SVG corresponde. id_svg queda NULL: las salas aún no están en el mapa.
UPDATE espacios SET id_zona = CONCAT('bloque_', LOWER(pabellon_bloque))
WHERE pabellon_bloque IN ('B', 'I', 'J', 'K', 'L');

-- 5. Bloques horarios (mock)
INSERT INTO bloques_horarios (numero, nombre, tipo, hora_inicio, hora_fin) VALUES
    (1, 'Bloque 1', 'CLASE', '08:00:00', '08:45:00'),
    (2, 'Bloque 2', 'CLASE', '08:45:00', '09:30:00'),
    (3, 'Recreo 1', 'RECREO', '09:30:00', '09:45:00'),
    (4, 'Bloque 3', 'CLASE', '09:45:00', '10:30:00'),
    (5, 'Bloque 4', 'CLASE', '10:30:00', '11:15:00'),
    (6, 'Recreo 2', 'RECREO', '11:15:00', '11:30:00'),
    (7, 'Bloque 5', 'CLASE', '11:30:00', '12:15:00'),
    (8, 'Bloque 6', 'CLASE', '12:15:00', '13:00:00'),
    (9, 'Almuerzo', 'ALMUERZO', '13:00:00', '13:45:00'),
    (10, 'Bloque 7', 'CLASE', '13:45:00', '14:30:00'),
    (11, 'Bloque 8', 'CLASE', '14:30:00', '15:15:00'),
    (12, 'Salida', 'SALIDA', '15:15:00', '15:30:00');

-- 6. Cursos, matrícula y horarios de ejemplo (sin solapamientos de curso, profesor ni sala)
UPDATE cursos SET id_profesor_jefe = (SELECT id_usuario FROM usuarios WHERE rut = '20100005-K')
WHERE id_curso = '2A';

INSERT INTO curso_alumno (id_curso, id_alumno)
SELECT '2A', id_usuario FROM usuarios WHERE rut IN ('20100007-6', '20100008-4');

INSERT INTO horarios (id_curso, id_materia, id_profesor, id_espacio, id_bloque, dia_semana, hora_inicio, hora_fin)
SELECT h.id_curso, m.id_materia, u.id_usuario, h.id_espacio, b.id_bloque, h.dia, b.hora_inicio, b.hora_fin
FROM (
    SELECT '1F' AS id_curso, 'Matemáticas' AS materia, '20100004-1' AS rut, 'A_32' AS id_espacio, 1 AS bloque, 1 AS dia
    UNION ALL SELECT '1F', 'Matemáticas', '20100004-1', 'A_32', 2, 1
    UNION ALL SELECT '1F', 'Lenguaje', '20100005-K', 'A_32', 4, 1
    UNION ALL SELECT '1F', 'Electrónica', '20100004-1', 'ELECTRON', 1, 2
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 1, 1
    UNION ALL SELECT '2A', 'Lenguaje', '20100005-K', 'A_23', 2, 1
    UNION ALL SELECT '2A', 'Matemáticas', '20100004-1', 'A_23', 4, 1
) h
JOIN materias m ON m.nombre = h.materia
JOIN usuarios u ON u.rut = h.rut
JOIN bloques_horarios b ON b.numero = h.bloque;

-- 7. Anuncios de ejemplo: global (id_curso NULL) y por curso
INSERT INTO anuncios (id_curso, id_autor, titulo, contenido, prioridad)
SELECT NULL, id_usuario, 'Bienvenidos a LiceoMap',
    'Esta es una versión de prueba con datos sintéticos.', 'INFORMATIVO'
FROM usuarios WHERE rut = '20100002-5';

INSERT INTO anuncios (id_curso, id_autor, titulo, contenido, prioridad)
SELECT '1F', id_usuario, 'Prueba de Matemáticas',
    'El lunes se rinde la prueba del primer semestre.', 'RECORDATORIO'
FROM usuarios WHERE rut = '20100004-1';
