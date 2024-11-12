import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
#warn: Si se quiere ver los comentarios dinamicamente, instale 'BetterComments' en Visual Studio Code
#warn 2: Si se quiere obtener la base de datos, abra este github:

class Conexion:
    def __init__(self):
        self.user = "root",
        self.password = ""
        self.database = "dbescolar"
        self.host = "localhost"
        self.conn = None
    def open(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database
            )
            return self.conn
        except Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            return None
    
    def close(self):
        if self.conn:
            self.conn.close()

class dbEscolar:
    def __init__(self):
        self.con = Conexion()

    #FUNC:-----------------------LOGIN-----------------------#

    def verifyUsers(self, usuarios_id, password):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM usuarios WHERE usuarios_id = %s AND password = %s"
            try:
                cursor.execute(sql, (usuarios_id, password))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {e}")
            finally:
                self.con.close()
        return None
    
    #FUNC:-----------------------HORARIO-----------------------#

    def saveHorario(self, horario):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO horarios (turno, hora) VALUES (%s, %s, %s)"
            datos = (horario['turno'], horario['hora'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Horario guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar horario: {e}")
            finally:
                self.con.close()

    def searchHorario(self, horario_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM horarios WHERE horario_id = %s"
            try:
                cursor.execute(sql, (horario_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar el horario: {e}")
            finally:
                self.con.close()
        return None
    
    def editHorario(self, horario):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = """UPDATE horarios 
                     SET turno = %s, hora = %s
                     WHERE horario_id = %s"""
            datos = (horario['turno'], horario['hora'], horario['horario_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Horario editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar horario: {e}")
            finally:
                self.con.close()

    def removeHorario(self, horario_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM horarios WHERE horario_id = %s"
            try:
                cursor.execute(sql, (horario_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Horario eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar el horario: {e}")
            finally:
                self.con.close()

#?-----------------------LOGIN WINDOW-----------------------#

class LoginWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Login - Escolar")
        self.geometry("400x300")

        ttk.Label(self, text="Codigo:").pack(pady=10)
        self.codEntry = ttk.Entry(self)
        self.codEntry.pack(pady=5)

        ttk.Label(self, text="Password:").pack(pady=10)
        self.passEntry = ttk.Entry(self, show="*")
        self.passEntry.pack(pady=5)

        self.logBtn = ttk.Button(self, text="Login", command=self.verfLogin)
        self.logBtn.pack(pady=20)

        self.cancelBtn = ttk.Button(self, text="Cancel", command=self.cancelLogin)

    def verfLogin(self):
        codigo = self.codEntry.get()
        password = self.passEntry.get()

        db = dbEscolar()
        cod = db.verifyUsers(codigo, password)

        if cod:
            nombre = cod[1]
            self.destroy()
            root.deiconify()
            app = Application(root, nombre)
        else:
            messagebox.showerror("Error", "Usuario y/o Contraseña incorrecto(s)")
    
    def cancelLogin(self):
        self.telEntry.delete(0, 'end')
        self.passEntry.delete(0, 'end')
    
#?-----------------------MAIN WINDOW-----------------------#

class Application(ttk.Frame):
    def __init__(self, mainWind, nombre):
        super().__init__(mainWind)
        mainWind.title("Control Escolar " + nombre)
        mainWind.geometry("850x500")

        self.notebook = ttk.Notebook(self)
     
        #?-----------------------USUARIOS-----------------------#
        
        pestanaUsuarios = ttk.Frame(self.notebook)
        pestanaUsuarios.grid_columnconfigure(0, weight=1)
        pestanaUsuarios.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaUsuarios, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdUsuarioBuscar = ttk.Entry(pestanaUsuarios, width=30)
        self.txIdUsuarioBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarUsuario = ttk.Button(pestanaUsuarios, text="Buscar")
        self.btnBuscarUsuario.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestanaUsuarios, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txNombreUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txNombreUsuario.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="A. Paterno:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txAPaternoUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txAPaternoUsuario.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="A. Materno:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.txAMaternoUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txAMaternoUsuario.grid(row=2, column=3, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.txEmailUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txEmailUsuario.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="Username:").grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.txUsernameUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txUsernameUsuario.grid(row=3, column=3, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="Password:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.txPassewordUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txPassewordUsuario.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="Perfil:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.comboPerfilUsuario = ttk.Combobox(pestanaUsuarios, values=["Seleccione", "Admin", "Rector", "Secretaria"], state='readonly')
        self.comboPerfilUsuario.set("Seleccione")
        self.comboPerfilUsuario.grid(row=5, column=1, padx=10, pady=5)

        self.btnNuevoUsuario = ttk.Button(pestanaUsuarios, text="Nuevo")
        self.btnNuevoUsuario.grid(row=7, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarUsuario = ttk.Button(pestanaUsuarios, text="Guardar")
        self.btnGuardarUsuario.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarUsuario = ttk.Button(pestanaUsuarios, text="Cancelar")
        self.btnCancelarUsuario.grid(row=7, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarUsuario = ttk.Button(pestanaUsuarios, text="Editar")
        self.btnEditarUsuario.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarUsuario = ttk.Button(pestanaUsuarios, text="Eliminar")
        self.btnEliminarUsuario.grid(row=7, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaUsuarios, text="Usuarios")

        #?-----------------------ALUMNOS-----------------------#

        pestanaAlumnos = ttk.Frame(self.notebook)
        pestanaAlumnos.grid_columnconfigure(0, weight=1)
        pestanaAlumnos.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaAlumnos, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
        self.txIdAlumnoBuscar = ttk.Entry(pestanaAlumnos, width=30)
        self.txIdAlumnoBuscar.grid(row=0, column=1, padx=5, pady=5)

        self.btnBuscarAlumno = ttk.Button(pestanaAlumnos, text="Buscar")
        self.btnBuscarAlumno.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(pestanaAlumnos, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.txNombreAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txNombreAlumno.grid(row=1, column=1, pady=5)

        ttk.Label(pestanaAlumnos, text="Estado:").grid(row=1, column=2, sticky="e")
        self.estadoComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", "Aguascalientes", "Baja California", "Baja California Sur",
                                                            "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", 
                                                            "Ciudad de México", "Durango", "Guanajuato", "Guerrero",
                                                            "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
                                                            "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
                                                            "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", 
                                                            "Zacatecas"], width=28)
        self.estadoComboAlumno.grid(row=1, column=3, pady=5)
        self.estadoComboAlumno.set("Seleccione")

        ttk.Label(pestanaAlumnos, text="A Paterno:").grid(row=2, column=0, sticky="e")
        self.txAPaternoAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txAPaternoAlumno.grid(row=2, column=1, pady=5)

        ttk.Label(pestanaAlumnos, text="Fecha Nac:").grid(row=2, column=2, sticky="e")
        self.txFechaAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txFechaAlumno.grid(row=2, column=3, pady=5)

        ttk.Label(pestanaAlumnos, text="A Materno:").grid(row=3, column=0, sticky="e")
        self.txAMaternoAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txAMaternoAlumno.grid(row=3, column=1, pady=5)

        ttk.Label(pestanaAlumnos, text="Carrera:").grid(row=3, column=2, sticky="e")
        self.carreraComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
        self.carreraComboAlumno.grid(row=3, column=3, pady=5)
        self.carreraComboAlumno.set("Seleccione")

        ttk.Label(pestanaAlumnos, text="Email:").grid(row=4, column=0, sticky="e")
        self.txEmailAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txEmailAlumno.grid(row=4, column=1, pady=5)

        ttk.Label(pestanaAlumnos, text="Materia:").grid(row=4, column=2, sticky="e")
        self.materiaComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", 
            "Física 1", "Programación Estructura", "Estructura de Datos", 
            "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
        self.materiaComboAlumno.grid(row=4, column=3, pady=5)
        self.materiaComboAlumno.set("Seleccione")

        self.btnAgregarMateriaAlumno = ttk.Button(pestanaAlumnos, text="Agregar")
        self.btnAgregarMateriaAlumno.grid(row=5, column=3, padx=5, pady=5)

        self.treeMateriaAlumno = ttk.Treeview(pestanaAlumnos, columns=("Nombre"), show="headings", height=6)
        self.treeMateriaAlumno.heading("Nombre", text="Nombre")
        self.treeMateriaAlumno.grid(row=6, column=3, pady=5)

        self.btnNuevoAlumno = ttk.Button(pestanaAlumnos, text="Nuevo")
        self.btnNuevoAlumno.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarAlumno = ttk.Button(pestanaAlumnos, text="Guardar")
        self.btnGuardarAlumno.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarAlumno = ttk.Button(pestanaAlumnos, text="Cancelar")
        self.btnCancelarAlumno.grid(row=8, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarAlumno = ttk.Button(pestanaAlumnos, text="Editar")
        self.btnEditarAlumno.grid(row=8, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarAlumno = ttk.Button(pestanaAlumnos, text="Eliminar")
        self.btnEliminarAlumno.grid(row=8, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaAlumnos, text="Alumnos")

        #?-----------------------MAESTROS-----------------------#

        pestanaMaestros = ttk.Frame(self.notebook)
        pestanaMaestros.grid_columnconfigure(0, weight=1)
        pestanaMaestros.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaMaestros, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
        self.txIdMaestroBuscar = ttk.Entry(pestanaMaestros, width=30)
        self.txIdMaestroBuscar.grid(row=0, column=1, padx=5, pady=5)

        self.btnBuscarMaestro = ttk.Button(pestanaMaestros, text="Buscar")
        self.btnBuscarMaestro.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(pestanaMaestros, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.txNombreMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txNombreMaestro.grid(row=1, column=1, pady=5)

        ttk.Label(pestanaMaestros, text="Grado de Estudios:").grid(row=1, column=2, sticky="e")
        self.txGradoEstudiosMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txGradoEstudiosMaestro.grid(row=1, column=3, pady=5)

        ttk.Label(pestanaMaestros, text="A Paterno:").grid(row=2, column=0, sticky="e")
        self.txAPaternoMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txAPaternoMaestro.grid(row=2, column=1, pady=5)

        ttk.Label(pestanaMaestros, text="Carrera:").grid(row=2, column=2, sticky="e")
        self.carreraComboMaestro = ttk.Combobox(pestanaMaestros, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
        self.carreraComboMaestro.grid(row=2, column=3, pady=5)
        self.carreraComboMaestro.set("Seleccione")

        ttk.Label(pestanaMaestros, text="A Materno:").grid(row=3, column=0, sticky="e")
        self.txAMaternoMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txAMaternoMaestro.grid(row=3, column=1, pady=5)

        ttk.Label(pestanaMaestros, text="Materia:").grid(row=3, column=2, sticky="e")
        self.materiaComboMaestro = ttk.Combobox(pestanaMaestros, values=[
            "Física 1", "Programación Estructura", "Estructura de Datos", 
            "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
        self.materiaComboMaestro.grid(row=3, column=3, pady=5)
        self.materiaComboMaestro.set("Seleccione")

        ttk.Label(pestanaMaestros, text="Email:").grid(row=4, column=0, sticky="e")
        self.txEmailMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txEmailMaestro.grid(row=4, column=1, pady=5)

        self.btnAgregarMateriaMaestro = ttk.Button(pestanaMaestros, text="Agregar")
        self.btnAgregarMateriaMaestro.grid(row=5, column=3, padx=5, pady=5)

        self.treeMateriaMaestro = ttk.Treeview(pestanaMaestros, columns=("Nombre"), show="headings", height=6)
        self.treeMateriaMaestro.heading("Nombre", text="Nombre")
        self.treeMateriaMaestro.grid(row=6, column=3, pady=5)

        self.btnNuevoMaestro = ttk.Button(pestanaMaestros, text="Nuevo")
        self.btnNuevoMaestro.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarMaestro = ttk.Button(pestanaMaestros, text="Guardar")
        self.btnGuardarMaestro.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarMaestro = ttk.Button(pestanaMaestros, text="Cancelar")
        self.btnCancelarMaestro.grid(row=8, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarMaestro = ttk.Button(pestanaMaestros, text="Editar")
        self.btnEditarMaestro.grid(row=8, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarMaestro = ttk.Button(pestanaMaestros, text="Eliminar")
        self.btnEliminarMaestro.grid(row=8, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaMaestros, text="Maestros")

        #?-----------------------MATERIAS-----------------------#

        pestanaMaterias = ttk.Frame(self.notebook)
        pestanaMaterias.grid_columnconfigure(0, weight=1)
        pestanaMaterias.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaMaterias, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIDMateriaBuscar = ttk.Entry(pestanaMaterias, width=30)
        self.txIDMateriaBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarMateria = ttk.Button(pestanaMaterias, text="Buscar")
        self.btnBuscarMateria.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestanaMaterias, text="Asignatura:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txAsignaturaMateria = ttk.Entry(pestanaMaterias, width=30)
        self.txAsignaturaMateria.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestanaMaterias, text="Creditos:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txCreditosMateria = ttk.Entry(pestanaMaterias, width=30)
        self.txCreditosMateria.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(pestanaMaterias, text="Carrera:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.carreraComboMateria = ttk.Combobox(pestanaMaterias, values=["Seleccione", "Ingeniería", "Licenciatura"], width=30)
        self.carreraComboMateria.grid(row=2, column=3, padx=10, pady=5)
        self.carreraComboMateria.set("Seleccione")

        ttk.Label(pestanaMaterias, text="Semestre:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.txSemestreMateria = ttk.Entry(pestanaMaterias, width=30)
        self.txSemestreMateria.grid(row=3, column=1, padx=10, pady=5)

        self.btnNuevoMateria = ttk.Button(pestanaMaterias, text="Nuevo")
        self.btnNuevoMateria.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarMateria = ttk.Button(pestanaMaterias, text="Guardar")
        self.btnGuardarMateria.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarMateria = ttk.Button(pestanaMaterias, text="Cancelar")
        self.btnCancelarMateria.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarMateria = ttk.Button(pestanaMaterias, text="Editar")
        self.btnEditarMateria.grid(row=5, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarMateria = ttk.Button(pestanaMaterias, text="Eliminar")
        self.btnEliminarMateria.grid(row=5, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaMaterias, text="Materias")

        #?-----------------------GRUPOS-----------------------#

        pestanaGrupos = ttk.Frame(self.notebook)
        pestanaGrupos.grid_columnconfigure(0, weight=1)
        pestanaGrupos.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaGrupos, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
        self.txIdGrupoBuscar = ttk.Entry(pestanaGrupos, width=30)
        self.txIdGrupoBuscar.grid(row=0, column=1, padx=5, pady=5)

        self.btnBuscarGrupo = ttk.Button(pestanaGrupos, text="Buscar")
        self.btnBuscarGrupo.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(pestanaGrupos, text="Nombre Grupo:").grid(row=1, column=0, sticky="e")
        self.txNombreGrupo = ttk.Entry(pestanaGrupos, width=30)
        self.txNombreGrupo.grid(row=1, column=1, pady=5)

        ttk.Label(pestanaGrupos, text="Fecha:").grid(row=1, column=2, sticky="e")
        self.txFechaGrupo = ttk.Entry(pestanaGrupos, width=30)
        self.txFechaGrupo.grid(row=1, column=3, pady=5)

        ttk.Label(pestanaGrupos, text="Salon:").grid(row=2, column=0, sticky="e")
        self.salonComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione","Salones"], width=28)
        self.salonComboGrupo.grid(row=2, column=1, pady=5)
        self.salonComboGrupo.set("Seleccione")

        ttk.Label(pestanaGrupos, text="Horario:").grid(row=2, column=2, sticky="e")
        self.horarioComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "Horario"], width=28)
        self.horarioComboGrupo.grid(row=2, column=3, pady=5)
        self.horarioComboGrupo.set("Seleccione")

        ttk.Label(pestanaGrupos, text="Semestre:").grid(row=3, column=0, sticky="e")
        self.txSemestreGrupo = ttk.Entry(pestanaGrupos, width=30)
        self.xSemestreGrupo.grid(row=3, column=1, pady=5)

        ttk.Label(pestanaGrupos, text="Carrera:").grid(row=3, column=2, sticky="e")
        self.carreraComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
        self.carreraComboGrupo.grid(row=3, column=3, pady=5)
        self.carreraComboGrupo.set("Seleccione")

        ttk.Label(pestanaGrupos, text="Maestros:").grid(row=4, column=0, sticky="e")
        self.maestrosComboGrupo = ttk.Combobox(pestanaGrupos, values=["Maestros"], width=28)
        self.maestrosComboGrupo.grid(row=4, column=1, pady=5)
        self.maestrosComboGrupo.set("Seleccione")

        ttk.Label(pestanaGrupos, text="Materia:").grid(row=4, column=2, sticky="e")
        self.materiaComboGrupo = ttk.Combobox(pestanaGrupos, values=[
            "Física 1", "Programación Estructura", "Estructura de Datos", 
            "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
        self.materiaComboGrupo.grid(row=4, column=3, pady=5)
        self.materiaComboGrupo.set("Seleccione")

        ttk.Label(pestanaGrupos, text="Alumnos Max.:").grid(row=5, column=0, sticky="e")
        self.maxAlumsComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "1", "2", "3"], width=28)
        self.maxAlumsComboGrupo.grid(row=5, column=1, pady=5)
        self.maxAlumsComboGrupo.set("Seleccione")

        self.btnNuevoCompra = ttk.Button(pestanaGrupos, text="Nuevo")
        self.btnNuevoCompra.grid(row=7, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarCompra = ttk.Button(pestanaGrupos, text="Guardar")
        self.btnGuardarCompra.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarCompra = ttk.Button(pestanaGrupos, text="Cancelar")
        self.btnCancelarCompra.grid(row=7, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarCompra = ttk.Button(pestanaGrupos, text="Editar")
        self.btnEditarCompra.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarCompra = ttk.Button(pestanaGrupos, text="Eliminar")
        self.btnEliminarCompra.grid(row=7, column=4, padx=10, pady=10, sticky="w")
                
        self.notebook.add(pestanaGrupos, text="Grupos")

        #?-----------------------HORARIO-----------------------#

        pestanaHorario = ttk.Frame(self.notebook)
        pestanaHorario.grid_columnconfigure(0, weight=1)
        pestanaHorario.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaHorario, text="Ingrese ID grupo:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdBuscarHorario = ttk.Entry(pestanaHorario, width=30)
        self.txIdBuscarHorario.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarHorario = ttk.Button(pestanaHorario, text="Buscar")
        self.btnBuscarHorario.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestanaHorario, text="Turno:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.comboTurnoHorario = ttk.Combobox(pestanaHorario, values=["Seleccione", "Matutino", "Vespertino"], width=28)
        self.comboTurnoHorario.set("Seleccione")
        self.comboTurnoHorario.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestanaHorario, text="Hora:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txHoraHorario = ttk.Entry(pestanaHorario, width=30)
        self.txHoraHorario.grid(row=2, column=1, padx=10, pady=5)

        self.btnNuevoHorario = ttk.Button(pestanaHorario, text="Nuevo")
        self.btnNuevoHorario.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarHorario = ttk.Button(pestanaHorario, text="Guardar")
        self.btnGuardarHorario.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarHorario = ttk.Button(pestanaHorario, text="Cancelar")
        self.btnCancelarHorario.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarHorario = ttk.Button(pestanaHorario, text="Editar")
        self.btnEditarHorario.grid(row=6, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarHorario = ttk.Button(pestanaHorario, text="Eliminar")
        self.btnEliminarHorario.grid(row=6, column=4, padx=10, pady=10, sticky="w")
                
        self.notebook.add(pestanaHorario, text="Horario")

        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.pack()

    #FUNCIONES PARA EL CRUD
    #FUNC:-----------------------HORARIO-----------------------#

    def limpiarCamposHorario(self):
        self.comboTurnoHorario.set("Seleccione")
        self.txHoraHorario.delete(0, 'end')
    
    def guardarHorario(self):
        if self.validarCamposHorario():
            horario = {
                'turno': self.comboTurnoHorario.get(),
                'hora': self.txHoraHorario.get()
            }
            db = dbEscolar()
            db.saveHorario(horario)
    
    def buscarHorario(self):
        horario_id = self.txIdBuscarHorario.get()
        if horario_id:
            db = dbEscolar()
            horario = db.searchHorario(horario_id)
            if horario:
                self.comboTurnoHorario.set(horario[1])
                self.txHoraHorario.delete(0, 'end')
                self.txHoraHorario.insert(0, horario[2])
            else:
                messagebox.showerror("Error", "Horario no encontrado")
    
    def editarHorario(self):
        if self.validarCamposHorario():
            horario = {
                'turno': self.comboTurnoHorario.get(),
                'hora': self.txHoraHorario.get()
            }
            db = dbEscolar()
            db.editHorario(horario)
    
    def eliminarHorario(self):
        horario_id = self.txIdBuscarHorario.get()
        if horario_id:
            db = dbEscolar()
            db.removeHorario(horario_id)
            self.limpiarCamposHorario()
        
    def validarCamposHorario(self):
        if self.comboTurnoHorario.get() == "Seleccione" or not self.txHoraHorario.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()
    login = LoginWindow(root)
    root.mainloop()