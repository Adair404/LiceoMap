-- Solo aditiva. No reejecutar las migraciones históricas 001–003.
CREATE TABLE anuncios_historial (
    id_historial BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_anuncio INT UNSIGNED NOT NULL,
    id_actor INT UNSIGNED NOT NULL,
    accion ENUM('CREAR','EDITAR','RETIRAR') NOT NULL,
    datos JSON NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_anuncio) REFERENCES anuncios(id_anuncio) ON DELETE RESTRICT,
    FOREIGN KEY (id_actor) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    INDEX idx_historial_anuncio(id_anuncio, id_historial)
) ENGINE=InnoDB;
