-- =========================================================
-- Migración 001: zonas/mapa en dos niveles, bloques horarios y anuncios globales
-- Aditiva: no elimina tablas ni datos existentes.
-- =========================================================
USE colegio_db;

-- 1. Rol de Inspectoría
INSERT IGNORE INTO roles (nombre) VALUES ('inspectoria');

-- 2. Zonas / pabellones del mapa general (nivel 1).
--    id_zona coincide con el id del elemento en el SVG (ver design/standard_ids.md).
CREATE TABLE IF NOT EXISTS zonas (
    id_zona VARCHAR(40) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('BLOQUE', 'PATIO', 'ACCESO', 'DEPORTE', 'OTRO') NOT NULL,
    id_svg VARCHAR(60) NULL,
    latitud DECIMAL(10,8) NULL,
    longitud DECIMAL(11,8) NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_zonas_coordenadas CHECK (
        (latitud IS NULL AND longitud IS NULL) OR
        (latitud BETWEEN -90 AND 90 AND longitud BETWEEN -180 AND 180)
    ),
    UNIQUE KEY uq_zonas_id_svg (id_svg)
) ENGINE = InnoDB;

-- 3. SVG de detalle por zona y piso (nivel 2). La app lo carga al expandir una zona.
CREATE TABLE IF NOT EXISTS zonas_svg_detalle (
    id_zona VARCHAR(40) NOT NULL,
    piso INT NOT NULL,
    archivo_svg VARCHAR(150) NOT NULL,
    PRIMARY KEY (id_zona, piso),
    CONSTRAINT fk_zonas_detalle_zona
        FOREIGN KEY (id_zona) REFERENCES zonas(id_zona)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_zonas_detalle_piso CHECK (piso >= 0)
) ENGINE = InnoDB;

-- 4. Espacios: pertenencia a zona e id del SVG (NULL hasta que la sala exista en el mapa)
ALTER TABLE espacios
    ADD COLUMN IF NOT EXISTS id_zona VARCHAR(40) NULL AFTER pabellon_bloque,
    ADD COLUMN IF NOT EXISTS id_svg VARCHAR(60) NULL AFTER id_zona;

ALTER TABLE espacios
    ADD CONSTRAINT fk_espacios_zona
        FOREIGN KEY (id_zona) REFERENCES zonas(id_zona)
        ON UPDATE CASCADE ON DELETE SET NULL,
    ADD UNIQUE KEY uq_espacios_id_svg (id_svg);

-- 5. Grafo de navegación (estructura lista; se llena cuando existan nodos en el SVG)
CREATE TABLE IF NOT EXISTS nodos_ruta (
    id_nodo VARCHAR(60) PRIMARY KEY,
    id_zona VARCHAR(40) NULL,
    id_espacio VARCHAR(20) NULL,
    piso INT NOT NULL DEFAULT 1,
    x DECIMAL(9,2) NULL,
    y DECIMAL(9,2) NULL,
    CONSTRAINT fk_nodos_zona
        FOREIGN KEY (id_zona) REFERENCES zonas(id_zona)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_nodos_espacio
        FOREIGN KEY (id_espacio) REFERENCES espacios(id_espacio)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_nodos_piso CHECK (piso >= 0)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS aristas_ruta (
    id_arista INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_nodo_origen VARCHAR(60) NOT NULL,
    id_nodo_destino VARCHAR(60) NOT NULL,
    peso DECIMAL(8,2) NOT NULL,
    accesible BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_aristas_origen
        FOREIGN KEY (id_nodo_origen) REFERENCES nodos_ruta(id_nodo)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_aristas_destino
        FOREIGN KEY (id_nodo_destino) REFERENCES nodos_ruta(id_nodo)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_aristas_peso CHECK (peso > 0),
    UNIQUE KEY uq_aristas (id_nodo_origen, id_nodo_destino)
) ENGINE = InnoDB;

-- 6. Bloques horarios (clases, recreos, almuerzo, salida)
CREATE TABLE IF NOT EXISTS bloques_horarios (
    id_bloque INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    numero TINYINT UNSIGNED NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    tipo ENUM('CLASE', 'RECREO', 'ALMUERZO', 'SALIDA') NOT NULL DEFAULT 'CLASE',
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    CONSTRAINT chk_bloques_horas CHECK (hora_inicio < hora_fin),
    UNIQUE KEY uq_bloques_numero (numero)
) ENGINE = InnoDB;

ALTER TABLE horarios
    ADD COLUMN IF NOT EXISTS id_bloque INT UNSIGNED NULL AFTER id_espacio;

ALTER TABLE horarios
    ADD CONSTRAINT fk_horarios_bloque
        FOREIGN KEY (id_bloque) REFERENCES bloques_horarios(id_bloque)
        ON UPDATE CASCADE ON DELETE SET NULL;

-- 7. Anuncios globales (id_curso NULL) y prioridad
ALTER TABLE anuncios
    MODIFY COLUMN id_curso VARCHAR(10) NULL,
    ADD COLUMN IF NOT EXISTS prioridad ENUM('INFORMATIVO', 'URGENTE', 'RECORDATORIO')
        NOT NULL DEFAULT 'INFORMATIVO' AFTER contenido;
