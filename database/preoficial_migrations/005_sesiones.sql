CREATE TABLE auth_sessions (
    id_sesion CHAR(64) PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    expira_en DATETIME NOT NULL,
    revocada BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    INDEX idx_sesiones_usuario(id_usuario, expira_en)
) ENGINE=InnoDB;
