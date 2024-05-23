import pymongo
import tkinter as tk
from tkinter import messagebox

# Establecer conexión con el servidor MongoDB
client = pymongo.MongoClient('192.168.200.220', 27017)
MONGO_DB = 'mi_base_de_datos'
db = client[MONGO_DB]

# Variables para los widgets de entrada
entry_matricula_buscar = None
entry_matricula = None
entry_marca = None
entry_modelo = None
entry_matricula_mant = None
entry_fecha = None
entry_descripcion = None
entry_costo = None

# Función para verificar la contraseña de administrador
def verificar_admin():
    if entry_usuario.get() == "admin" and entry_contraseña.get() == "admin":
        ventana_login.destroy()  # Cerrar la ventana de inicio de sesión
        abrir_ventana_principal()  # Abrir la ventana principal de la aplicación
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

# Función para agregar un nuevo vehículo
def agregar_vehiculo(matricula, marca, modelo):
    if not vehiculo_existe(matricula):
        vehiculos = db['Vehiculos']
        vehiculo = {
            "matricula": matricula,
            "marca": marca,
            "modelo": modelo
        }
        vehiculos.insert_one(vehiculo)
        messagebox.showinfo('Éxito', 'Vehículo agregado correctamente.')
        # Limpiar los campos de entrada después de agregar el vehículo
        entry_matricula.delete(0, tk.END)
        entry_marca.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
    else:
        messagebox.showerror('Error', 'La matrícula ya existe en la base de datos.')

# Función para verificar si un vehículo ya existe en la base de datos
def vehiculo_existe(matricula):
    vehiculos = db['Vehiculos']
    vehiculo = vehiculos.find_one({"matricula": matricula})
    return vehiculo is not None

# Función para agregar un nuevo mantenimiento
def agregar_mantenimiento(matricula, fecha, descripcion, costo):
    mantenimientos = db['Mantenimiento']
    mantenimiento = {
        "matricula": matricula,
        "fecha": fecha,
        "descripcion": descripcion,
        "costo": costo
    }
    mantenimientos.insert_one(mantenimiento)
    messagebox.showinfo('Éxito', 'Mantenimiento registrado correctamente.')
    # Limpiar los campos de entrada después de agregar el mantenimiento
    entry_matricula_mant.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_costo.delete(0, tk.END)

# Función para buscar mantenimientos por matrícula
def buscar_mantenimientos():
    matricula = entry_matricula_buscar.get()

    if matricula:
        mantenimientos = db['Mantenimiento']
        resultados = mantenimientos.find({"matricula": matricula})

        mensaje = f'Mantenimientos para la matrícula {matricula}: \n'
        for mantenimiento in resultados:
            mensaje += f'Fecha: {mantenimiento["fecha"]}, Descripción: {mantenimiento["descripcion"]}, Costo: {mantenimiento["costo"]}\n'
        if mensaje == f'Mantenimientos para la matrícula {matricula}: \n':
            mensaje = f'No se encontraron mantenimientos para la matrícula {matricula}'
        messagebox.showinfo('Mantenimientos', mensaje)
        
        # Limpiar el campo de entrada después de la búsqueda
        entry_matricula_buscar.delete(0, tk.END)
    else:
        messagebox.showerror('Error', 'Ingrese una matrícula para buscar los mantenimientos.')

# Crear la ventana de inicio de sesión
ventana_login = tk.Tk()
ventana_login.title('Inicio de Sesión')
ventana_login.configure(bg="light blue")

tk.Label(ventana_login, text='Usuario:', bg="light blue").grid(row=0, column=0)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.grid(row=0, column=1)

tk.Label(ventana_login, text='Contraseña:', bg="light blue").grid(row=1, column=0)
entry_contraseña = tk.Entry(ventana_login, show="*")
entry_contraseña.grid(row=1, column=1)

btn_ingresar = tk.Button(ventana_login, text='Ingresar', bg="blue", fg="white", command=verificar_admin)
btn_ingresar.grid(row=2, columnspan=2)

# Función para abrir la ventana principal
def abrir_ventana_principal():
    global entry_matricula_buscar, entry_matricula, entry_marca, entry_modelo, entry_matricula_mant, entry_fecha, entry_descripcion, entry_costo
    
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Gestión de Vehículos')
    root.configure(bg="light blue")  # Cambiar el color de fondo de la ventana principal

    # Crear y posicionar los widgets para agregar vehículo
    tk.Label(root, text='Matrícula:', bg="light blue").grid(row=0, column=0)
    entry_matricula = tk.Entry(root)
    entry_matricula.grid(row=0, column=1)

    tk.Label(root, text='Marca:', bg="light blue").grid(row=1, column=0)
    entry_marca = tk.Entry(root)
    entry_marca.grid(row=1, column=1)

    tk.Label(root, text='Modelo:', bg="light blue").grid(row=2, column=0)
    entry_modelo = tk.Entry(root)
    entry_modelo.grid(row=2, column=1)

    btn_agregar_vehiculo = tk.Button(root, text='Agregar Vehículo', bg="blue", fg="white", command=lambda: agregar_vehiculo(entry_matricula.get(), entry_marca.get(), entry_modelo.get()))
    btn_agregar_vehiculo.grid(row=3, columnspan=2)

    # Crear y posicionar los widgets para agregar mantenimiento
    tk.Label(root, text='Matrícula:', bg="light blue").grid(row=4, column=0)
    entry_matricula_mant = tk.Entry(root)
    entry_matricula_mant.grid(row=4, column=1)

    tk.Label(root, text='Fecha (YYYY-MM-DD):', bg="light blue").grid(row=5, column=0)
    entry_fecha = tk.Entry(root)
    entry_fecha.grid(row=5, column=1)

    tk.Label(root, text='Descripción:', bg="light blue").grid(row=6, column=0)
    entry_descripcion = tk.Entry(root)
    entry_descripcion.grid(row=6, column=1)

    tk.Label(root, text='Costo:', bg="light blue").grid(row=7, column=0)
    entry_costo = tk.Entry(root)
    entry_costo.grid(row=7, column=1)

    btn_agregar_mantenimiento = tk.Button(root, text='Agregar Mantenimiento', bg="blue", fg="white", command=lambda: agregar_mantenimiento(entry_matricula_mant.get(), entry_fecha.get(), entry_descripcion.get(), entry_costo.get()))
    btn_agregar_mantenimiento.grid(row=8, columnspan=2)

    # Crear y posicionar los widgets para buscar mantenimientos
    tk.Label(root, text='Buscar Mantenimientos por Matrícula:', bg="light blue").grid(row=9, column=0)
    entry_matricula_buscar = tk.Entry(root)
    entry_matricula_buscar.grid(row=9, column=1)

    btn_buscar_mantenimientos = tk.Button(root, text='Buscar Mantenimientos', bg="blue", fg="white", command=buscar_mantenimientos)
    btn_buscar_mantenimientos.grid(row=10, columnspan=2)

    # Iniciar el bucle de eventos de la ventana principal
    root.mainloop()

# Iniciar el bucle de eventos de la ventana de inicio de sesión
ventana_login.mainloop()




