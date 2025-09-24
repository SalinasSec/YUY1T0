from BD.conexionSQL import DAO, Error

# ------------------ USUARIOS/ADMIN ------------------


def registrar(nombre, email, password):
    conn = DAO.yconectar()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password),
        )
        conn.commit()
        return True
    except Error as e:
        print("Error:", e)
        return False
    finally:
        cur.close()
        conn.close()


def login(email, password):
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ------------------ TURNOS ------------------


def crearTurno(usuario_id):
    conn = DAO.yconectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO turnos (usuario_id) VALUES (%s)", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()


def listarTurnos():
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """SELECT t.id, u.nombre, u.email, t.estado, t.fecha
                   FROM turnos t JOIN usuarios u ON u.id = t.usuario_id
                   ORDER BY t.fecha"""
    )
    turnos = cur.fetchall()
    cur.close()
    conn.close()
    return turnos


def aceptarTurno(turnoId):
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT estado FROM turnos WHERE id=%s", (turnoId,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return "no_existe"
    estado = row["estado"]
    if estado == "atendido":
        cur.close()
        conn.close()
        return "ya_atendido"
    elif estado == "rechazado":
        cur.close()
        conn.close()
        return "rechazado"
    elif estado == "cancelado":
        cur.close()
        conn.close()
        return "cancelado"
    elif estado == "pendiente":
        cur.execute("UPDATE turnos SET estado='aceptado' WHERE id=%s", (turnoId,))
        conn.commit()
        cur.close()
        conn.close()
        return "ok"


def rechazarTurno(turnoId):
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT estado FROM turnos WHERE id=%s", (turnoId,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return "no_existe"
    estado = row["estado"]
    if estado == "atendido":
        cur.close()
        conn.close()
        return "ya_atendido"
    elif estado == "rechazado":
        cur.close()
        conn.close()
        return "rechazado"
    elif estado == "cancelado":
        cur.close()
        conn.close()
        return "cancelado"
    else:
        cur.execute("UPDATE turnos SET estado='rechazado' WHERE id=%s", (turnoId,))
        conn.commit()
        cur.close()
        conn.close()
        return "ok"


def atenderTurno(turnoId):
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT estado FROM turnos WHERE id=%s", (turnoId,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return "no_existe"
    estado = row["estado"]
    if estado == "pendiente":
        cur.close()
        conn.close()
        return "falta_aceptar"
    elif estado == "atendido":
        cur.close()
        conn.close()
        return "ya_atendido"
    elif estado == "rechazado":
        cur.close()
        conn.close()
        return "rechazado"
    elif estado == "cancelado":
        cur.close()
        conn.close()
        return "cancelado"
    elif estado == "aceptado":
        cur.execute("UPDATE turnos SET estado='atendido' WHERE id=%s", (turnoId,))
        conn.commit()
        cur.close()
        conn.close()
        return "ok"


def cancelarTurno(turnoId, usuarioId):
    conn = DAO.yconectar()
    cur = conn.cursor()
    cur.execute(
        "UPDATE turnos SET estado='cancelado' WHERE id=%s AND usuario_id=%s",
        (turnoId, usuarioId),
    )
    conn.commit()
    cur.close()
    conn.close()


def obtenerCorreo(turnoId):
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT t.id, u.nombre, u.email, t.estado FROM turnos t JOIN usuarios u ON u.id = t.usuario_id WHERE t.id=%s",
        (turnoId,),
    )
    turno = cur.fetchone()
    cur.close()
    conn.close()
    return turno


def existeUsuario(email):
    conn = DAO.yconectar()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM usuarios WHERE email=%s", (email,))
    fila = cur.fetchone()
    cur.close()
    conn.close()
    return fila is not None
