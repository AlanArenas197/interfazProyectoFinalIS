import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Control Escolar - <USUARIO>")
root.geometry("850x500")

notebook = ttk.Notebook(root)
     
#-----------------------USUARIOS-----------------------#
        
pestanaUsuarios = ttk.Frame(notebook)
pestanaUsuarios.grid_columnconfigure(0, weight=1)
pestanaUsuarios.grid_columnconfigure(1, weight=1)

ttk.Label(pestanaUsuarios, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
txIdUsuarioBuscar = ttk.Entry(pestanaUsuarios, width=30)
txIdUsuarioBuscar.grid(row=0, column=1, padx=10, pady=10)

btnBuscarUsuario = ttk.Button(pestanaUsuarios, text="Buscar")
btnBuscarUsuario.grid(row=0, column=2, padx=10, pady=10)

ttk.Label(pestanaUsuarios, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
txNombreUsuario = ttk.Entry(pestanaUsuarios, width=30)
txNombreUsuario.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(pestanaUsuarios, text="A. Paterno:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
txAPaternoUsuario = ttk.Entry(pestanaUsuarios, width=30)
txAPaternoUsuario.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(pestanaUsuarios, text="A. Materno:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
txAMaternoUsuario = ttk.Entry(pestanaUsuarios, width=30)
txAMaternoUsuario.grid(row=2, column=3, padx=10, pady=5)

ttk.Label(pestanaUsuarios, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
txEmailUsuario = ttk.Entry(pestanaUsuarios, width=30)
txEmailUsuario.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(pestanaUsuarios, text="Username:").grid(row=3, column=2, padx=10, pady=5, sticky="e")
txUsernameUsuario = ttk.Entry(pestanaUsuarios, width=30)
txUsernameUsuario.grid(row=3, column=3, padx=10, pady=5)

ttk.Label(pestanaUsuarios, text="Password:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
txPassewordUsuario = ttk.Entry(pestanaUsuarios, width=30)
txPassewordUsuario.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(pestanaUsuarios, text="Perfil:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
comboPerfilUsuario = ttk.Combobox(pestanaUsuarios, values=["Seleccione", "Admin", "Rector", "Secretaria"], state='readonly')
comboPerfilUsuario.set("Seleccione")
comboPerfilUsuario.grid(row=5, column=1, padx=10, pady=5)

btnNuevoUsuario = ttk.Button(pestanaUsuarios, text="Nuevo")
btnNuevoUsuario.grid(row=7, column=0, padx=10, pady=10, sticky="e")

btnGuardarUsuario = ttk.Button(pestanaUsuarios, text="Guardar")
btnGuardarUsuario.grid(row=7, column=1, padx=10, pady=10, sticky="w")

btnCancelarUsuario = ttk.Button(pestanaUsuarios, text="Cancelar")
btnCancelarUsuario.grid(row=7, column=2, padx=10, pady=10, sticky="w")

btnEditarUsuario = ttk.Button(pestanaUsuarios, text="Editar")
btnEditarUsuario.grid(row=7, column=3, padx=10, pady=10, sticky="w")

btnEliminarUsuario = ttk.Button(pestanaUsuarios, text="Eliminar")
btnEliminarUsuario.grid(row=7, column=4, padx=10, pady=10, sticky="w")

notebook.add(pestanaUsuarios, text="Usuarios")

#-----------------------ALUMNOS-----------------------#
pestanaAlumnos = ttk.Frame(notebook)
pestanaAlumnos.grid_columnconfigure(0, weight=1)
pestanaAlumnos.grid_columnconfigure(1, weight=1)

ttk.Label(pestanaAlumnos, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
txIdAlumnoBuscar = ttk.Entry(pestanaAlumnos, width=30)
txIdAlumnoBuscar.grid(row=0, column=1, padx=5, pady=5)

btnBuscarAlumno = ttk.Button(pestanaAlumnos, text="Buscar")
btnBuscarAlumno.grid(row=0, column=2, padx=5, pady=5)

ttk.Label(pestanaAlumnos, text="Nombre:").grid(row=1, column=0, sticky="e")
txNombreAlumno = ttk.Entry(pestanaAlumnos, width=30)
txNombreAlumno.grid(row=1, column=1, pady=5)

ttk.Label(pestanaAlumnos, text="Estado:").grid(row=1, column=2, sticky="e")
estadoComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", "Aguascalientes", "Baja California", "Baja California Sur",
                                                    "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", 
                                                    "Ciudad de México", "Durango", "Guanajuato", "Guerrero",
                                                    "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
                                                    "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
                                                    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", 
                                                    "Zacatecas"], width=28)
estadoComboAlumno.grid(row=1, column=3, pady=5)
estadoComboAlumno.set("Seleccione")

ttk.Label(pestanaAlumnos, text="A Paterno:").grid(row=2, column=0, sticky="e")
txAPaternoAlumno = ttk.Entry(pestanaAlumnos, width=30)
txAPaternoAlumno.grid(row=2, column=1, pady=5)

ttk.Label(pestanaAlumnos, text="Fecha Nac:").grid(row=2, column=2, sticky="e")
txFechaAlumno = ttk.Entry(pestanaAlumnos, width=30)
txFechaAlumno.grid(row=2, column=3, pady=5)

ttk.Label(pestanaAlumnos, text="A Materno:").grid(row=3, column=0, sticky="e")
txAMaternoAlumno = ttk.Entry(pestanaAlumnos, width=30)
txAMaternoAlumno.grid(row=3, column=1, pady=5)

ttk.Label(pestanaAlumnos, text="Carrera:").grid(row=3, column=2, sticky="e")
carreraComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
carreraComboAlumno.grid(row=3, column=3, pady=5)
carreraComboAlumno.set("Seleccione")

ttk.Label(pestanaAlumnos, text="Email:").grid(row=4, column=0, sticky="e")
txEmailAlumno = ttk.Entry(pestanaAlumnos, width=30)
txEmailAlumno.grid(row=4, column=1, pady=5)

ttk.Label(pestanaAlumnos, text="Materia:").grid(row=4, column=2, sticky="e")
materiaComboAlumno = ttk.Combobox(pestanaAlumnos, values=["Seleccione", 
    "Física 1", "Programación Estructura", "Estructura de Datos", 
    "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
materiaComboAlumno.grid(row=4, column=3, pady=5)
materiaComboAlumno.set("Seleccione")

btnAgregarMateriaAlumno = ttk.Button(pestanaAlumnos, text="Agregar")
btnAgregarMateriaAlumno.grid(row=5, column=3, padx=5, pady=5)

treeMateriaAlumno = ttk.Treeview(pestanaAlumnos, columns=("Nombre"), show="headings", height=6)
treeMateriaAlumno.heading("Nombre", text="Nombre")
treeMateriaAlumno.grid(row=6, column=3, pady=5)

btnNuevoAlumno = ttk.Button(pestanaAlumnos, text="Nuevo")
btnNuevoAlumno.grid(row=8, column=0, padx=10, pady=10, sticky="e")

btnGuardarAlumno = ttk.Button(pestanaAlumnos, text="Guardar")
btnGuardarAlumno.grid(row=8, column=1, padx=10, pady=10, sticky="w")

btnCancelarAlumno = ttk.Button(pestanaAlumnos, text="Cancelar")
btnCancelarAlumno.grid(row=8, column=2, padx=10, pady=10, sticky="w")

btnEditarAlumno = ttk.Button(pestanaAlumnos, text="Editar")
btnEditarAlumno.grid(row=8, column=3, padx=10, pady=10, sticky="w")

btnEliminarAlumno = ttk.Button(pestanaAlumnos, text="Eliminar")
btnEliminarAlumno.grid(row=8, column=4, padx=10, pady=10, sticky="w")

notebook.add(pestanaAlumnos, text="Alumnos")

#-----------------------MAESTROS-----------------------#

pestanaMaestros = ttk.Frame(notebook)
pestanaMaestros.grid_columnconfigure(0, weight=1)
pestanaMaestros.grid_columnconfigure(1, weight=1)

ttk.Label(pestanaMaestros, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
txIdMaestroBuscar = ttk.Entry(pestanaMaestros, width=30)
txIdMaestroBuscar.grid(row=0, column=1, padx=5, pady=5)

btnBuscarMaestro = ttk.Button(pestanaMaestros, text="Buscar")
btnBuscarMaestro.grid(row=0, column=2, padx=5, pady=5)

ttk.Label(pestanaMaestros, text="Nombre:").grid(row=1, column=0, sticky="e")
txNombreMaestro = ttk.Entry(pestanaMaestros, width=30)
txNombreMaestro.grid(row=1, column=1, pady=5)

ttk.Label(pestanaMaestros, text="Grado de Estudios:").grid(row=1, column=2, sticky="e")
txGradoEstudiosMaestro = ttk.Entry(pestanaMaestros, width=30)
txGradoEstudiosMaestro.grid(row=1, column=3, pady=5)

ttk.Label(pestanaMaestros, text="A Paterno:").grid(row=2, column=0, sticky="e")
txAPaternoMaestro = ttk.Entry(pestanaMaestros, width=30)
txAPaternoMaestro.grid(row=2, column=1, pady=5)

ttk.Label(pestanaMaestros, text="Carrera:").grid(row=2, column=2, sticky="e")
carreraComboMaestro = ttk.Combobox(pestanaMaestros, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
carreraComboMaestro.grid(row=2, column=3, pady=5)
carreraComboMaestro.set("Seleccione")

ttk.Label(pestanaMaestros, text="A Materno:").grid(row=3, column=0, sticky="e")
txAMaternoMaestro = ttk.Entry(pestanaMaestros, width=30)
txAMaternoMaestro.grid(row=3, column=1, pady=5)

ttk.Label(pestanaMaestros, text="Materia:").grid(row=3, column=2, sticky="e")
materiaComboMaestro = ttk.Combobox(pestanaMaestros, values=[
    "Física 1", "Programación Estructura", "Estructura de Datos", 
    "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
materiaComboMaestro.grid(row=3, column=3, pady=5)
materiaComboMaestro.set("Seleccione")

ttk.Label(pestanaMaestros, text="Email:").grid(row=4, column=0, sticky="e")
txEmailMaestro = ttk.Entry(pestanaMaestros, width=30)
txEmailMaestro.grid(row=4, column=1, pady=5)

btnAgregarMateriaMaestro = ttk.Button(pestanaMaestros, text="Agregar")
btnAgregarMateriaMaestro.grid(row=5, column=3, padx=5, pady=5)

treeMateriaMaestro = ttk.Treeview(pestanaMaestros, columns=("Nombre"), show="headings", height=6)
treeMateriaMaestro.heading("Nombre", text="Nombre")
treeMateriaMaestro.grid(row=6, column=3, pady=5)

btnNuevoMaestro = ttk.Button(pestanaMaestros, text="Nuevo")
btnNuevoMaestro.grid(row=8, column=0, padx=10, pady=10, sticky="e")

btnGuardarMaestro = ttk.Button(pestanaMaestros, text="Guardar")
btnGuardarMaestro.grid(row=8, column=1, padx=10, pady=10, sticky="w")

btnCancelarMaestro = ttk.Button(pestanaMaestros, text="Cancelar")
btnCancelarMaestro.grid(row=8, column=2, padx=10, pady=10, sticky="w")

btnEditarMaestro = ttk.Button(pestanaMaestros, text="Editar")
btnEditarMaestro.grid(row=8, column=3, padx=10, pady=10, sticky="w")

btnEliminarMaestro = ttk.Button(pestanaMaestros, text="Eliminar")
btnEliminarMaestro.grid(row=8, column=4, padx=10, pady=10, sticky="w")

notebook.add(pestanaMaestros, text="Maestros")

#-----------------------MATERIAS-----------------------#

pestanaMaterias = ttk.Frame(notebook)
pestanaMaterias.grid_columnconfigure(0, weight=1)
pestanaMaterias.grid_columnconfigure(1, weight=1)

ttk.Label(pestanaMaterias, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
txIDMateriaBuscar = ttk.Entry(pestanaMaterias, width=30)
txIDMateriaBuscar.grid(row=0, column=1, padx=10, pady=10)

btnBuscarMateria = ttk.Button(pestanaMaterias, text="Buscar")
btnBuscarMateria.grid(row=0, column=2, padx=10, pady=10)

ttk.Label(pestanaMaterias, text="Asignatura:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
txAsignaturaMateria = ttk.Entry(pestanaMaterias, width=30)
txAsignaturaMateria.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(pestanaMaterias, text="Creditos:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
txCreditosMateria = ttk.Entry(pestanaMaterias, width=30)
txCreditosMateria.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(pestanaMaterias, text="Carrera:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
carreraComboMateria = ttk.Combobox(pestanaMaterias, values=["Seleccione", "Ingeniería", "Licenciatura"], width=30)
carreraComboMateria.grid(row=2, column=3, padx=10, pady=5)
carreraComboMateria.set("Seleccione")

ttk.Label(pestanaMaterias, text="Semestre:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
txSemestreMateria = ttk.Entry(pestanaMaterias, width=30)
txSemestreMateria.grid(row=3, column=1, padx=10, pady=5)

btnNuevoMateria = ttk.Button(pestanaMaterias, text="Nuevo")
btnNuevoMateria.grid(row=5, column=0, padx=10, pady=10, sticky="e")

btnGuardarMateria = ttk.Button(pestanaMaterias, text="Guardar")
btnGuardarMateria.grid(row=5, column=1, padx=10, pady=10, sticky="w")

btnCancelarMateria = ttk.Button(pestanaMaterias, text="Cancelar")
btnCancelarMateria.grid(row=5, column=2, padx=10, pady=10, sticky="w")

btnEditarMateria = ttk.Button(pestanaMaterias, text="Editar")
btnEditarMateria.grid(row=5, column=3, padx=10, pady=10, sticky="w")

btnEliminarMateria = ttk.Button(pestanaMaterias, text="Eliminar")
btnEliminarMateria.grid(row=5, column=4, padx=10, pady=10, sticky="w")

notebook.add(pestanaMaterias, text="Materias")

#-----------------------GRUPOS-----------------------#

pestanaGrupos = ttk.Frame(notebook)
pestanaGrupos.grid_columnconfigure(0, weight=1)
pestanaGrupos.grid_columnconfigure(1, weight=1)

ttk.Label(pestanaGrupos, text="Ingrese ID a buscar:").grid(row=0, column=0, pady=5, sticky="e")
txIdGrupoBuscar = ttk.Entry(pestanaGrupos, width=30)
txIdGrupoBuscar.grid(row=0, column=1, padx=5, pady=5)

btnBuscarGrupo = ttk.Button(pestanaGrupos, text="Buscar")
btnBuscarGrupo.grid(row=0, column=2, padx=5, pady=5)

ttk.Label(pestanaGrupos, text="Nombre Grupo:").grid(row=1, column=0, sticky="e")
txNombreGrupo = ttk.Entry(pestanaGrupos, width=30)
txNombreGrupo.grid(row=1, column=1, pady=5)

ttk.Label(pestanaGrupos, text="Fecha:").grid(row=1, column=2, sticky="e")
txFechaGrupo = ttk.Entry(pestanaGrupos, width=30)
txFechaGrupo.grid(row=1, column=3, pady=5)

ttk.Label(pestanaGrupos, text="Salon:").grid(row=2, column=0, sticky="e")
salonComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione","Salones"], width=28)
salonComboGrupo.grid(row=2, column=1, pady=5)
salonComboGrupo.set("Seleccione")

ttk.Label(pestanaGrupos, text="Horario:").grid(row=2, column=2, sticky="e")
horarioComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "Horario"], width=28)
horarioComboGrupo.grid(row=2, column=3, pady=5)
horarioComboGrupo.set("Seleccione")

ttk.Label(pestanaGrupos, text="Semestre:").grid(row=3, column=0, sticky="e")
txSemestreGrupo = ttk.Entry(pestanaGrupos, width=30)
txSemestreGrupo.grid(row=3, column=1, pady=5)

ttk.Label(pestanaGrupos, text="Carrera:").grid(row=3, column=2, sticky="e")
carreraComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "Ingeniería", "Licenciatura"], width=28)
carreraComboGrupo.grid(row=3, column=3, pady=5)
carreraComboGrupo.set("Seleccione")

ttk.Label(pestanaGrupos, text="Maestros:").grid(row=4, column=0, sticky="e")
maestrosComboGrupo = ttk.Combobox(pestanaGrupos, values=["Maestros"], width=28)
maestrosComboGrupo.grid(row=4, column=1, pady=5)
maestrosComboGrupo.set("Seleccione")

ttk.Label(pestanaGrupos, text="Materia:").grid(row=4, column=2, sticky="e")
materiaComboGrupo = ttk.Combobox(pestanaGrupos, values=[
    "Física 1", "Programación Estructura", "Estructura de Datos", 
    "Inteligencia Artificial 1", "Ingeniería de Software 1"], width=28)
materiaComboGrupo.grid(row=4, column=3, pady=5)
materiaComboGrupo.set("Seleccione")

ttk.Label(pestanaGrupos, text="Alumnos Max.:").grid(row=5, column=0, sticky="e")
maxAlumsComboGrupo = ttk.Combobox(pestanaGrupos, values=["Seleccione", "1", "2", "3"], width=28)
maxAlumsComboGrupo.grid(row=5, column=1, pady=5)
maxAlumsComboGrupo.set("Seleccione")

btnNuevoCompra = ttk.Button(pestanaGrupos, text="Nuevo")
btnNuevoCompra.grid(row=7, column=0, padx=10, pady=10, sticky="e")

btnGuardarCompra = ttk.Button(pestanaGrupos, text="Guardar")
btnGuardarCompra.grid(row=7, column=1, padx=10, pady=10, sticky="w")

btnCancelarCompra = ttk.Button(pestanaGrupos, text="Cancelar")
btnCancelarCompra.grid(row=7, column=2, padx=10, pady=10, sticky="w")

btnEditarCompra = ttk.Button(pestanaGrupos, text="Editar")
btnEditarCompra.grid(row=7, column=3, padx=10, pady=10, sticky="w")

btnEliminarCompra = ttk.Button(pestanaGrupos, text="Eliminar")
btnEliminarCompra.grid(row=7, column=4, padx=10, pady=10, sticky="w")
        
notebook.add(pestanaGrupos, text="Grupos")

#-----------------------HORARIO-----------------------#

pestanaHorario = ttk.Frame(notebook)
pestanaHorario.grid_columnconfigure(0, weight=1)
pestanaHorario.grid_columnconfigure(1, weight=1)

ttk.Label(pestanaHorario, text="Ingrese ID grupo:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
txIdBuscarHorario = ttk.Entry(pestanaHorario, width=30)
txIdBuscarHorario.grid(row=0, column=1, padx=10, pady=10)

btnBuscarHorario = ttk.Button(pestanaHorario, text="Buscar")
btnBuscarHorario.grid(row=0, column=2, padx=10, pady=10)

ttk.Label(pestanaHorario, text="Turno:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
comboTurnoHorario = ttk.Combobox(pestanaHorario, values=["Seleccione", "Matutino", "Vespertino"], width=28)
comboTurnoHorario.set("Seleccione")
comboTurnoHorario.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(pestanaHorario, text="Hora:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
txHoraHorario = ttk.Entry(pestanaHorario, width=30)
txHoraHorario.grid(row=2, column=1, padx=10, pady=5)

btnNuevoHorario = ttk.Button(pestanaHorario, text="Nuevo")
btnNuevoHorario.grid(row=6, column=0, padx=10, pady=10, sticky="e")

btnGuardarHorario = ttk.Button(pestanaHorario, text="Guardar")
btnGuardarHorario.grid(row=6, column=1, padx=10, pady=10, sticky="w")

btnCancelarHorario = ttk.Button(pestanaHorario, text="Cancelar")
btnCancelarHorario.grid(row=6, column=2, padx=10, pady=10, sticky="w")

btnEditarHorario = ttk.Button(pestanaHorario, text="Editar")
btnEditarHorario.grid(row=6, column=3, padx=10, pady=10, sticky="w")

btnEliminarHorario = ttk.Button(pestanaHorario, text="Eliminar")
btnEliminarHorario.grid(row=6, column=4, padx=10, pady=10, sticky="w")
        
notebook.add(pestanaHorario, text="Horario")

notebook.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()