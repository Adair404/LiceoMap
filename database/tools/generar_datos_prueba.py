"""Genera la migración 003 (datos de prueba ampliados) y docs/datos_prueba.md.

Solo datos sintéticos. Es determinista (semilla fija), así que los RUT y nombres
no cambian entre ejecuciones; los hashes bcrypt sí cambian por su sal.

Uso (desde la raíz del repo):
    api/.venv/bin/python database/tools/generar_datos_prueba.py
"""
import random
import unicodedata
from pathlib import Path

import bcrypt

RAIZ = Path(__file__).resolve().parents[2]
SQL_SALIDA = RAIZ / "database" / "migrations" / "003_datos_prueba_ampliados.sql"
DOC_SALIDA = RAIZ / "docs" / "datos_prueba.md"

MARCA = "-- >>> DATOS DE PRUEBA AMPLIADOS (migración 003, generado por database/tools/generar_datos_prueba.py)"
PASS = {"dev": "Dev2026!", "utp": "Utp2026!", "inspectoria": "Insp2026!",
        "profesor": "Prof2026!", "alumno": "Alum2026!"}

NOMBRES_F = ["Sofía", "Valentina", "Martina", "Isidora", "Antonella", "Catalina", "Javiera", "Fernanda",
             "Constanza", "Francisca", "Amanda", "Florencia", "Renata", "Josefa", "Agustina", "Emilia",
             "Daniela", "Camila", "Trinidad", "Paula", "Rocío", "Bárbara", "Ignacia", "Maite"]
NOMBRES_M = ["Matías", "Benjamín", "Vicente", "Martín", "Joaquín", "Tomás", "Sebastián", "Cristóbal",
             "Maximiliano", "Nicolás", "Lucas", "Diego", "Felipe", "Ignacio", "Gabriel", "Bastián",
             "Álvaro", "Rodrigo", "Franco", "Esteban", "Cristian", "Alonso", "Ángel", "Gonzalo"]
APELLIDOS = ["González", "Muñoz", "Rojas", "Díaz", "Pérez", "Soto", "Contreras", "Silva", "Martínez", "Sepúlveda",
             "Morales", "Rodríguez", "López", "Araya", "Fuentes", "Hernández", "Torres", "Espinoza", "Vásquez",
             "Castillo", "Reyes", "Gutiérrez", "Tapia", "Campos", "Cortés", "Núñez", "Figueroa", "Riquelme",
             "Carrasco", "Vera", "Álvarez", "Cáceres", "Bravo", "Molina", "Valenzuela", "Pizarro", "Leiva",
             "Guzmán", "Ortiz", "Navarro", "Jara", "Aguilera", "Godoy", "Orellana", "Salazar", "Medina"]

# Los 8 primeros ya existen desde la migración 002
EXISTENTES = [
    ("20100001-7", "Daniel", "Creador", "dev"),
    ("20100002-5", "Marta", "Rojas", "utp"),
    ("20100003-3", "Pablo", "Soto", "inspectoria"),
    ("20100004-1", "Juan", "Carlos", "profesor"),
    ("20100005-K", "Ana", "Fuentes", "profesor"),
    ("20100006-8", "Jorge", "Badani", "alumno"),
    ("20100007-6", "Camila", "Vega", "alumno"),
    ("20100008-4", "Diego", "Torres", "alumno"),
]
# Personal nuevo: (RUT sin DV, nombre, apellido, rol)
PERSONAL_NUEVO = [
    (13456789, "Héctor", "Carrasco Lagos", "utp"),
    (14234567, "Rosa", "Valenzuela Mena", "inspectoria"),
    (12876543, "Roberto", "Muñoz Parra", "profesor"),
    (15345678, "Carolina", "Pizarro Ibáñez", "profesor"),
    (13987654, "Felipe", "Araya Sandoval", "profesor"),
    (14765432, "Patricia", "Leiva Rivas", "profesor"),
    (12654321, "Sergio", "Contreras Toro", "profesor"),
]

CURSOS = {"1F": ("A_32", 1), "1G": ("A_33", 1), "2A": ("A_23", 2), "2B": ("A_24", 2)}  # sala base, nivel
ALUMNOS_POR_CURSO = 30

MATERIAS = ["Matemáticas", "Lenguaje", "Historia", "Inglés", "Ciencias Naturales",
            "Educación Física", "Electrónica", "Computación", "Orientación"]
HORAS = {"Matemáticas": 6, "Lenguaje": 6, "Historia": 3, "Inglés": 3, "Ciencias Naturales": 4,
         "Educación Física": 2, "Electrónica": 3, "Computación": 2, "Orientación": 1}  # 30 por curso
SALA_FIJA = {"Educación Física": "GIM", "Electrónica": "ELECTRON", "Computación": "SCC"}
BLOQUES_CLASE = [1, 2, 4, 5, 7, 8]  # números de bloques_horarios tipo CLASE de la mañana


def dv(cuerpo):
    suma, peso = 0, 2
    for d in reversed(str(cuerpo)):
        suma += int(d) * peso
        peso = 2 if peso == 7 else peso + 1
    r = 11 - suma % 11
    return "0" if r == 11 else "K" if r == 10 else str(r)


def rut(cuerpo):
    return f"{cuerpo}-{dv(cuerpo)}"


def hash_pw(rol):
    return bcrypt.hashpw(PASS[rol].encode(), bcrypt.gensalt(10)).decode()


def sin_acentos(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().replace(" ", "")


def q(t):
    return "'" + t.replace("'", "''") + "'"


def main():
    rng = random.Random(2026)
    usados = {r for r, *_ in EXISTENTES}
    emails = set()

    def email(nombre, apellido):
        base = f"{sin_acentos(nombre.split()[0])}.{sin_acentos(apellido.split()[0])}"
        e, n = base, 1
        while e in emails:
            n += 1
            e = f"{base}{n}"
        emails.add(e)
        return f"{e}@liceomap.test"

    personal = [(rut(c), n, a, rol) for c, n, a, rol in PERSONAL_NUEVO]
    por_nombre = {n: r for r, n, _, _ in personal}
    usados |= {r for r, *_ in personal}
    jefes = {"1F": "20100004-1", "1G": por_nombre["Carolina"], "2A": "20100005-K", "2B": por_nombre["Felipe"]}
    docente = {
        "Matemáticas": "20100004-1", "Lenguaje": "20100005-K", "Historia": por_nombre["Roberto"],
        "Inglés": por_nombre["Carolina"], "Ciencias Naturales": por_nombre["Felipe"],
        "Educación Física": por_nombre["Patricia"], "Electrónica": por_nombre["Sergio"],
        "Computación": por_nombre["Sergio"],
    }

    alumnos = {c: [] for c in CURSOS}
    alumnos["1F"].append(("20100006-8", "Jorge", "Badani"))
    alumnos["2A"] += [("20100007-6", "Camila", "Vega"), ("20100008-4", "Diego", "Torres")]
    nuevos, combos = [], set()
    for curso, (_, nivel) in CURSOS.items():
        lo, hi = (23_300_000, 23_900_000) if nivel == 1 else (22_500_000, 23_100_000)
        while len(alumnos[curso]) < ALUMNOS_POR_CURSO:
            nombre = rng.choice(NOMBRES_F + NOMBRES_M)
            ape = f"{rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}"
            r = rut(rng.randint(lo, hi))
            if (nombre, ape) in combos or r in usados:
                continue
            combos.add((nombre, ape))
            usados.add(r)
            alumnos[curso].append((r, nombre, ape))
            nuevos.append((r, nombre, ape, "alumno"))

    def generar_horario(semilla):
        # Se llena franja por franja; si un curso se queda sin opción se reintenta con otra semilla
        r = random.Random(semilla)
        faltan = {(c, m): HORAS[m] for c in CURSOS for m in MATERIAS}
        ocup_prof, ocup_sala, por_dia, res = set(), set(), {}, []
        for d in range(1, 6):
            for b in BLOQUES_CLASE:
                cursos = list(CURSOS)
                r.shuffle(cursos)
                for c in cursos:
                    opciones = []
                    for m in MATERIAS:
                        prof = jefes[c] if m == "Orientación" else docente[m]
                        sala = SALA_FIJA.get(m, CURSOS[c][0])
                        if (faltan[(c, m)] > 0 and (prof, d, b) not in ocup_prof and (sala, d, b) not in ocup_sala
                                and por_dia.get((c, m, d), 0) < 2):
                            opciones.append((faltan[(c, m)] + r.random() * 2, m, prof, sala))
                    if not opciones:
                        return None
                    _, m, prof, sala = max(opciones)
                    ocup_prof.add((prof, d, b)); ocup_sala.add((sala, d, b))
                    por_dia[(c, m, d)] = por_dia.get((c, m, d), 0) + 1
                    faltan[(c, m)] -= 1
                    res.append((c, m, prof, sala, d, b))
        return sorted(res, key=lambda x: (x[0], x[4], x[5]))

    horario = next((h for h in (generar_horario(s) for s in range(1, 5000)) if h), None)
    assert horario, "No se pudo generar un horario sin choques"

    todos_nuevos = personal + nuevos
    sql = [
        "-- =========================================================",
        "-- Migración 003: datos de prueba ampliados (GENERADO)",
        "-- Generado por database/tools/generar_datos_prueba.py. Solo datos sintéticos.",
        "-- 4 cursos (1F, 1G, 2A, 2B) con 30 alumnos cada uno, personal por rol,",
        "-- horario semanal completo sin choques y anuncios. Requiere 001 y 002.",
        "-- Credenciales de prueba: docs/datos_prueba.md",
        "-- =========================================================",
        "USE colegio_db;", "",
        "-- Usuarios nuevos (el rol se resuelve por nombre)",
        "INSERT INTO usuarios (rut, password_hash, nombre, apellido, email, id_rol)",
        "SELECT v.rut, v.hash, v.nombre, v.apellido, v.email, r.id_rol FROM (",
    ]
    for i, (r_, n, a, rol) in enumerate(todos_nuevos):
        al = (lambda s: f" AS {s}") if i == 0 else (lambda s: "")
        pre = "SELECT " if i == 0 else "UNION ALL SELECT "
        sql.append(f"    {pre}{q(r_)}{al('rut')}, {q(hash_pw(rol))}{al('hash')}, {q(n)}{al('nombre')}, "
                   f"{q(a)}{al('apellido')}, {q(email(n, a))}{al('email')}, {q(rol)}{al('rol')}")
    sql += [") v JOIN roles r ON r.nombre = v.rol;", "", "-- Correos de los usuarios creados en la migración 002"]
    sql += [f"UPDATE usuarios SET email = {q(email(n, a))} WHERE rut = {q(r_)};" for r_, n, a, _ in EXISTENTES]

    sql += ["", "-- Profesores jefe y matrícula (se reemplaza la matrícula de los 4 cursos)"]
    for c, j in jefes.items():
        sql.append(f"UPDATE cursos SET id_profesor_jefe = (SELECT id_usuario FROM usuarios WHERE rut = {q(j)}) WHERE id_curso = {q(c)};")
    sql.append(f"DELETE FROM curso_alumno WHERE id_curso IN ({', '.join(q(c) for c in CURSOS)});")
    for c, lista in alumnos.items():
        sql.append(f"INSERT INTO curso_alumno (id_curso, id_alumno) SELECT {q(c)}, id_usuario FROM usuarios WHERE rut IN (")
        sql.append("    " + ", ".join(q(x[0]) for x in lista))
        sql.append(");")

    sql += ["", "-- Materias", "INSERT IGNORE INTO materias (nombre) VALUES " + ", ".join(f"({q(m)})" for m in MATERIAS) + ";",
            "", "-- Horario semanal (reemplaza los horarios de ejemplo anteriores)", "DELETE FROM horarios;",
            "INSERT INTO horarios (id_curso, id_materia, id_profesor, id_espacio, id_bloque, dia_semana, hora_inicio, hora_fin)",
            "SELECT h.id_curso, m.id_materia, u.id_usuario, h.id_espacio, b.id_bloque, h.dia, b.hora_inicio, b.hora_fin FROM ("]
    for i, (c, m, prof, sala, d, b) in enumerate(horario):
        al = (lambda s: f" AS {s}") if i == 0 else (lambda s: "")
        pre = "SELECT " if i == 0 else "UNION ALL SELECT "
        sql.append(f"    {pre}{q(c)}{al('id_curso')}, {q(m)}{al('materia')}, {q(prof)}{al('rut')}, "
                   f"{q(sala)}{al('id_espacio')}, {b}{al('bloque')}, {d}{al('dia')}")
    sql += [") h JOIN materias m ON m.nombre = h.materia JOIN usuarios u ON u.rut = h.rut",
            "JOIN bloques_horarios b ON b.numero = h.bloque;", ""]

    utp2 = rut(13456789)
    anuncios = [
        (None, "20100002-5", "Bienvenidos a LiceoMap", "Esta es una versión de prueba con datos sintéticos.", "INFORMATIVO"),
        (None, "20100003-3", "Suspensión de clases por lluvia", "Mañana no habrá clases en el liceo por alerta meteorológica.", "URGENTE"),
        (None, utp2, "Reunión de apoderados", "La reunión general será el próximo jueves a las 19:00 en el gimnasio.", "RECORDATORIO"),
        ("1F", "20100004-1", "Prueba de Matemáticas", "El lunes se rinde la prueba del primer semestre.", "RECORDATORIO"),
        ("1G", por_nombre["Carolina"], "Entrega de trabajo de Inglés", "El trabajo grupal se entrega el viernes antes del recreo.", "RECORDATORIO"),
        ("2A", "20100005-K", "Salida pedagógica", "Traer la autorización firmada hasta el miércoles.", "INFORMATIVO"),
        ("2B", por_nombre["Felipe"], "Laboratorio de Ciencias", "Traer delantal blanco para la clase del martes.", "INFORMATIVO"),
    ]
    sql += ["-- Anuncios (reemplaza los de ejemplo; NULL = global)", "DELETE FROM anuncios;",
            "INSERT INTO anuncios (id_curso, id_autor, titulo, contenido, prioridad)"]
    for i, (c, autor, t, cont, p) in enumerate(anuncios):
        pre = "SELECT " if i == 0 else "UNION ALL SELECT "
        sql.append(f"{pre}{q(c) if c else 'NULL'}, (SELECT id_usuario FROM usuarios WHERE rut = {q(autor)}), "
                   f"{q(t)}, {q(cont)}, {q(p)}")
    sql[-1] += ";"
    SQL_SALIDA.write_text("\n".join(sql) + "\n", encoding="utf-8")

    # database.sql consolidado: se reemplaza todo lo que sigue a la marca por la migración 003
    consolidado = RAIZ / "database" / "database.sql"
    texto = consolidado.read_text(encoding="utf-8")
    cabecera = texto[:texto.index(MARCA)] + MARCA + "\n"
    consolidado.write_text(cabecera + "\n".join(sql[9:]) + "\n", encoding="utf-8")  # sin cabecera ni USE

    d = ["# Datos de prueba (sintéticos)", "",
         "Generados por `database/tools/generar_datos_prueba.py` (migración `003`). **Ninguno corresponde a personas reales.**",
         "Las contraseñas son por rol y solo sirven en desarrollo. El RUT se puede escribir con o sin puntos.", "",
         "| Rol | Contraseña |", "|---|---|"]
    d += [f"| {r} | `{p}` |" for r, p in PASS.items()]
    nombres = {r: f"{n} {a}" for r, n, a, _ in EXISTENTES + personal}
    d += ["", "## Cursos", "", "| Curso | Sala base | Profesor jefe | Alumnos |", "|---|---|---|---|"]
    d += [f"| {c} | {s} | {nombres[jefes[c]]} | {len(alumnos[c])} |" for c, (s, _) in CURSOS.items()]
    mat = {}
    for m, r_ in docente.items():
        mat.setdefault(r_, []).append(m)
    for c, j in jefes.items():
        mat.setdefault(j, []).append(f"Orientación {c}")
    d += ["", "## Personal", "", "| RUT | Nombre | Rol | Materias |", "|---|---|---|---|"]
    d += [f"| {r_} | {n} {a} | {rol} | {', '.join(mat.get(r_, [])) or '—'} |"
          for r_, n, a, rol in EXISTENTES + personal if rol != "alumno"]
    d += ["", "## Alumnos"]
    for c, lista in alumnos.items():
        d += ["", f"### {c}", "", "| N° | RUT | Nombre |", "|---|---|---|"]
        d += [f"| {i} | {r_} | {n} {a} |" for i, (r_, n, a) in enumerate(lista, 1)]
    DOC_SALIDA.write_text("\n".join(d) + "\n", encoding="utf-8")
    print("alumnos:", sum(len(v) for v in alumnos.values()), "horarios:", len(horario), "usuarios nuevos:", len(todos_nuevos))


if __name__ == "__main__":
    main()
