import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
#warn: Si se quiere ver los comentarios dinamicamente, instale 'BetterComments' en Visual Studio Code
#warn 2: Si se quiere obtener la base de datos, abra este github: https://github.com/AlanArenas197/interfazProyectoFinalIS

class Conexion:
    def __init__(self):
        self.user = "root"
        self.password = ""
        self.database = "dbescolar"
        self.host = "localhost"
        self.conn = None
    def open(self):
        if not self.conn or not self.conn.is_connected():
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
        return self.conn
    
    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None

class dbEscolar:
    def __init__(self):
        self.con = Conexion()

    def verifyUsers(self, email, password):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
            try:
                cursor.execute(sql, (email, password))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {e}")
            finally:
                self.con.close()
        return None

#!-----------------------USUARIO-----------------------#

class Usuarios:
    def __init__(self, conexion):
        self.con = conexion

    def email(self, email):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar el email.")
            return False

        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar email: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, usuario):
        conn = self.con.open()
        if conn:
            if self.email(usuario['email']):
                messagebox.showerror("Error", "El email ya está registrado.")
                return
            cursor = conn.cursor()
            sql = """INSERT INTO usuarios (nombre, apaterno, amaterno, email, username, password, perfil) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            datos = (usuario['nombre'], usuario['apaterno'], usuario['amaterno'], usuario['email'], 
                     usuario['username'], usuario['password'], usuario['perfil'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar usuario: {e}")
            finally:
                cursor.close()
                self.con.close()

    def search(self, usuarios_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM usuarios WHERE usuarios_id = %s"
            try:
                cursor.execute(sql, (usuarios_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar el usuario: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, usuario):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = """UPDATE usuarios 
                     SET nombre = %s, apaterno = %s, amaterno = %s, email = %s, username = %s, password = %s, perfil = %s
                     WHERE usuarios_id = %s"""
            datos = (usuario['nombre'], usuario['apaterno'], usuario['amaterno'], usuario['email'], usuario['username'], usuario['password'], usuario['perfil'], usuario['usuarios_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar usuario: {e}")
            finally:
                self.con.close()

    def remove(self, usuarios_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM usuarios WHERE usuarios_id = %s"
            try:
                cursor.execute(sql, (usuarios_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar el usuario: {e}")
            finally:
                self.con.close()

#!-----------------------ALUMNO-----------------------#

class Alumnos:
    def __init__(self, conexion):
        self.con = conexion

    def email(self, email):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar el email.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM alumnos WHERE email = %s"
            cursor.execute(sql, (email,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar email: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
    
    def verifyCupo(self, nombre):
        conn = self.con.open()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT max_alumnos, alum_reg FROM grupos WHERE nombre = %s"
                cursor.execute(sql, (nombre,))
                grupo = cursor.fetchone()
                if grupo:
                    max_alumnos, alum_reg = grupo
                    if int(alum_reg) < int(max_alumnos):
                        return True
                    else:
                        return False
                else:
                    messagebox.showerror("Error", "El grupo no existe.")
                    return False
            except Error as e:
                messagebox.showerror("Error", f"Error al verificar el cupo del grupo: {e}")
                return False
            finally:
                if conn.is_connected():
                    cursor.close()
        else:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")
            return False
    
    def updateGroups(self, nombre, incrementar=True):
        conn = self.con.open()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE grupos SET alum_reg = alum_reg + %s WHERE nombre = %s"
                cursor.execute(sql, (1 if incrementar else -1, nombre))
                conn.commit()
            except Error as e:
                messagebox.showerror("Error", f"Error al actualizar alumnos registrados: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()

    def save(self, alumno):
        conn = self.con.open()
        if conn:
            try:
                cursor = conn.cursor()
                grupo_id = alumno['grupo']
                if self.email(alumno['email']):
                    messagebox.showerror("Error", "El email ya está registrado.")
                    return
                if not self.verifyCupo(grupo_id):
                    messagebox.showerror("Error", "El grupo ya alcanzó el máximo de alumnos permitidos.")
                    return
                sql = """
                    INSERT INTO alumnos 
                    (nombre, apaterno, amaterno, email, estado, fecha_nac, carrera, materia, password, grupo) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                datos = (
                    alumno['nombre'], alumno['apaterno'], alumno['amaterno'], alumno['email'], 
                    alumno['estado'], alumno['fecha_nac'], alumno['carrera'], alumno['materia'], 
                    alumno['password'], grupo_id
                )
                cursor.execute(sql, datos)
                conn.commit()
                self.updateGroups(grupo_id, incrementar=True)
                messagebox.showinfo("Éxito", "Alumno guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar alumno: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()

    def search(self, alumnos_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM alumnos WHERE alumnos_id = %s"
            try:
                cursor.execute(sql, (alumnos_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar el alumno: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, alumno):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql_buscar = "SELECT grupo FROM alumnos WHERE alumnos_id = %s"
            cursor.execute(sql_buscar, (alumno['alumnos_id'],))
            grupo_actual = cursor.fetchone()
            if grupo_actual:
                grupo_actual = grupo_actual[0]
                grupo_nuevo = alumno['grupo']
                if grupo_actual != grupo_nuevo:
                    if not self.verifyCupo(grupo_nuevo):
                        messagebox.showerror("Error", "El grupo nuevo ya alcanzó el máximo de alumnos permitidos.")
                        return
                    self.updateGroups(grupo_actual, incrementar=False)
                    self.updateGroups(grupo_nuevo, incrementar=True)

            sql = """
                UPDATE alumnos SET nombre = %s, apaterno = %s, amaterno = %s, email = %s, 
                estado = %s, fecha_nac = %s, carrera = %s, materia = %s, password = %s, grupo = %s 
                WHERE alumnos_id = %s
            """
            datos = (
                alumno['nombre'], alumno['apaterno'], alumno['amaterno'], alumno['email'], 
                alumno['estado'], alumno['fecha_nac'], alumno['carrera'], alumno['materia'], 
                alumno['password'], grupo_nuevo, alumno['alumnos_id']
            )
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Alumno actualizado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al actualizar al alumno: {e}")
            finally:
                self.con.close()

    def remove(self, alumnos_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM alumnos WHERE alumnos_id = %s"
            try:
                cursor.execute(sql, (alumnos_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar el alumno: {e}")
            finally:
                self.con.close()

#!-----------------------MAESTRO-----------------------#

class Maestros:
    def __init__(self, conexion):
        self.con = conexion
    
    def email(self, email):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar el email.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM maestros WHERE email = %s"
            cursor.execute(sql, (email,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar email: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, maestro):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.email(maestro['email']):
                messagebox.showerror("Error", "El email ya está registrado.")
                return
            sql = "INSERT INTO maestros (nombre, apaterno, amaterno, email, carrera, materia, grado_estudios, grupo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (maestro['nombre'], maestro['apaterno'], maestro['amaterno'], maestro['email'], maestro['carrera'], maestro['materia'], maestro['grado_estudios'], maestro['grupo'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Maestro guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar maestro: {e}")
            finally:
                self.con.close()

    def search(self, maestro_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM maestros WHERE maestro_id = %s"
            try:
                cursor.execute(sql, (maestro_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar el maestro: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, maestro):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = """UPDATE maestros 
                     SET nombre = %s, apaterno = %s, amaterno = %s, email = %s, carrera = %s, materia = %s, grado_estudios = %s, grupo = %s
                     WHERE maestro_id = %s"""
            datos = (maestro['nombre'], maestro['apaterno'], maestro['amaterno'], maestro['email'], maestro['carrera'], maestro['materia'], maestro['grado_estudios'], maestro['grupo'], maestro['maestro_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Maestro editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar maestro: {e}")
            finally:
                self.con.close()

    def remove(self, maestro_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM maestros WHERE maestro_id = %s"
            try:
                cursor.execute(sql, (maestro_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Maestro eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar el maestro: {e}")
            finally:
                self.con.close()

#!-----------------------MATERIA-----------------------#

class Materias:
    def __init__(self, conexion):
        self.con = conexion

    def assigment(self, asignatura):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar la asignatura.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM materias WHERE asignatura = %s"
            cursor.execute(sql, (asignatura,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar la asignatura: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, materia):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.assigment(materia['asignatura']):
                messagebox.showerror("Error", "La asignatura ya está registrada.")
                return
            sql = "INSERT INTO materias (asignatura, creditos, semestre, carrera) VALUES (%s, %s, %s, %s)"
            datos = (materia['asignatura'], materia['creditos'], materia['semestre'], materia['carrera'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Materia guardada correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar materia: {e}")
            finally:
                self.con.close()

    def search(self, materias_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM materias WHERE materias_id = %s"
            try:
                cursor.execute(sql, (materias_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar la materia: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, materia):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = """UPDATE materias 
                     SET asignatura = %s, creditos = %s, semestre = %s, carrera = %s
                     WHERE materias_id = %s"""
            datos = (materia['asignatura'], materia['creditos'], materia['semestre'], materia['carrera'], materia['materias_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Materia editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar materia: {e}")
            finally:
                self.con.close()

    def remove(self, materias_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM materias WHERE materias_id = %s"
            try:
                cursor.execute(sql, (materias_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Materia eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar la materia: {e}")
            finally:
                self.con.close()

#!-----------------------GRUPOS-----------------------#

class Grupos:
    def __init__(self, conexion):
        self.con = conexion
    
    def availability(self, horario, salon, nombre):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar el grupo.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM grupos WHERE horario = %s AND salon = %s AND nombre = %s"
            cursor.execute(sql, (horario, salon, nombre,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar la disponibilidad: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, grupos):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.availability(grupos['horario'], grupos['salon'], grupos['nombre']):
                messagebox.showerror("Error", "El grupo ya está registrado.")
                return
            sql = "INSERT INTO grupos (nombre, fecha, carrera, materia, maestro, salon, horario, semestre, max_alumnos, alum_reg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            datos = (grupos['nombre'], grupos['fecha'], grupos['carrera'], grupos['materia'], grupos['maestro'], grupos['salon'], grupos['horario'], grupos['semestre'], grupos['max_alumnos'], grupos['alum_reg'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Grupo guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar grupo: {e}")
            finally:
                self.con.close()

    def search(self, grupo_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM grupos WHERE grupo_id = %s"
            try:
                cursor.execute(sql, (grupo_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar el grupo: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, grupos):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = """UPDATE grupos 
                     SET nombre = %s, fecha = %s, carrera = %s, materia = %s, maestro = %s, salon = %s, horario = %s, semestre = %s, max_alumnos = %s, alum_reg = %s
                     WHERE grupo_id = %s"""
            datos = (grupos['nombre'], grupos['fecha'], grupos['carrera'], grupos['materia'], grupos['maestro'], grupos['salon'], grupos['horario'], grupos['semestre'], grupos['max_alumnos'], grupos['alum_reg'], grupos['grupo_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Grupo editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar grupo: {e}")
            finally:
                self.con.close()

    def remove(self, grupo_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM grupos WHERE grupo_id = %s"
            try:
                cursor.execute(sql, (grupo_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Grupo eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar el grupo: {e}")
            finally:
                self.con.close()

#!-----------------------HORARIO-----------------------#

class Horarios:
    def __init__(self, conexion):
        self.con = conexion

    def availability(self, hora, turno):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar el horario.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM horarios WHERE hora = %s AND turno = %s"
            cursor.execute(sql, (hora, turno,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar la disponibilidad: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, horario):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.availability(horario['hora'], horario['turno']):
                messagebox.showerror("Error", "El horario ya está registrado.")
                return
            sql = "INSERT INTO horarios (turno, hora) VALUES (%s, %s)"
            datos = (horario['turno'], horario['hora'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Horario guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar horario: {e}")
            finally:
                self.con.close()

    def search(self, horario_id):
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

    def edit(self, horario):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.availability(horario['hora'], horario['turno']):
                messagebox.showerror("Error", "El horario ya está registrado.")
                return
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

    def remove(self, horario_id):
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

#!-----------------------SALONES-----------------------#

class Salones:
    def __init__(self, conexion):
        self.con = conexion

    def availability(self, nombre, edificio):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar el salon.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM salones WHERE nombre = %s AND edificio = %s"
            cursor.execute(sql, (nombre, edificio,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar la disponibilidad: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, salon):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.availability(salon['nombre'], salon['edificio']):
                messagebox.showerror("Error", "El salon ya está registrado.")
                return
            sql = "INSERT INTO salones (nombre, edificio) VALUES (%s, %s)"
            datos = (salon['nombre'], salon['edificio'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Salon guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar salon: {e}")
            finally:
                self.con.close()

    def search(self, salon_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM salones WHERE salon_id = %s"
            try:
                cursor.execute(sql, (salon_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar el salon: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, salon):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.availability(salon['nombre'], salon['edificio']):
                messagebox.showerror("Error", "El horario ya está registrado.")
                return
            sql = """UPDATE horarios 
                     SET nombre = %s, edificio = %s
                     WHERE salon_id = %s"""
            datos = (salon['nombre'], salon['edificio'], salon['salon_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Salon editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar salon: {e}")
            finally:
                self.con.close()

    def remove(self, salon_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM salones WHERE salon_id = %s"
            try:
                cursor.execute(sql, (salon_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Salon eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar el salon: {e}")
            finally:
                self.con.close()

#!-----------------------CARRERAS-----------------------#

class Carreras:
    def __init__(self, conexion):
        self.con = conexion

    def existence(self, nombre):
        conn = self.con.open()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos para verificar la carrera.")
            return False
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM carreras WHERE nombre = %s"
            cursor.execute(sql, (nombre,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            messagebox.showerror("Error", f"Error al verificar la disponibilidad: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()

    def save(self, carrera):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.existence(carrera['nombre']):
                messagebox.showerror("Error", "La carrera ya está registrada.")
                return
            sql = "INSERT INTO carreras (nombre, num_semestres) VALUES (%s, %s)"
            datos = (carrera['nombre'], carrera['num_semestres'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Carrera guardada correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar carrera: {e}")
            finally:
                self.con.close()

    def search(self, carrera_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM carreras WHERE carrera_id = %s"
            try:
                cursor.execute(sql, (carrera_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar la carrera: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, carrera):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            if self.existence(carrera['nombre'], carrera['edificio']):
                messagebox.showerror("Error", "La carrera ya está registrada.")
                return
            sql = """UPDATE carreras 
                     SET nombre = %s, num_semestres = %s
                     WHERE carrera_id = %s"""
            datos = (carrera['nombre'], carrera['num_semestres'], carrera['carrera_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Carrera editada correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar carrera: {e}")
            finally:
                self.con.close()

    def remove(self, carrera_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM carreras WHERE carrera_id = %s"
            try:
                cursor.execute(sql, (carrera_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Carrera eliminada correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar la carrera: {e}")
            finally:
                self.con.close()

#!-----------------------PLANEACIÓN-----------------------#

class Planeacion:
    def __init__(self, conexion):
        self.con = conexion

    def groups(self):
        conn = self.con.open()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, salon, materia, maestro, horario FROM grupos ORDER BY horario")
        planHorario = cursor.fetchall()
        conn.close()
        return planHorario


#?-----------------------LOGIN WINDOW-----------------------#

class LoginWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Login - Escolar")
        self.geometry("400x300")

        ttk.Label(self, text="Email:").pack(pady=10)
        self.codEntry = ttk.Entry(self, width=30)
        self.codEntry.pack(pady=5)

        ttk.Label(self, text="Password:").pack(pady=10)
        self.passEntry = ttk.Entry(self, show="*")
        self.passEntry.pack(pady=5)

        self.logBtn = ttk.Button(self, text="Login", command=self.verfLogin)
        self.logBtn.pack(pady=20)

        self.cancelBtn = ttk.Button(self, text="Cancel", command=self.cancelLogin)

    def verfLogin(self):
        email = self.codEntry.get()
        password = self.passEntry.get()

        db = dbEscolar()
        cod = db.verifyUsers(email, password)

        if cod:
            nombre = cod[1]
            self.destroy()
            root.deiconify()
            app = Application(root, nombre, db.con)
        else:
            messagebox.showerror("Error", "Usuario y/o Contraseña incorrecto(s)")
    
    def cancelLogin(self):
        self.codEntry.delete(0, 'end')
        self.passEntry.delete(0, 'end')
    
#?-----------------------MAIN WINDOW-----------------------#

class Application(ttk.Frame):
    def __init__(self, mainWind, nombre, conexion):
        super().__init__(mainWind)
        mainWind.title("Control Escolar - " + nombre)
        mainWind.geometry("850x500")
        
        self.usuarios = Usuarios(conexion)
        self.alumnos = Alumnos(conexion)
        self.maestros = Maestros(conexion)
        self.materias = Materias(conexion)
        self.grupos = Grupos(conexion)
        self.horarios = Horarios(conexion)
        self.salones = Salones(conexion)
        self.carreras = Carreras(conexion)
        self.planeacion = Planeacion(conexion)

        self.notebook = ttk.Notebook(self)
     
        #?-----------------------USUARIOS-----------------------#
        
        pestanaUsuarios = ttk.Frame(self.notebook)
        pestanaUsuarios.grid_columnconfigure(0, weight=1)
        pestanaUsuarios.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaUsuarios, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdUsuarioBuscar = ttk.Entry(pestanaUsuarios, width=30)
        self.txIdUsuarioBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarUsuario = ttk.Button(pestanaUsuarios, text="Buscar", command=self.buscarUsuario)
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
        self.txPasswordUsuario = ttk.Entry(pestanaUsuarios, width=30)
        self.txPasswordUsuario.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(pestanaUsuarios, text="Perfil:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.comboPerfilUsuario = ttk.Combobox(pestanaUsuarios, values=["Seleccione", "Admin", "Rector", "Secretaria"], state='readonly')
        self.comboPerfilUsuario.set("Seleccione")
        self.comboPerfilUsuario.grid(row=5, column=1, padx=10, pady=5)

        self.btnNuevoUsuario = ttk.Button(pestanaUsuarios, text="Nuevo", command=self.limpiarCamposUsuario)
        self.btnNuevoUsuario.grid(row=7, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarUsuario = ttk.Button(pestanaUsuarios, text="Guardar", command = self.guardarUsuario)
        self.btnGuardarUsuario.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarUsuario = ttk.Button(pestanaUsuarios, text="Cancelar", command=self.limpiarCamposUsuario)
        self.btnCancelarUsuario.grid(row=7, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarUsuario = ttk.Button(pestanaUsuarios, text="Editar", command=self.editarUsuario)
        self.btnEditarUsuario.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarUsuario = ttk.Button(pestanaUsuarios, text="Eliminar", command=self.eliminarUsuario)
        self.btnEliminarUsuario.grid(row=7, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaUsuarios, text="Usuarios")

        #?-----------------------ALUMNOS-----------------------#

        pestanaAlumnos = ttk.Frame(self.notebook)
        pestanaAlumnos.grid_columnconfigure(0, weight=1)
        pestanaAlumnos.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaAlumnos, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
        self.txIdAlumnoBuscar = ttk.Entry(pestanaAlumnos, width=30)
        self.txIdAlumnoBuscar.grid(row=0, column=1, padx=5, pady=5)

        self.btnBuscarAlumno = ttk.Button(pestanaAlumnos, text="Buscar", command=self.buscarAlumno)
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
        self.cargarCarreraAlumno()
        self.carreraComboAlumno.bind("<<ComboboxSelected>>", self.actualizarCarreraAlumno)

        ttk.Label(pestanaAlumnos, text="Email:").grid(row=4, column=0, sticky="e")
        self.txEmailAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txEmailAlumno.grid(row=4, column=1, pady=5)

        ttk.Label(pestanaAlumnos, text="Materia:").grid(row=4, column=2, sticky="e")
        self.materiaComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", 
            "Física 1", "Programación Estructura", "Estructura de Datos", 
            "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
        self.materiaComboAlumno.grid(row=4, column=3, pady=5)
        self.materiaComboAlumno.set("Seleccione")
        self.cargarMateriasAlumno()
        self.materiaComboAlumno.bind("<<ComboboxSelected>>", self.actualizarMateriasAlumno)

        ttk.Label(pestanaAlumnos, text="Contraseña:").grid(row=5, column=0, sticky="e")
        self.txPasswordAlumno = ttk.Entry(pestanaAlumnos, width=30)
        self.txPasswordAlumno.grid(row=5, column=1, pady=5)

        ttk.Label(pestanaAlumnos, text="Grupo:").grid(row=6, column=0, sticky="e")
        self.grupoComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", "<GRUPOS>"], width=28)
        self.grupoComboAlumno.grid(row=6, column=1, pady=5)
        self.grupoComboAlumno.set("Seleccione")
        self.cargarGrupoAlumno()
        self.grupoComboAlumno.bind("<<ComboboxSelected>>", self.actualizaGruposAlumno)

        self.btnAgregarMateriaAlumno = ttk.Button(pestanaAlumnos, text="Agregar", command=self.agregarMateriaAlumno)
        self.btnAgregarMateriaAlumno.grid(row=5, column=3, padx=5, pady=5)

        self.treeMateriaAlumno = ttk.Treeview(pestanaAlumnos, columns=("Nombre"), show="headings", height=6)
        self.treeMateriaAlumno.heading("Nombre", text="Nombre")
        self.treeMateriaAlumno.grid(row=6, column=3, pady=5)

        self.btnNuevoAlumno = ttk.Button(pestanaAlumnos, text="Nuevo", command=self.limpiarCamposAlumno)
        self.btnNuevoAlumno.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarAlumno = ttk.Button(pestanaAlumnos, text="Guardar", command=self.guardarAlumno)
        self.btnGuardarAlumno.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarAlumno = ttk.Button(pestanaAlumnos, text="Cancelar", command=self.limpiarCamposAlumno)
        self.btnCancelarAlumno.grid(row=8, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarAlumno = ttk.Button(pestanaAlumnos, text="Editar", command=self.editarAlumno)
        self.btnEditarAlumno.grid(row=8, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarAlumno = ttk.Button(pestanaAlumnos, text="Eliminar", command=self.eliminarAlumno)
        self.btnEliminarAlumno.grid(row=8, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaAlumnos, text="Alumnos")

        #?-----------------------MAESTROS-----------------------#

        pestanaMaestros = ttk.Frame(self.notebook)
        pestanaMaestros.grid_columnconfigure(0, weight=1)
        pestanaMaestros.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaMaestros, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
        self.txIdMaestroBuscar = ttk.Entry(pestanaMaestros, width=30)
        self.txIdMaestroBuscar.grid(row=0, column=1, padx=5, pady=5)

        self.btnBuscarMaestro = ttk.Button(pestanaMaestros, text="Buscar", command=self.buscarMaestro)
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
        self.cargarCarreraProfe()
        self.carreraComboMaestro.bind("<<ComboboxSelected>>", self.actualizarCarreraProfe)

        ttk.Label(pestanaMaestros, text="A Materno:").grid(row=3, column=0, sticky="e")
        self.txAMaternoMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txAMaternoMaestro.grid(row=3, column=1, pady=5)

        ttk.Label(pestanaMaestros, text="Materia:").grid(row=3, column=2, sticky="e")
        self.materiaComboMaestro = ttk.Combobox(pestanaMaestros, values=[
            "Física 1", "Programación Estructura", "Estructura de Datos", 
            "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
        self.materiaComboMaestro.grid(row=3, column=3, pady=5)
        self.materiaComboMaestro.set("Seleccione")
        self.cargarMateriasMaestro()
        self.materiaComboMaestro.bind("<<ComboboxSelected>>", self.actualizarMateriasMaestro)

        ttk.Label(pestanaMaestros, text="Email:").grid(row=4, column=0, sticky="e")
        self.txEmailMaestro = ttk.Entry(pestanaMaestros, width=30)
        self.txEmailMaestro.grid(row=4, column=1, pady=5)

        ttk.Label(pestanaMaestros, text="Grupo:").grid(row=5, column=0, sticky="e")
        self.grupoComboMaestro = ttk.Combobox(pestanaMaestros, values=["Seleccione", "<GRUPOS>"], width=28)
        self.grupoComboMaestro.grid(row=5, column=1, pady=5)
        self.grupoComboMaestro.set("Seleccione")
        self.cargarGrupoMaestro()
        self.grupoComboMaestro.bind("<<ComboboxSelected>>", self.actualizaGruposMaestro)

        self.btnAgregarMateriaMaestro = ttk.Button(pestanaMaestros, text="Agregar", command=self.agregarMateriaMaestro)
        self.btnAgregarMateriaMaestro.grid(row=5, column=3, padx=5, pady=5)

        self.treeMateriaMaestro = ttk.Treeview(pestanaMaestros, columns=("Nombre"), show="headings", height=6)
        self.treeMateriaMaestro.heading("Nombre", text="Nombre")
        self.treeMateriaMaestro.grid(row=6, column=3, pady=5)

        self.btnNuevoMaestro = ttk.Button(pestanaMaestros, text="Nuevo", command=self.limpiarCamposMaestro)
        self.btnNuevoMaestro.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarMaestro = ttk.Button(pestanaMaestros, text="Guardar", command=self.guardarMaestro)
        self.btnGuardarMaestro.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarMaestro = ttk.Button(pestanaMaestros, text="Cancelar", command=self.limpiarCamposMaestro)
        self.btnCancelarMaestro.grid(row=8, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarMaestro = ttk.Button(pestanaMaestros, text="Editar", command=self.editarMaestro)
        self.btnEditarMaestro.grid(row=8, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarMaestro = ttk.Button(pestanaMaestros, text="Eliminar", command=self.eliminarMaestro)
        self.btnEliminarMaestro.grid(row=8, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaMaestros, text="Maestros")

        #?-----------------------MATERIAS-----------------------#

        pestanaMaterias = ttk.Frame(self.notebook)
        pestanaMaterias.grid_columnconfigure(0, weight=1)
        pestanaMaterias.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaMaterias, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIDMateriaBuscar = ttk.Entry(pestanaMaterias, width=30)
        self.txIDMateriaBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarMateria = ttk.Button(pestanaMaterias, text="Buscar", command=self.buscarMateria)
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
        self.cargarCarreraMateria()
        self.carreraComboMateria.bind("<<ComboboxSelected>>", self.actualizarCarreraMateria)

        ttk.Label(pestanaMaterias, text="Semestre:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.txSemestreMateria = ttk.Entry(pestanaMaterias, width=30)
        self.txSemestreMateria.grid(row=3, column=1, padx=10, pady=5)

        self.btnNuevoMateria = ttk.Button(pestanaMaterias, text="Nuevo", command=self.limpiarCamposMateria)
        self.btnNuevoMateria.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarMateria = ttk.Button(pestanaMaterias, text="Guardar", command=self.guardarMateria)
        self.btnGuardarMateria.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarMateria = ttk.Button(pestanaMaterias, text="Cancelar", command=self.limpiarCamposMateria)
        self.btnCancelarMateria.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarMateria = ttk.Button(pestanaMaterias, text="Editar", command=self.editarMateria)
        self.btnEditarMateria.grid(row=5, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarMateria = ttk.Button(pestanaMaterias, text="Eliminar", command=self.eliminarMateria)
        self.btnEliminarMateria.grid(row=5, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestanaMaterias, text="Materias")

        #?-----------------------GRUPOS-----------------------#

        pestanaGrupos = ttk.Frame(self.notebook)
        pestanaGrupos.grid_columnconfigure(0, weight=1)
        pestanaGrupos.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaGrupos, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
        self.txIdGrupoBuscar = ttk.Entry(pestanaGrupos, width=30)
        self.txIdGrupoBuscar.grid(row=0, column=1, padx=5, pady=5)

        self.btnBuscarGrupo = ttk.Button(pestanaGrupos, text="Buscar", command=self.buscarGrupo)
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
        self.cargarSalones()
        self.salonComboGrupo.bind("<<ComboboxSelected>>", self.actualizarSalonesGrupo)

        ttk.Label(pestanaGrupos, text="Horario:").grid(row=2, column=2, sticky="e")
        self.horarioComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "Horario"], width=28)
        self.horarioComboGrupo.grid(row=2, column=3, pady=5)
        self.horarioComboGrupo.set("Seleccione")
        self.cargarHorario()
        self.horarioComboGrupo.bind("<<ComboboxSelected>>", self.actualizarHorarioGrupo)

        ttk.Label(pestanaGrupos, text="Semestre:").grid(row=3, column=0, sticky="e")
        self.txSemestreGrupo = ttk.Entry(pestanaGrupos, width=30)
        self.txSemestreGrupo.grid(row=3, column=1, pady=5)

        ttk.Label(pestanaGrupos, text="Carrera:").grid(row=3, column=2, sticky="e")
        self.carreraComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
        self.carreraComboGrupo.grid(row=3, column=3, pady=5)
        self.carreraComboGrupo.set("Seleccione")
        self.cargarCarreraGrupo()
        self.carreraComboGrupo.bind("<<ComboboxSelected>>", self.actualizarCarreraGrupo)

        ttk.Label(pestanaGrupos, text="Maestros:").grid(row=4, column=0, sticky="e")
        self.maestrosComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione"], width=28)
        self.maestrosComboGrupo.grid(row=4, column=1, pady=5)
        self.maestrosComboGrupo.set("Seleccione")
        self.cargarMaestros()
        self.maestrosComboGrupo.bind("<<ComboboxSelected>>", self.actualizarMaestroGrupo)

        ttk.Label(pestanaGrupos, text="Materia:").grid(row=4, column=2, sticky="e")
        self.materiaComboGrupo = ttk.Combobox(pestanaGrupos, values=[
            "Física 1", "Programación Estructura", "Estructura de Datos", 
            "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
        self.materiaComboGrupo.grid(row=4, column=3, pady=5)
        self.materiaComboGrupo.set("Seleccione")
        self.cargarMateriasGrupo()
        self.materiaComboGrupo.bind("<<ComboboxSelected>>", self.actualizarHorarioGrupo)

        ttk.Label(pestanaGrupos, text="Alumnos Max.:").grid(row=5, column=0, sticky="e")
        self.maxAlumsComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "1", "2", "3"], width=28)
        self.maxAlumsComboGrupo.grid(row=5, column=1, pady=5)
        self.maxAlumsComboGrupo.set("Seleccione")

        ttk.Label(pestanaGrupos, text="Alumnos Reg.:").grid(row=5, column=2, sticky="e")
        self.txAlumnosReg = ttk.Entry(pestanaGrupos, width=30)
        self.txAlumnosReg.grid(row=5, column=3, pady=5)

        """self.btnAgregarMateriaGrupo = ttk.Button(pestanaGrupos, text="Agregar", command=self.agregarMateriaGrupo)
        self.btnAgregarMateriaGrupo.grid(row= 5, column= 3, pady=5)

        self.treeMateriaGrupo = ttk.Treeview(pestanaGrupos, columns=("Nombre"), show="headings", height=6)
        self.treeMateriaGrupo.heading("Nombre", text="Nombre")
        self.treeMateriaGrupo.grid(row=6, column=3, pady=5)"""

        self.btnNuevoGrupo = ttk.Button(pestanaGrupos, text="Nuevo", command=self.limpiarCamposGrupo)
        self.btnNuevoGrupo.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarGrupo = ttk.Button(pestanaGrupos, text="Guardar", command=self.guardarGrupo)
        self.btnGuardarGrupo.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarGrupo = ttk.Button(pestanaGrupos, text="Cancelar", command=self.limpiarCamposGrupo)
        self.btnCancelarGrupo.grid(row=8, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarGrupo = ttk.Button(pestanaGrupos, text="Editar", command=self.editarGrupo)
        self.btnEditarGrupo.grid(row=8, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarGrupo = ttk.Button(pestanaGrupos, text="Eliminar", command=self.eliminarGrupo)
        self.btnEliminarGrupo.grid(row=8, column=4, padx=10, pady=10, sticky="w")
                
        self.notebook.add(pestanaGrupos, text="Grupos")

        #?-----------------------HORARIO-----------------------#

        pestanaHorario = ttk.Frame(self.notebook)
        pestanaHorario.grid_columnconfigure(0, weight=1)
        pestanaHorario.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaHorario, text="Ingrese ID grupo:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdBuscarHorario = ttk.Entry(pestanaHorario, width=30)
        self.txIdBuscarHorario.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarHorario = ttk.Button(pestanaHorario, text="Buscar", command=self.buscarHorario)
        self.btnBuscarHorario.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestanaHorario, text="Turno:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.comboTurnoHorario = ttk.Combobox(pestanaHorario, values=["Seleccione", "Matutino", "Vespertino"], width=28)
        self.comboTurnoHorario.set("Seleccione")
        self.comboTurnoHorario.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestanaHorario, text="Hora:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txHoraHorario = ttk.Entry(pestanaHorario, width=30)
        self.txHoraHorario.grid(row=2, column=1, padx=10, pady=5)

        self.btnNuevoHorario = ttk.Button(pestanaHorario, text="Nuevo", command=self.limpiarCamposHorario)
        self.btnNuevoHorario.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarHorario = ttk.Button(pestanaHorario, text="Guardar", command=self.guardarHorario)
        self.btnGuardarHorario.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarHorario = ttk.Button(pestanaHorario, text="Cancelar", command=self.limpiarCamposHorario)
        self.btnCancelarHorario.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarHorario = ttk.Button(pestanaHorario, text="Editar", command=self.editarHorario)
        self.btnEditarHorario.grid(row=6, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarHorario = ttk.Button(pestanaHorario, text="Eliminar", command=self.eliminarHorario)
        self.btnEliminarHorario.grid(row=6, column=4, padx=10, pady=10, sticky="w")
                
        self.notebook.add(pestanaHorario, text="Horario")

        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.pack()

        #?-----------------------SALONES-----------------------#

        pestanaSalon = ttk.Frame(self.notebook)
        pestanaSalon.grid_columnconfigure(0, weight=1)
        pestanaSalon.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaSalon, text="Ingrese ID salon:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdBuscarSalon = ttk.Entry(pestanaSalon, width=30)
        self.txIdBuscarSalon.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarSalon = ttk.Button(pestanaSalon, text="Buscar", command=self.buscarSalon)
        self.btnBuscarSalon.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestanaSalon, text="Edificio:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.comboEdificioSalon = ttk.Combobox(pestanaSalon, values=["Seleccione", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                                                                    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], width=28)
        self.comboEdificioSalon.set("Seleccione")
        self.comboEdificioSalon.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestanaSalon, text="Aula:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txAula = ttk.Entry(pestanaSalon, width=30)
        self.txAula.grid(row=2, column=1, padx=10, pady=5)

        self.btnNuevoSalon = ttk.Button(pestanaSalon, text="Nuevo", command=self.limpiarCamposSalon)
        self.btnNuevoSalon.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarSalon = ttk.Button(pestanaSalon, text="Guardar", command=self.guardarSalon)
        self.btnGuardarSalon.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarSalon = ttk.Button(pestanaSalon, text="Cancelar", command=self.limpiarCamposSalon)
        self.btnCancelarSalon.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarSalon = ttk.Button(pestanaSalon, text="Editar", command=self.editarSalon)
        self.btnEditarSalon.grid(row=6, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarSalon = ttk.Button(pestanaSalon, text="Eliminar", command=self.eliminarSalon)
        self.btnEliminarSalon.grid(row=6, column=4, padx=10, pady=10, sticky="w")
                
        self.notebook.add(pestanaSalon, text="Salon")

        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.pack()

        #?-----------------------CARRERAS-----------------------#

        pestanaCarrera = ttk.Frame(self.notebook)
        pestanaCarrera.grid_columnconfigure(0, weight=1)
        pestanaCarrera.grid_columnconfigure(1, weight=1)

        ttk.Label(pestanaCarrera, text="Ingrese ID carrera:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdBuscarCarrera = ttk.Entry(pestanaCarrera, width=30)
        self.txIdBuscarCarrera.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscarCarrera = ttk.Button(pestanaCarrera, text="Buscar", command=self.buscarCarrera)
        self.btnBuscarCarrera.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestanaCarrera, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txNombreCarrera = ttk.Entry(pestanaCarrera, width=30)
        self.txNombreCarrera.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestanaCarrera, text="Num. Semestres:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.comboNumSemestres = ttk.Combobox(pestanaCarrera, values=["Seleccione", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], width=28)
        self.comboNumSemestres.set("Seleccione")
        self.comboNumSemestres.grid(row=2, column=1, padx=10, pady=5)

        self.btnNuevaCarrera = ttk.Button(pestanaCarrera, text="Nuevo", command=self.limpiarCamposCarrera)
        self.btnNuevaCarrera.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardarCarrera = ttk.Button(pestanaCarrera, text="Guardar", command=self.guardarCarrera)
        self.btnGuardarCarrera.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelarCarrera = ttk.Button(pestanaCarrera, text="Cancelar", command=self.limpiarCamposCarrera)
        self.btnCancelarCarrera.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        self.btnEditarCarrera = ttk.Button(pestanaCarrera, text="Editar", command=self.editarCarrera)
        self.btnEditarCarrera.grid(row=6, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminarCarrera = ttk.Button(pestanaCarrera, text="Eliminar", command=self.eliminarCarrera)
        self.btnEliminarCarrera.grid(row=6, column=4, padx=10, pady=10, sticky="w")
                
        self.notebook.add(pestanaCarrera, text="Carrera")

        #?-----------------------PLANEACIÓN DE HORARIOS-----------------------#

        pestanaPlaneacion = ttk.Frame(self.notebook)
        pestanaPlaneacion.grid_columnconfigure(0, weight=1)
        pestanaPlaneacion.grid_columnconfigure(1, weight=1)

        self.btnActualizar = ttk.Button(pestanaPlaneacion, text="Actualizar", command=self.actualizarDatosPlan)
        self.btnActualizar.pack(pady=10)

        self.treePlaneacion = ttk.Treeview(pestanaPlaneacion, columns=("nombre", "salon", "materia", "maestro", "horario"), show="headings")
        self.treePlaneacion.column("nombre", width=50)
        self.treePlaneacion.heading("nombre", text="Nombre")

        self.treePlaneacion.column("salon", width=50)
        self.treePlaneacion.heading("salon", text="Salón")

        self.treePlaneacion.column("materia", width=50)
        self.treePlaneacion.heading("materia", text="Materia")

        self.treePlaneacion.column("maestro", width=50)
        self.treePlaneacion.heading("maestro", text="Maestro")

        self.treePlaneacion.column("horario", width=50)
        self.treePlaneacion.heading("horario", text="Horario")

        self.treePlaneacion.pack(fill=tk.BOTH, expand=True)
    
        self.notebook.add(pestanaPlaneacion, text="Planeación")

        #?-----------------------CONFIG DEL NOTEBOOK-----------------------#

        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.pack()

    #FUNCIONES PARA EL CRUD
    #FUNC:-----------------------USUARIOS-----------------------#

    def limpiarCamposUsuario(self):
        self.txNombreUsuario.delete(0, 'end')
        self.txAPaternoUsuario.delete(0, 'end')
        self.txAMaternoUsuario.delete(0, 'end')
        self.txEmailUsuario.delete(0, 'end')
        self.txUsernameUsuario.delete(0, 'end')
        self.txPasswordUsuario.delete(0, 'end')
        self.comboPerfilUsuario.set("Seleccione")
    
    def guardarUsuario(self):
        if self.validarCamposUsuario():
            usuario = {
                'nombre': self.txNombreUsuario.get(),
                'apaterno': self.txAPaternoUsuario.get(),
                'amaterno': self.txAMaternoUsuario.get(),
                'email': self.txEmailUsuario.get(),
                'username': self.txUsernameUsuario.get(),
                'password': self.txPasswordUsuario.get(),
                'perfil': self.comboPerfilUsuario.get()
            }
            self.usuarios.save(usuario)
    
    def buscarUsuario(self):
        usuarios_id = self.txIdUsuarioBuscar.get()
        if usuarios_id:
            usuario = self.usuarios.search(usuarios_id)
            if usuario:
                self.limpiarCamposUsuario()
                self.txNombreUsuario.insert(0, usuario[1])
                self.txAPaternoUsuario.insert(0, usuario[2])
                self.txAMaternoUsuario.insert(0, usuario[3])
                self.txEmailUsuario.insert(0, usuario[4])
                self.txUsernameUsuario.insert(0, usuario[5])
                self.txPasswordUsuario.insert(0, usuario[6])
                self.comboPerfilUsuario.set(usuario[7])
            else:
                messagebox.showerror("Error", "Usuario no encontrado")
    
    def editarUsuario(self):
        if self.validarCamposUsuario():
            usuario = {
                'usuarios_id': self.txIdUsuarioBuscar.get(),
                'nombre': self.txNombreUsuario.get(),
                'apaterno': self.txAPaternoUsuario.get(),
                'amaterno': self.txAMaternoUsuario.get(),
                'email': self.txEmailUsuario.get(),
                'username': self.txUsernameUsuario.get(),
                'password': self.txPasswordUsuario.get(),
                'perfil': self.comboPerfilUsuario.get()
            }
            self.usuarios.edit(usuario)
    
    def eliminarUsuario(self):
        usuarios_id = self.txIdUsuarioBuscar.get()
        if usuarios_id:
            self.usuarios.remove(usuarios_id)
            self.limpiarCamposUsuario()
        
    def validarCamposUsuario(self):
        if self.comboPerfilUsuario.get() == "Seleccione" or not self.txNombreUsuario.get() or not self.txAPaternoUsuario.get() or not self.txAMaternoUsuario.get() or not self.txEmailUsuario.get()\
            or not self.txUsernameUsuario.get() or not self.txPasswordUsuario.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True

    #FUNC:-----------------------ALUMNOS-----------------------#

    def limpiarCamposAlumno(self):
        self.txNombreAlumno.delete(0, 'end')
        self.txAPaternoAlumno.delete(0, 'end')
        self.txAMaternoAlumno.delete(0, 'end')
        self.txEmailAlumno.delete(0, 'end')
        self.estadoComboAlumno.set("Seleccione")
        self.txFechaAlumno.delete(0, 'end')
        self.carreraComboAlumno.set("Seleccione")
        self.materiaComboAlumno.set("Seleccione")
        self.txPasswordAlumno.delete(0, 'end')
        self.grupoComboAlumno.set("Seleccione")
        self.treeMateriaAlumno.delete(*self.treeMateriaAlumno.get_children())
    
    def guardarAlumno(self):
        if self.validarCamposAlumno():
            materias = [self.treeMateriaAlumno.item(item, 'values')[0] for item in self.treeMateriaAlumno.get_children()]
            if not materias:
                messagebox.showerror("Error", "Debe agregar al menos una materia.")
                return
            materias_str = ', '.join(materias)
            alumno = {
                'nombre': self.txNombreAlumno.get(),
                'apaterno': self.txAPaternoAlumno.get(),
                'amaterno': self.txAMaternoAlumno.get(),
                'email': self.txEmailAlumno.get(),
                'estado': self.estadoComboAlumno.get(),
                'fecha_nac': self.txFechaAlumno.get(),
                'carrera': self.carreraComboAlumno.get(),
                'materia': materias_str,
                'password': self.txPasswordAlumno.get(),
                'grupo': self.grupoComboAlumno.get()
            }

            self.alumnos.save(alumno)
            messagebox.showinfo("Éxito", "Alumno guardado correctamente")

    def buscarAlumno(self):
        alumnos_id = self.txIdAlumnoBuscar.get()
        if alumnos_id:
            alumno = self.alumnos.search(alumnos_id)
            if alumno:
                self.limpiarCamposAlumno()
                self.txNombreAlumno.insert(0, alumno[1])
                self.txAPaternoAlumno.insert(0, alumno[2])
                self.txAMaternoAlumno.insert(0, alumno[3])
                self.txEmailAlumno.insert(0, alumno[4])
                self.estadoComboAlumno.set(alumno[5])
                self.txFechaAlumno.insert(0, alumno[6])
                self.carreraComboAlumno.set(alumno[7])
                materias = alumno[8].split(', ') if alumno[8] else []
                for materia in materias:
                    self.treeMateriaAlumno.insert('', 'end', values=(materia,))
                self.txPasswordAlumno.insert(0, alumno[9])
                self.grupoComboAlumno.set(alumno[10])
            else:
                messagebox.showerror("Error", "Alumno no encontrado")

    def editarAlumno(self):
        if self.validarCamposAlumno():
            materias = [self.treeMateriaAlumno.item(item, 'values')[0] for item in self.treeMateriaAlumno.get_children()]
            if not materias:
                messagebox.showerror("Error", "Debe agregar al menos una materia.")
                return
            materias_str = ', '.join(materias)
            alumno = {
                'alumnos_id': self.txIdAlumnoBuscar.get(),
                'nombre': self.txNombreAlumno.get(),
                'apaterno': self.txAPaternoAlumno.get(),
                'amaterno': self.txAMaternoAlumno.get(),
                'email': self.txEmailAlumno.get(),
                'estado': self.estadoComboAlumno.get(),
                'fecha_nac': self.txFechaAlumno.get(),
                'carrera': self.carreraComboAlumno.get(),
                'materia': materias_str,
                'password': self.txPasswordAlumno.get(),
                'grupo': self.grupoComboAlumno.get()
            }
            self.alumnos.edit(alumno)
            messagebox.showinfo("Éxito", "Alumno editado correctamente")
    
    def eliminarAlumno(self):
        alumnos_id = self.txIdAlumnoBuscar.get()
        if alumnos_id:
            self.alumnos.remove(alumnos_id)
            self.limpiarCamposAlumno()
    
    def agregarMateriaAlumno(self):
        materia = self.materiaComboAlumno.get()
        if materia == "Seleccione":
            messagebox.showerror("Error", "Seleccione una materia válida.")
            return
        for item in self.treeMateriaAlumno.get_children():
            if self.treeMateriaAlumno.item(item, 'values')[0] == materia:
                messagebox.showerror("Error", "La materia ya está en la lista.")
                return
        self.treeMateriaAlumno.insert('', 'end', values=(materia,))

    def cargarGrupoAlumno(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT grupo_id, nombre FROM grupos")
            grupos = cursor.fetchall()
            self.listaGrupos = {nombre: grupo_id for grupo_id, nombre in grupos}
            self.grupoComboAlumno['values'] = list(self.listaGrupos.keys())
            db.con.close()
    
    def actualizaGruposAlumno(self, event):
        nombreGrupo = self.grupoComboAlumno.get()
        grupoNombre = self.listaGrupos.get(nombreGrupo, "")
     
    def validarCamposAlumno(self):
        if self.estadoComboAlumno.get() == "Seleccione" or self.carreraComboAlumno.get() == "Seleccione" or not self.txNombreAlumno.get() or not self.txAPaternoAlumno.get()\
            or not self.txAMaternoAlumno.get() or not self.txEmailAlumno.get() or not self.txFechaAlumno.get() or not self.txPasswordAlumno.get() or self.grupoComboAlumno.get() == "Seleccione":
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True
    
    #FUNC:-----------------------MAESTROS-----------------------#

    def limpiarCamposMaestro(self):
        self.txNombreMaestro.delete(0, 'end')
        self.txAPaternoMaestro.delete(0, 'end')
        self.txAMaternoMaestro.delete(0, 'end')
        self.txEmailMaestro.delete(0, 'end')
        self.carreraComboMaestro.set("Seleccione")
        self.materiaComboMaestro.set("Seleccione")
        self.txGradoEstudiosMaestro.delete(0, 'end')
        self.grupoComboMaestro.set("Seleccione")
        self.treeMateriaMaestro.delete(*self.treeMateriaMaestro.get_children())
    
    def guardarMaestro(self):
        if self.validarCamposMaestro():
            materias = [self.treeMateriaMaestro.item(item, 'values')[0] for item in self.treeMateriaMaestro.get_children()]
            if not materias:
                messagebox.showerror("Error", "Debe agregar al menos una materia.")
                return
            materias_str = ', '.join(materias)
            maestro = {
                'nombre': self.txNombreMaestro.get(),
                'apaterno': self.txAPaternoMaestro.get(),
                'amaterno': self.txAMaternoMaestro.get(),
                'email': self.txEmailMaestro.get(),
                'grado_estudios': self.txGradoEstudiosMaestro.get(),
                'carrera': self.carreraComboMaestro.get(),
                'materia': materias_str,
                'grupo': self.grupoComboMaestro.get()
            }
            self.maestros.save(maestro)
            messagebox.showinfo("Éxito", "Maestro guardado correctamente")
    
    def buscarMaestro(self):
        maestro_id = self.txIdMaestroBuscar.get()
        if maestro_id:
            maestro = self.maestros.search(maestro_id)
            if maestro:
                self.limpiarCamposMaestro()
                self.txNombreMaestro.insert(0, maestro[1])
                self.txAPaternoMaestro.insert(0, maestro[2])
                self.txAMaternoMaestro.insert(0, maestro[3])
                self.txEmailMaestro.insert(0, maestro[4])
                self.carreraComboMaestro.set(maestro[5])
                materias = maestro[6].split(', ') if maestro[6] else []
                for materia in materias:
                    self.treeMateriaMaestro.insert('', 'end', values=(materia,))
                self.txGradoEstudiosMaestro.insert(0, maestro[7])
                self.grupoComboMaestro.set(maestro[8])
            else:
                messagebox.showerror("Error", "Maestro no encontrado")
    
    def editarMaestro(self):
        if self.validarCamposMaestro():
            materias = [self.treeMateriaMaestro.item(item, 'values')[0] for item in self.treeMateriaMaestro.get_children()]
            if not materias:
                messagebox.showerror("Error", "Debe agregar al menos una materia.")
                return
            materias_str = ', '.join(materias)
            maestro = {
                'maestro_id': self.txIdMaestroBuscar.get(),
                'nombre': self.txNombreMaestro.get(),
                'apaterno': self.txAPaternoMaestro.get(),
                'amaterno': self.txAMaternoMaestro.get(),
                'email': self.txEmailMaestro.get(),
                'grado_estudios': self.txGradoEstudiosMaestro.get(),
                'carrera': self.carreraComboMaestro.get(),
                'materia': materias_str,
                'grupo': self.grupoComboMaestro.get()
            }
            self.maestros.edit(maestro)
            messagebox.showinfo("Éxito", "Maestro editado correctamente")
    
    def eliminarMaestro(self):
        maestro_id = self.txIdMaestroBuscar.get()
        if maestro_id:
            self.maestros.remove(maestro_id)
            self.limpiarCamposMaestro()
    
    def cargarMaestros(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT maestro_id, nombre FROM maestros")
            maestros = cursor.fetchall()
            self.listaMaestros = {nombre: maestro_id for maestro_id, nombre in maestros}
            self.maestrosComboGrupo['values'] = list(self.listaMaestros.keys())
            db.con.close()
    
    def actualizarMaestroGrupo(self, event):
        nombreMaestro = self.maestrosComboGrupo.get()
        maestroID = self.listaMaestros.get(nombreMaestro, "")

    def cargarGrupoMaestro(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT grupo_id, nombre FROM grupos")
            grupos = cursor.fetchall()
            self.listaGrupos = {nombre: grupo_id for grupo_id, nombre in grupos}
            self.grupoComboMaestro['values'] = list(self.listaGrupos.keys())
            db.con.close()
    
    def actualizaGruposMaestro(self, event):
        nombreGrupo = self.grupoComboMaestro.get()
        maestroID = self.listaGrupos.get(nombreGrupo, "")
    
    def agregarMateriaMaestro(self):
        materia = self.materiaComboMaestro.get()
        if materia == "Seleccione":
            messagebox.showerror("Error", "Seleccione una materia válida.")
            return
        for item in self.treeMateriaMaestro.get_children():
            if self.treeMateriaMaestro.item(item, 'values')[0] == materia:
                messagebox.showerror("Error", "La materia ya está en la lista.")
                return
        self.treeMateriaMaestro.insert('', 'end', values=(materia,))
        
    def validarCamposMaestro(self):
        if self.carreraComboMaestro.get() == "Seleccione" or not self.txNombreMaestro.get() or not self.txAPaternoMaestro.get() or not self.txAMaternoMaestro.get()\
                or not self.txEmailMaestro.get() or not self.txGradoEstudiosMaestro.get() or self.grupoComboMaestro.get() == "Seleccione":
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True
    
    #FUNC:-----------------------MATERIAS-----------------------#

    def limpiarCamposMateria(self):
        self.txAsignaturaMateria.delete(0, 'end')
        self.txCreditosMateria.delete(0, 'end')
        self.carreraComboMateria.set("Seleccione")
        self.txSemestreMateria.delete(0, 'end')
    
    def guardarMateria(self):
        if self.validarCamposMateria():
            materia = {
                'asignatura': self.txAsignaturaMateria.get(),
                'creditos': self.txCreditosMateria.get(),
                'semestre': self.carreraComboMateria.get(),
                'carrera': self.txSemestreMateria.get()
            }
            self.materias.save(materia)
    
    def buscarMateria(self):
        materias_id = self.txIDMateriaBuscar.get()
        if materias_id:
            materia = self.materias.search(materias_id)
            if materia:
                self.txAsignaturaMateria.delete(0, 'end')
                self.txCreditosMateria.delete(0, 'end')
                self.carreraComboMateria.set("Seleccione")
                self.txSemestreMateria.delete(0, 'end')
                self.txAsignaturaMateria.insert(0, materia[1])
                self.txCreditosMateria.insert(0, materia[2])
                self.txSemestreMateria.insert(0, materia[3])
                self.carreraComboMateria.set(materia[4])
            else:
                messagebox.showerror("Error", "Materia no encontrada")
    
    def editarMateria(self):
        if self.validarCamposMateria():
            materia = {
                'materias_id': self.txIDMateriaBuscar.get(),
                'asignatura': self.txAsignaturaMateria.get(),
                'creditos': self.txCreditosMateria.get(),
                'carrera': self.carreraComboMateria.get(),
                'semestre': self.txSemestreMateria.get()
            }
            self.materias.edit(materia)
    
    def eliminarMateria(self):
        materias_id = self.txIDMateriaBuscar.get()
        if materias_id:
            self.materias.remove(materias_id)
            self.limpiarCamposMateria()
    
    def cargarMateriasAlumno(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT materias_id, asignatura FROM materias")
            materias = cursor.fetchall()
            self.listaMateriasAlumno = {asignatura: materias_id for materias_id, asignatura in materias}
            self.materiaComboAlumno['values'] = list(self.listaMateriasAlumno.keys())
            db.con.close()
    
    def cargarMateriasGrupo(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT materias_id, asignatura FROM materias")
            materias = cursor.fetchall()
            self.listaMateriasGrupo = {asignatura: materias_id for materias_id, asignatura in materias}
            self.materiaComboGrupo['values'] = list(self.listaMateriasGrupo.keys())
            db.con.close()
    
    def cargarMateriasMaestro(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT materias_id, asignatura FROM materias")
            materias = cursor.fetchall()
            self.listaMateriasMaestro = {asignatura: materias_id for materias_id, asignatura in materias}
            self.materiaComboMaestro['values'] = list(self.listaMateriasMaestro.keys())
            db.con.close()
    
    def actualizarMateriasGrupo(self, event):
        asignatura = self.materiaComboGrupo.get()
        materiasID = self.listaMaestros.get(asignatura, "")
    
    def actualizarMateriasAlumno(self, event):
        asignatura = self.materiaComboAlumno.get()
        materiasID = self.listaMaestros.get(asignatura, "")

    def actualizarMateriasMaestro(self, event):
        asignatura = self.materiaComboMaestro.get()
        materiasID = self.listaMaestros.get(asignatura, "")
        
    def validarCamposMateria(self):
        if self.carreraComboMateria.get() == "Seleccione" or not self.txAsignaturaMateria.get() or not self.txCreditosMateria.get() or not self.txSemestreMateria.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True
    
    #FUNC:-----------------------GRUPOS-----------------------#

    def limpiarCamposGrupo(self):
        self.txNombreGrupo.delete(0, 'end')
        self.txFechaGrupo.delete(0, 'end')
        self.salonComboGrupo.set("Seleccione")
        self.horarioComboGrupo.set("Seleccione")
        self.txSemestreGrupo.delete(0, 'end')
        self.carreraComboGrupo.set("Seleccione")
        self.maestrosComboGrupo.set("Seleccione")
        self.materiaComboGrupo.set("Seleccione")
        self.maxAlumsComboGrupo.set("Seleccione")
        self.txAlumnosReg.delete(0, 'end')
        #!self.treeMateriaGrupo.delete(*self.treeMateriaGrupo.get_children())
    
    def guardarGrupo(self):
        if self.validarCamposGrupo():
            """materias = [self.treeMateriaGrupo.item(item, 'values')[0] for item in self.treeMateriaGrupo.get_children()]
            if not materias:
                messagebox.showerror("Error", "Debe agregar al menos una materia.")
                return
            materias_str = ', '.join(materias)"""
            grupo = {
                'nombre': self.txNombreGrupo.get(),
                'fecha': self.txFechaGrupo.get(),
                'carrera': self.carreraComboGrupo.get(),
                'materia': self.materiaComboGrupo.get(),
                'maestro': self.maestrosComboGrupo.get(),
                'salon': self.salonComboGrupo.get(),
                'horario': self.horarioComboGrupo.get(),
                'semestre': self.txSemestreGrupo.get(),
                'max_alumnos': self.maxAlumsComboGrupo.get(),
                'alum_reg': self.txAlumnosReg.get()
            }
            self.grupos.save(grupo)
    
    def buscarGrupo(self):
        grupo_id = self.txIdGrupoBuscar.get()
        if grupo_id:
            grupo = self.grupos.search(grupo_id)
            if grupo:
                self.limpiarCamposGrupo()
                self.txNombreGrupo.insert(0, grupo[1])
                self.txFechaGrupo.insert(0, grupo[2])
                self.carreraComboGrupo.set(grupo[3])
                self.materiaComboGrupo.set(grupo[4])
                self.maestrosComboGrupo.set(grupo[5])
                self.salonComboGrupo.set(grupo[6])
                self.horarioComboGrupo.set(grupo[7])
                self.txSemestreGrupo.insert(0, grupo[8])
                self.maxAlumsComboGrupo.set(grupo[9])
                self.txAlumnosReg.insert(0, grupo[10])
            else:
                messagebox.showerror("Error", "Grupo no encontrado")
    
    def editarGrupo(self):
        if self.validarCamposGrupo():
            """materias = [self.treeMateriaGrupo.item(item, 'values')[0] for item in self.treeMateriaGrupo.get_children()]
            if not materias:
                messagebox.showerror("Error", "Debe agregar al menos una materia.")
                return
            materias_str = ', '.join(materias)"""
            grupo = {
                'grupo_id': self.txIdGrupoBuscar.get(),
                'nombre': self.txNombreGrupo.get(),
                'fecha': self.txFechaGrupo.get(),
                'carrera': self.carreraComboGrupo.get(),
                'materia': self.materiaComboGrupo.get(),
                'maestro': self.maestrosComboGrupo.get(),
                'salon': self.salonComboGrupo.get(),
                'horario': self.horarioComboGrupo.get(),
                'semestre': self.txSemestreGrupo.get(),
                'max_alumnos': self.maxAlumsComboGrupo.get(),
                'alum_reg': self.txAlumnosReg.get()
            }
            self.grupos.edit(grupo)
    
    def eliminarGrupo(self):
        grupo_id = self.txIdGrupoBuscar.get()
        if grupo_id:
            self.grupos.remove(grupo_id)
            self.limpiarCamposGrupo()

    def agregarMateriaGrupo(self):
        materia = self.materiaComboGrupo.get()
        if materia == "Seleccione":
            messagebox.showerror("Error", "Seleccione una materia válida.")
            return
        for item in self.treeMateriaGrupo.get_children():
            if self.treeMateriaGrupo.item(item, 'values')[0] == materia:
                messagebox.showerror("Error", "La materia ya está en la lista.")
                return
        self.treeMateriaGrupo.insert('', 'end', values=(materia,))
        
    def validarCamposGrupo(self):
        if self.salonComboGrupo.get() == "Seleccione" or self.horarioComboGrupo.get() == "Seleccione" or self.carreraComboGrupo.get() == "Seleccione"\
            or self.maestrosComboGrupo.get() == "Seleccione" or self.maxAlumsComboGrupo.get() == "Seleccione" or self.materiaComboGrupo.get() == "Seleccione"\
                or not self.txNombreGrupo.get() or not self.txFechaGrupo.get() or not self.txSemestreGrupo.get() or not self.txAlumnosReg.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True

    # -----------------------HORARIO-----------------------#

    def limpiarCamposHorario(self):
        self.comboTurnoHorario.set("Seleccione")
        self.txHoraHorario.delete(0, 'end')
    
    def guardarHorario(self):
        if self.validarCamposHorario():
            horario = {
                'turno': self.comboTurnoHorario.get(),
                'hora': self.txHoraHorario.get()
            }
            self.horarios.save(horario)
    
    def buscarHorario(self):
        horario_id = self.txIdBuscarHorario.get()
        if horario_id:
            horario = self.horarios.search(horario_id)
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
            self.horarios.edit(horario)
    
    def eliminarHorario(self):
        horario_id = self.txIdBuscarHorario.get()
        if horario_id:
            self.horarios.remove(horario_id)
            self.limpiarCamposHorario()
    
    def cargarHorario(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT horario_id, hora FROM horarios")
            horarios = cursor.fetchall()
            self.listaHorarios = {hora: horario_id for horario_id, hora in horarios}
            self.horarioComboGrupo['values'] = list(self.listaHorarios.keys())
            db.con.close()
    
    def actualizarHorarioGrupo(self, event):
        horaHorario = self.horarioComboGrupo.get()
        maestroID = self.listaHorarios.get(horaHorario, "")
        
    def validarCamposHorario(self):
        if self.comboTurnoHorario.get() == "Seleccione" or not self.txHoraHorario.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True
    
    #-----------------------SALON-----------------------#

    def limpiarCamposSalon(self):
        self.comboEdificioSalon.set("Seleccione")
        self.txAula.delete(0, 'end')
    
    def guardarSalon(self):
        if self.validarCamposSalon():
            salon = {
                'edificio': self.comboEdificioSalon.get(),
                'nombre': self.txAula.get()
            }
            self.salones.save(salon)
    
    def buscarSalon(self):
        salon_id = self.txIdBuscarSalon.get()
        if salon_id:
            salon = self.salones.search(salon_id)
            if salon:
                self.comboEdificioSalon.set(salon[2])
                self.txAula.delete(0, 'end')
                self.txAula.insert(0, salon[1])
            else:
                messagebox.showerror("Error", "Salon no encontrado")
    
    def editarSalon(self):
        if self.validarCamposSalon():
            salon = {
                'edificio': self.comboEdificioSalon.get(),
                'nombre': self.txAula.get()
            }
            self.salones.edit(salon)
    
    def eliminarSalon(self):
        salon_id = self.txIdBuscarSalon.get()
        if salon_id:
            self.salones.remove(salon_id)
            self.limpiarCamposSalon()
    
    def cargarSalones(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT salon_id, nombre FROM salones")
            Salones = cursor.fetchall()
            self.listaSalones = {nombre: salon_id for salon_id, nombre in Salones}
            self.salonComboGrupo['values'] = list(self.listaSalones.keys())
            db.con.close()
    
    def actualizarSalonesGrupo(self, event):
        aulaSalon = self.salonComboGrupo.get()
        salonID = self.listaSalones.get(aulaSalon, "")
        
    def validarCamposSalon(self):
        if self.comboEdificioSalon.get() == "Seleccione" or not self.txAula.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True
    
    # -----------------------CARRERA-----------------------#

    def limpiarCamposCarrera(self):
        self.comboNumSemestres.set("Seleccione")
        self.txNombreCarrera.delete(0, 'end')
    
    def guardarCarrera(self):
        if self.validarCamposCarrera():
            carrera = {
                'nombre': self.txNombreCarrera.get(),
                'num_semestres': self.comboNumSemestres.get()
            }
            self.carreras.save(carrera)
    
    def buscarCarrera(self):
        carrera_id = self.txIdBuscarCarrera.get()
        if carrera_id:
            carrera = self.carreras.search(carrera_id)
            if carrera:
                self.comboNumSemestres.set(carrera[2])
                self.txNombreCarrera.delete(0, 'end')
                self.txNombreCarrera.insert(0, carrera[1])
            else:
                messagebox.showerror("Error", "Carrera no encontrada")
    
    def editarCarrera(self):
        if self.validarCamposCarrera():
            carrera = {
                'nombre': self.txNombreCarrera.get(),
                'num_semestres': self.comboNumSemestres.get()
            }
            self.carreras.edit(carrera)
    
    def eliminarCarrera(self):
        carrera_id = self.txIdBuscarCarrera.get()
        if carrera_id:
            self.carreras.remove(carrera_id)
            self.limpiarCamposCarrera()
    
    def validarCamposCarrera(self):
        if self.comboNumSemestres.get() == "Seleccione" or not self.txNombreCarrera.get():
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True
    
    def cargarCarreraAlumno(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT carrera_id, nombre FROM carreras")
            carreras = cursor.fetchall()
            self.listaCarreraAlumno = {nombre: carrera_id for carrera_id, nombre in carreras}
            self.carreraComboAlumno['values'] = list(self.listaCarreraAlumno.keys())
            db.con.close()
    
    def actualizarCarreraAlumno(self, event):
        carreraAlumno = self.carreraComboAlumno.get()
        carreraAlmID = self.listaCarreraAlumno.get(carreraAlumno, "")
    
    def cargarCarreraProfe(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT carrera_id, nombre FROM carreras")
            carreras = cursor.fetchall()
            self.listaCarreraProfe = {nombre: carrera_id for carrera_id, nombre in carreras}
            self.carreraComboMaestro['values'] = list(self.listaCarreraProfe.keys())
            db.con.close()
    
    def actualizarCarreraProfe(self, event):
        carreraProfe = self.carreraComboMaestro.get()
        carreraProfID = self.listaCarreraProfe.get(carreraProfe, "")
    
    def cargarCarreraMateria(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT carrera_id, nombre FROM carreras")
            carreras = cursor.fetchall()
            self.listaCarreraMateria = {nombre: carrera_id for carrera_id, nombre in carreras}
            self.carreraComboMateria['values'] = list(self.listaCarreraMateria.keys())
            db.con.close()
    
    def actualizarCarreraMateria(self, event):
        carreraMateria = self.carreraComboMateria.get()
        carreraMatID = self.listaCarreraMateria.get(carreraMateria, "")
    
    def cargarCarreraGrupo(self):
        db = dbEscolar()
        conn = db.con.open()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT carrera_id, nombre FROM carreras")
            carreras = cursor.fetchall()
            self.listaCarreraGrupo = {nombre: carrera_id for carrera_id, nombre in carreras}
            self.carreraComboGrupo['values'] = list(self.listaCarreraGrupo.keys())
            db.con.close()
    
    def actualizarCarreraGrupo(self, event):
        carreraGrupo = self.carreraComboGrupo.get()
        carreraGrupoID = self.listaCarreraGrupo.get(carreraGrupo, "")
    
    #-----------------------PLANEACIÓN-----------------------#

    def actualizarDatosPlan(self):
        for item in self.treePlaneacion.get_children():
            self.treePlaneacion.delete(item)

        planHorario = self.planeacion.groups()
        planHorario_ordenado = sorted(planHorario, key=lambda x: x[4])

        for row in planHorario_ordenado:
            self.treePlaneacion.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    login = LoginWindow(root)
    root.mainloop()