from tkinter import *
from tkinter import messagebox, simpledialog
from BD.metodos import *
from time import sleep
from os import name, system
from re import match
from TKINTER.correo import enviarCode, enviarAviso
from tkinter import ttk

codeGlobal = None
usuarioActual = None

# ------------------ FUNCIONES GENERALES ------------------


def cambiarPantalla(pantalla):
    for widget in framePrincipal.winfo_children():
        widget.destroy()
    pantalla()


def mostrarTurnos():
    turnos = listarTurnos()
    txt = ""
    for t in turnos:
        txt += f"ID:{t['id']} - {t['nombre']} ({t['email']}) [{t['estado']}]\n"
    messagebox.showinfo("Turnos", txt if txt else "No hay turnos")


def lPantallaT():
    system("cls" if name == "nt" else "clear")


def validarGmail(correo):
    patron = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    return match(patron, correo) is not None


# ------------------ LOGIN ------------------


def inicio():
    ttk.Button(
        framePrincipal,
        text="Iniciar Sesión",
        style="BotonGrande.TButton",
        width=20,
        command=lambda: cambiarPantalla(iniciarSesion),
    ).pack()
    ttk.Button(
        framePrincipal,
        text="Registrar",
        style="BotonGrande.TButton",
        width=20,
        command=lambda: cambiarPantalla(registrarI),
    ).pack(pady=50)


def registrarI():
    global codeGlobal, entryNombre, entryEmail, entryPass

    Label(
        framePrincipal,
        text="Registrarse",
        font=("Arial", 32, "bold"),
        bg="#DE9331",
    ).pack(pady=40)

    Label(
        framePrincipal,
        text="Nombre:",
        font=("Arial", 18),
        bg="#d6eaf8",
    ).pack()
    entryNombre = Entry(framePrincipal, font=("Arial", 18), width=30)
    entryNombre.pack(pady=10)

    Label(framePrincipal, text="Email:", font=("Arial", 18), bg="#d6eaf8").pack()
    entryEmail = Entry(framePrincipal, font=("Arial", 18), width=30)
    entryEmail.pack(pady=10)

    Label(framePrincipal, text="Password:", font=("Arial", 18), bg="#d6eaf8").pack()
    entryPass = Entry(framePrincipal, show="*", font=("Arial", 18), width=30)
    entryPass.pack(pady=10)

    ttk.Button(
        framePrincipal,
        text="Registrar",
        style="BotonGrande.TButton",
        width=20,
        command=funcRegister,
    ).pack(pady=30)

    ttk.Button(
        framePrincipal,
        text="Volver",
        style="BotonGrande.TButton",
        width=20,
        command=volver,
    ).pack(pady=30)


def funcRegister():
    nombre = entryNombre.get()
    email = entryEmail.get()
    password = entryPass.get()

    if nombre == "" or password == "" or email == "":
        messagebox.showerror("Error:", "Campos nulos")
        return
    if email == "admin@clinica.com":
        messagebox.showwarning("Aviso:", "Email ya utilizado")
        return
    if not validarGmail(email):
        messagebox.showerror(
            "Error:", "Ingreso de correo erroneo (ejemplo123@gmail.com)"
        )
        return
    if existeUsuario(email):
        messagebox.showwarning("Error", "El correo ya está registrado")
        return
    codeGlobal = enviarCode(email)
    messagebox.showinfo("Verificación", "Código enviado a tu correo")

    codeIngresado = simpledialog.askstring(
        "Verificación", "Ingrese el código recibido:"
    )

    if codeIngresado == codeGlobal:
        messagebox.showinfo("Éxito", "Usuario registrado")
        registrar(nombre, email, password)
    else:
        messagebox.showerror("Error", "Código Incorrecto")


def iniciarSesion():
    global usuarioActual, entryNombre, entryEmail, entryPass

    Label(
        framePrincipal,
        text="Iniciar Sesion",
        font=("Arial", 32, "bold"),
        bg="#92D9E0",
    ).pack(pady=40)

    Label(framePrincipal, text="Email:", font=("Arial", 18), bg="#d6eaf8").pack()
    entryEmail = Entry(framePrincipal, font=("Arial", 18), width=30)
    entryEmail.pack(pady=10)

    Label(framePrincipal, text="Password:", font=("Arial", 18), bg="#d6eaf8").pack()
    entryPass = Entry(framePrincipal, show="*", font=("Arial", 18), width=30)
    entryPass.pack(pady=10)

    ttk.Button(
        framePrincipal,
        text="Iniciar Sesión",
        style="BotonGrande.TButton",
        width=20,
        command=funcLogin,
    ).pack(pady=30)

    ttk.Button(
        framePrincipal,
        text="Volver",
        style="BotonGrande.TButton",
        width=20,
        command=volver,
    ).pack(pady=30)


def funcLogin():
    email = entryEmail.get()
    password = entryPass.get()
    user = login(email, password)
    if user:
        usuarioActual = user
        messagebox.showinfo("Bienvenido", f"Hola {user['nombre']} ({user['rol']})")
        if user["rol"] == "usuario":
            cambiarPantalla(pantallaUsuario)
        else:
            cambiarPantalla(pantallaAdmin)
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")
    print("Usuario Actual:", usuarioActual)


def salir():
    raiz.destroy()
    txt = "Programa Finalizado."
    for i in txt:
        print(i, end="", flush=True)
        sleep(0.09)
    sleep(2)
    lPantallaT()


def volver():
    cambiarPantalla(inicio)


# ------------------ PANEL USUARIO ------------------


def pantallaUsuario():
    Label(
        framePrincipal,
        text=f"Bienvenido {usuarioActual['nombre']}",
        font=("Arial", 22),
        bg="#eaf2f8",
    ).pack(pady=20)

    frame = Frame(framePrincipal, bg="#fef9e7")
    frame.pack(pady=40)

    def generarTurno():
        crearTurno(usuarioActual["id"])
        messagebox.showinfo("OK", "Turno generado")

    def cancelar():
        turnos = listarTurnos()
        for t in turnos:
            if t["email"] == usuarioActual["email"] and t["estado"] == "pendiente":
                cancelarTurno(t["id"], usuarioActual["id"])
                messagebox.showinfo("OK", "Turno cancelado")
                return
        messagebox.showinfo("Info", "No tienes turno pendiente")

    ttk.Button(
        frame,
        text="Generar Turno",
        style="BotonMediano.TButton",
        width=25,
        command=generarTurno,
    ).pack(pady=10)
    ttk.Button(
        framePrincipal,
        text="Cancelar Turno",
        style="BotonMediano.TButton",
        width=25,
        command=cancelar,
    ).pack(pady=10)
    ttk.Button(
        frame,
        text="Consultar Turnos",
        style="BotonMediano.TButton",
        width=25,
        command=mostrarTurnos,
    ).pack(pady=10)
    ttk.Button(
        frame,
        text="Cerrar Sesión",
        style="BotonMediano.TButton",
        width=25,
        command=lambda: cambiarPantalla(inicio),
    ).pack(pady=20)


# ------------------ PANEL ADMIN ------------------


def pantallaAdmin():
    Label(
        framePrincipal,
        text="Panel de Administración",
        font=("Arial", 24, "bold"),
        bg="#fef9e7",
    ).pack(pady=20)

    frame = Frame(framePrincipal, bg="#fef9e7")
    frame.pack(pady=40)

    def aceptar():
        tid = simpledialog.askstring("Turno", "ID del turno:")
        if tid:
            res = aceptarTurno(int(tid))
            if res == "ok":
                messagebox.showinfo("OK", "Turno Aceptado")
            elif res == "ya_atendido":
                messagebox.showwarning("Aviso", "Este turno ya fue atendido")
            elif res == "rechazado":
                messagebox.showwarning("Aviso", "Este turno fue rechazado")
            elif res == "cancelado":
                messagebox.showwarning(
                    "Aviso", "Este turno fue cancelado por el usuario"
                )
            elif res == "no_existe":
                messagebox.showerror("Error", "No existe un turno con ese ID")

    def rechazar():
        tid = simpledialog.askstring("Turno", "ID del turno:")
        if tid:
            res = rechazarTurno(int(tid))
            if res == "ok":
                messagebox.showinfo("OK", "Turno Rechazado")
            elif res == "ya_atendido":
                messagebox.showwarning("Aviso", "Este turno ya fue atendido")
            elif res == "rechazado":
                messagebox.showwarning("Aviso", "Este turno fue rechazado")
            elif res == "cancelado":
                messagebox.showwarning(
                    "Aviso", "Este turno fue cancelado por el usuario"
                )
            elif res == "no_existe":
                messagebox.showerror("Error", "No existe un turno con ese ID")

    def atender():
        tid = simpledialog.askstring("Turno", "ID del turno:")
        if tid:
            res = atenderTurno(int(tid))
            if res == "ok":
                messagebox.showinfo("OK", "Turno Atendido")
            elif res == "falta_aceptar":
                messagebox.showwarning("Aviso", "Primero debes aceptar el turno")
            elif res == "ya_atendido":
                messagebox.showwarning("Aviso", "Este turno ya fue atendido")
            elif res == "rechazado":
                messagebox.showwarning("Aviso", "Este turno fue rechazado")
            elif res == "cancelado":
                messagebox.showwarning(
                    "Aviso", "Este turno fue cancelado por el usuario"
                )
            elif res == "no_existe":
                messagebox.showerror("Error", "No existe un turno con ese ID")

    def enviar_Aviso():
        tid = simpledialog.askstring("Turno", "ID del turno:")
        if tid:
            turno = obtenerCorreo(int(tid))
        if turno:
            if turno["estado"] != "aceptado":
                messagebox.showwarning("Aviso", "Turno no a sido acepatado")
            else:
                enviarAviso(turno["email"], turno["nombre"])
                messagebox.showinfo("Aviso", "Correo Enviado al usuario")
        else:
            messagebox.showerror("Error", "Turno no econtrado")

    ttk.Button(
        frame,
        text="Consultar Turnos",
        style="BotonMediano.TButton",
        width=20,
        command=mostrarTurnos,
    ).grid(row=0, column=0, padx=20, pady=20)
    ttk.Button(
        frame,
        text="Aceptar Turno",
        style="BotonMediano.TButton",
        width=20,
        command=aceptar,
    ).grid(row=0, column=1, padx=20, pady=20)
    ttk.Button(
        frame,
        text="Rechazar Turno",
        style="BotonMediano.TButton",
        width=20,
        command=rechazar,
    ).grid(row=1, column=0, padx=20, pady=20)
    ttk.Button(
        frame,
        text="Atender Turno",
        style="BotonMediano.TButton",
        width=20,
        command=atender,
    ).grid(row=1, column=1, padx=20, pady=20)
    ttk.Button(
        frame,
        text="Enviar aviso",
        width=20,
        style="BotonMediano.TButton",
        command=enviar_Aviso,
    ).grid(row=2, column=0, padx=20, pady=20)
    ttk.Button(
        frame,
        text="Cerrar Sesión",
        style="BotonMediano.TButton",
        width=20,
        command=lambda: cambiarPantalla(inicio),
    ).grid(row=2, column=1, padx=20, pady=30)


# ------------------ MAIN ------------------


def app():
    global raiz, framePrincipal

    raiz = Tk()
    raiz.title("Clínica")
    raiz.attributes("-fullscreen", True)
    raiz.configure(bg="#d6eaf8")
    style = ttk.Style()
    style.configure("BotonGrande.TButton", font=("Arial", 30, "bold"), padding=10)
    style.configure("BotonMediano.TButton", font=("Arial", 20, "bold"), padding=10)
    framePrincipal = Frame(raiz, bg="#d6eaf8")
    framePrincipal.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Button(raiz, text="Salir", width=5, command=salir).pack(
        side="top", anchor="sw", pady=15, padx=15
    )

    frameTitulo = Frame(raiz, bg="#d6eaf8")
    frameTitulo.pack(side="top")

    Label(
        frameTitulo,
        text="Sistema de Turnos - Clínica",
        font=("Arial", 40, "bold"),
        bg="#d6eaf8",
    ).pack()

    cambiarPantalla(inicio)

    raiz.mainloop()
