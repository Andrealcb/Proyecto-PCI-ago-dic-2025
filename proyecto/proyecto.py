import sqlite3
import os
from datetime import datetime
import csv
rango=None
nombre_usuario=None
reporte_ventas = []

def limpiar():
    os.system('cls')
    
def crear_tabla():
    conexion = sqlite3.connect("producto.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT NOT NULL UNIQUE,
            precio_unitario REAL NOT NULL,
            cantidad_stock INTEGER NOT NULL
        )
    ''')
    print("Tabla creada")
    conexion.commit()
    conexion.close()

def crear_tabla_empleados():
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Usuario TEXT NOT NULL,
            Contraseña TEXT NOT NULL
        )
    ''')
    print("Tabla creada")
    conexion.commit()
    conexion.close()

def crear_tabla_gerentes():
    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gerentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Usuario TEXT NOT NULL,
            Contraseña TEXT NOT NULL
        )
    ''')
    print("Tabla creada")
    conexion.commit()
    conexion.close()

def crear_tabla_administrador():
    conexion = sqlite3.connect("administrador.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administrador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Usuario TEXT NOT NULL,
            Contraseña TEXT NOT NULL
        )
    ''')
    print("Tabla creada")
    conexion.commit()
    conexion.close()

def crear_tabla_ventas():
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT,
            cantidad INTEGER,
            precio_unitario REAL,
            total REAL,
            vendedor TEXT,
            rango TEXT,
            fecha_hora TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def agregar_producto():
    limpiar()
    nombre = input("Ingrese el nombre del producto: ")
    codigo = input("Ingrese el código del producto: ")
    precio_unitario = float(input("Ingrese el precio unitario del producto: "))
    cantidad_stock = int(input("Ingrese la cantidad en stock del producto: "))
    
    
    conexion = sqlite3.connect("producto.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO producto (nombre, codigo, precio_unitario, cantidad_stock) VALUES (?, ?, ?, ?)", 
                       (nombre, codigo, precio_unitario, cantidad_stock))
        conexion.commit()
        print("Producto agregado exitosamente.")
    except sqlite3.IntegrityError:
        print("El codigo ingresado ya existe. Intente nuevamente con un codigo unico.")
    finally:
        conexion.close()

def agregar_gerente():
    limpiar()
    nombre = input("Ingrese el nombre de usuario(gerente): ")
    contraseña = input("Ingrese contraseña: ")
    
    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO gerentes (nombre, contraseña) VALUES (?, ?)", 
                       (nombre, contraseña))
        conexion.commit()
        print("Usuario guardado exitosamente.")
    except sqlite3.IntegrityError:
        print("No se pudo guardar, intentalo de nuevo.")
    finally:
        conexion.close()

def agregar_empleado():
    limpiar()
    nombre = input("Ingrese el nombre de usuario(empleado): ")
    contraseña = input("Ingrese contraseña: ")
    
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO empleados (nombre, contraseña) VALUES (?, ?)", 
                       (nombre, contraseña))
        conexion.commit()
        print("Usuario guardado exitosamente.")
    except sqlite3.IntegrityError:
        print("No se pudo guardar, intentalo de nuevo.")
    finally:
        conexion.close()

def buscar_producto(codigo):
    limpiar()
    conexion = sqlite3.connect("producto.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM producto WHERE codigo = ?", (codigo,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

def buscar_gerente(Usuario):
    limpiar()
    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM gerentes WHERE Usuario = ?", (Usuario,))
    gerentes = cursor.fetchone()
    conexion.close()
    return gerentes

def buscar_empleado(Usuario):
    limpiar()
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM emples WHERE Usuario = ?", (Usuario,))
    empleados = cursor.fetchone()
    conexion.close()
    return empleados

def modificar_producto(codigo):
    limpiar()
    conexion = sqlite3.connect("producto.db")
    cursor = conexion.cursor()
    producto = buscar_producto(codigo)
    
    if producto:
        print(f"Producto encontrado: Nombre: {producto[1]}, Código: {producto[2]}, Precio Unitario: {producto[3]}, Cantidad en stock: {producto[4]}")
        print("Ingrese los nuevos datos del producto:")
        nombre = input("Nuevo nombre del producto (enter para dejar sin cambios): ")
        precio_unitario = input("Nuevo precio unitario del producto (enter para dejar sin cambios): ")
        cantidad_stock = input("Nueva cantidad en stock del producto (enter para dejar sin cambios): ")
        
        if nombre:
            cursor.execute("UPDATE producto SET nombre = ? WHERE codigo = ?", (nombre, codigo))
        if precio_unitario:
            cursor.execute("UPDATE producto SET precio_unitario = ? WHERE codigo = ?", (float(precio_unitario), codigo))
        if cantidad_stock:
            cursor.execute("UPDATE producto SET cantidad_stock = ? WHERE codigo = ?", (int(cantidad_stock), codigo))
        
        conexion.commit()
        print("Producto modificado correctamente.")
    else:
        print("Producto no encontrado.")
    
    conexion.close()

def modificar_gerente(Usuario):
    limpiar()
    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    gerentes = buscar_gerente(Usuario)
    
    if gerentes:
        print(f"Usuario encontrado: Usuario: {gerentes[1]}, Contraseña: {gerentes[2]}")
        print("Ingrese los nuevos datos del usuario:")
        Usuario = input("Nuevo nombre de usuario (enter para dejar sin cambios): ")
        Contraseña = input("Nueva contraseña (enter para dejar sin cambios): ")
        
        if Usuario:
            cursor.execute("UPDATE gerentes SET Usuario = ? WHERE Usuario = ?", (Usuario, Usuario))
        if Contraseña:
            cursor.execute("UPDATE gerentes SET precio_unitario = ? WHERE codigo = ?", (Contraseña, Usuario))
        
        conexion.commit()
        print("Usuario modificado exitosamente.")
    else:
        print("Usuario encontrado.")
    
    conexion.close()

def modificar_empleado(Usuario):
    limpiar()
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    empleados = buscar_empleado(Usuario)
    
    if empleados:
        print(f"Usuario encontrado: Usuario: {empleados[1]}, Contraseña: {empleados[2]}")
        print("Ingrese los nuevos datos del usuario:")
        Usuario = input("Nuevo nombre de usuario (enter para dejar sin cambios): ")
        Contraseña = input("Nueva contraseña (enter para dejar sin cambios): ")
        
        if Usuario:
            cursor.execute("UPDATE empleados SET Usuario = ? WHERE Usuario = ?", (Usuario, Usuario))
        if Contraseña:
            cursor.execute("UPDATE empleados SET precio_unitario = ? WHERE codigo = ?", (Contraseña, Usuario))
        
        conexion.commit()
        print("Usuario modificado exitosamente.")
    else:
        print("Usuario encontrado.")
    
    conexion.close()

def eliminar_producto(codigo):
    limpiar()
    conexion = sqlite3.connect("producto.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM producto WHERE codigo = ?", (codigo,))
    if cursor.rowcount > 0:
        print("Producto eliminado correctamente.")
    else:
        print("No se encontró ningún producto con ese código.")
    conexion.commit()
    conexion.close()

def eliminar_gerente(Usuario):
    limpiar()
    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM gerentes WHERE Usuario = ?", (Usuario,))
    if cursor.rowcount > 0:
        print("Usuario eliminado correctamente.")
    else:
        print("No se encontró ningún Usuario.")
    conexion.commit()
    conexion.close()

def eliminar_empleado(Usuario):
    limpiar()
    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM emplados WHERE Usuario = ?", (Usuario,))
    if cursor.rowcount > 0:
        print("Usuario eliminado correctamente.")
    else:
        print("No se encontró ningún Usuario.")
    conexion.commit()
    conexion.close()

def vender_producto(nombre_usuario="Desconocido", rango="Desconocido"):
    from datetime import datetime
    limpiar()
    productos_a_vender = []
    while True:
        codigo = input("Ingrese el código del producto que desea vender (o 'fin' para terminar): ")
        if codigo.lower() == 'fin':
            break
        producto = buscar_producto(codigo)
        if producto:
            print(f"Producto encontrado: Nombre: {producto[1]}, Código: {producto[2]}, Precio Unitario: {producto[3]}, Cantidad en stock: {producto[4]}")
            cantidad_a_vender = int(input("Ingrese la cantidad a vender: "))
            if producto[4] >= cantidad_a_vender:
                productos_a_vender.append((producto, cantidad_a_vender))
            else:
                print("No hay suficiente stock para realizar la venta.")
        else:
            print("Producto no encontrado.")

    if productos_a_vender:
        total_venta = sum(p[1] * p[0][3] for p in productos_a_vender)
        print(f"Total a pagar: ${total_venta:.2f}")
        pago = float(input("Ingrese el monto con el que paga: $"))
        while pago < total_venta:
            print("Monto insuficiente. Por favor, ingrese un monto válido.")
            pago = float(input("Ingrese el monto con el que paga: $"))
        cambio = pago - total_venta
        
        conexion = sqlite3.connect("producto.db")
        cursor = conexion.cursor()
        for producto, cantidad_a_vender in productos_a_vender:
            nueva_cantidad_stock = producto[4] - cantidad_a_vender
            cursor.execute("UPDATE producto SET cantidad_stock = ? WHERE codigo = ?", (nueva_cantidad_stock, producto[2]))
        conexion.commit()
        conexion.close()
        
        print(f"Venta realizada con éxito. Cambio: ${cambio:.2f}")
        imprimir_ticket(productos_a_vender, total_venta, pago, cambio)

        registrar_venta(productos_a_vender, total_venta, nombre_usuario, rango)


def registrar_venta(productos_a_vender, total_venta, usuario, rango):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()

    for producto, cantidad_vendida in productos_a_vender:
        total_producto = producto[3] * cantidad_vendida

        cursor.execute("""
            INSERT INTO ventas (producto, cantidad, precio_unitario, total, vendedor, rango, fecha_hora)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (producto[1], cantidad_vendida, producto[3], total_producto, usuario, rango, fecha_hora))

        venta = [
            producto[1],       
            cantidad_vendida,   
            producto[3],        
            total_producto,     
            usuario,            
            rango,              
            fecha_hora         
        ]
        reporte_ventas.append(venta)

    conexion.commit()
    conexion.close()



def mostrar_reporte_ventas(fecha_inicio, fecha_fin):
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT producto, cantidad, precio_unitario, total, vendedor, rango, fecha_hora
        FROM ventas
        WHERE fecha_hora BETWEEN ? AND ?
        ORDER BY fecha_hora ASC
    """, (fecha_inicio + " 00:00:00", fecha_fin + " 23:59:59"))

    ventas = cursor.fetchall()
    conexion.close()

    print("\n--- REPORTE DE VENTAS ---")
    print(f"{'Fecha/Hora':<20} {'Producto':<15} {'Cant':<6} {'P.Unit':<8} {'Total':<8} {'Vendedor':<15} {'Rango':<10}")
    print("="*85)

    for v in ventas:
        print(f"{v[6]:<20} {v[0]:<15} {v[1]:<6} {v[2]:<8.2f} {v[3]:<8.2f} {v[4]:<15} {v[5]:<10}")



def imprimir_ticket(productos_a_vender, total_venta, pago, cambio):
    limpiar()
    tienda = "Nombre de la Tienda"
    direccion = "Septima avenida sur poniente no.64, Barrio Guadalupe"
    telefono = "9191123208"

    print("\n--- Ticket de Compra ---")
    print(tienda)
    print(direccion)
    print(f"Tel: {telefono}")
    print("------------------------")
    for producto, cantidad_vendida in productos_a_vender:
        print(f"Producto: {producto[1]}")  
        print(f"Codigo: {producto[2]}")
        print(f"Cantidad vendida: {cantidad_vendida}")
        print(f"Precio unitario: ${producto[3]:.2f}")
        print("------------------------")
    print(f"Total de la venta: ${total_venta:.2f}")
    print(f"Pago recibido: ${pago:.2f}")
    print(f"Cambio: ${cambio:.2f}")
    print("------------------------")
    print("Gracias por su compra.")
    print("------------------------\n")

def mostrar_productos():
   
    conexion = sqlite3.connect("producto.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, codigo, precio_unitario, cantidad_stock FROM producto")
    productos = cursor.fetchall()
    conexion.close()
    
    if productos:
        encabezados = ["Nombre", "Código", "Precio Unitario", "Cantidad en Stock"]
        print(f"{encabezados[0]:<20} {encabezados[1]:<15} {encabezados[2]:<15} {encabezados[3]:<15}")
        print("="*70)
        for producto in productos:
            print(f"{producto[0]:<20} {producto[1]:<15} {producto[2]:<15} {producto[3]:<15}")
    else:
        print("No hay productos registrados.")

def obtener_lista_usuarios():
    conexion_g = sqlite3.connect("gerentes.db")
    cursor_g = conexion_g.cursor()
    cursor_g.execute("SELECT Usuario, Contraseña FROM gerentes")
    gerentes = cursor_g.fetchall()
    conexion_g.close()
    
    conexion_e = sqlite3.connect("empleados.db")
    cursor_e = conexion_e.cursor()
    cursor_e.execute("SELECT Usuario, Contraseña FROM empleados")
    empleados = cursor_e.fetchall()
    conexion_e.close()

    
    usuarios_combinados = [["Tipo", "Usuario", "Contraseña"]]
    for g in gerentes:
        usuarios_combinados.append(["Gerente", g[0], g[1]])
    for e in empleados:
        usuarios_combinados.append(["Empleado", e[0], e[1]])

    return usuarios_combinados


def mostrar_usuarios_combinados():
    usuarios = obtener_lista_usuarios()
    print("\n--- LISTA DE USUARIOS (GERENTES Y EMPLEADOS) ---")
    print(f"{'Tipo':<10} {'Usuario':<20} {'Contraseña':<20}")
    print("=" * 55)
    for fila in usuarios[1:]:
        print(f"{fila[0]:<10} {fila[1]:<20} {fila[2]:<20}")

def menu_administradordueño(nombre_usuario, rango):
    limpiar()
    crear_tabla()
    
    while True:
        print("Por ahora solo funciona hasta la opcion 8")
        print("\nSeleccione una opción:")
        print("1. Agregar producto")
        print("2. Buscar producto por código:")
        print("3. Modificar producto")
        print("4. Eliminar producto")
        print("5. Vender producto")
        print("6. Mostrar productos")
        print("7. Mostrar todos los usuarios (gerentes y empleados)")
        print("8. Reporte de ventas")
        print("9. Agregar gerentes o empleados")
        print("10. Modificar gerentes o empleados")
        print("11. Eliminar empleados o gerentes")
        print("13. Salir (por ahora pon 9)")

        opcion = input("Opción: ")
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            codigo = input("Ingrese el código del producto que desea buscar: ")
            producto = buscar_producto(codigo)
            if producto:
                print(f"Producto encontrado: Nombre: {producto[1]}, Código: {producto[2]}, Precio Unitario: {producto[3]}, Cantidad en stock: {producto[4]}")
            else:
                print("Producto no encontrado.")
        elif opcion == "3":
            codigo = input("Ingrese el código del producto que desea modificar: ")
            modificar_producto(codigo)
        elif opcion == "4":
            codigo = input("Ingrese el código del producto que desea eliminar: ")
            eliminar_producto(codigo)
        elif opcion == "5":
            vender_producto(nombre_usuario, rango)
        elif opcion == "6":
            codigo= print("Productos")
            mostrar_productos()
        elif opcion == "7":
            mostrar_usuarios_combinados()
        elif opcion == "8":
            fecha_inicio = input("Ingrese fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese fecha final (YYYY-MM-DD): ")
            mostrar_reporte_ventas(fecha_inicio, fecha_fin) 
        elif opcion == "9":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente nuevamente.")

def menu_gerente():
    limpiar()
    crear_tabla()
    
    while True:
        
        print("\nSeleccione una opción:")
        print("1. Agregar producto")
        print("2. Buscar producto por código:")
        print("3. Modificar producto")
        print("4. Eliminar producto")
        print("5. Vender producto")
        print("6. Mostrar productos")
        print("7. Administrar empleados")
        print("8. Salir")

        opcion = input("Opción: ")
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            codigo = input("Ingrese el código del producto que desea buscar: ")
            producto = buscar_producto(codigo)
            if producto:
                print(f"Producto encontrado: Nombre: {producto[1]}, Código: {producto[2]}, Precio Unitario: {producto[3]}, Cantidad en stock: {producto[4]}")
            else:
                print("Producto no encontrado.")
        elif opcion == "3":
            codigo = input("Ingrese el código del producto que desea modificar: ")
            modificar_producto(codigo)
        elif opcion == "4":
            codigo = input("Ingrese el código del producto que desea eliminar: ")
            eliminar_producto(codigo)
        elif opcion == "5":
            vender_producto(nombre_usuario, rango)
        elif opcion == "6":
            codigo= print("Productos")
            mostrar_productos()
        elif opcion == "7":
            mostrar_usuarios_combinados()
        elif opcion == "8":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente nuevamente.")



def menu_empleados():
    
    crear_tabla()
    limpiar()
    while True:
        
        print("\nSeleccione una opción:")
        print("1. Buscar producto por código:")
        print("2. Vender producto")
        print("3. Mostrar productos")
        print("4. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            codigo = input("Ingrese el código del producto que desea buscar: ")
            producto = buscar_producto(codigo)
            if producto:
                print(f"Producto encontrado: Nombre: {producto[1]}, Código: {producto[2]}, Precio Unitario: {producto[3]}, Cantidad en stock: {producto[4]}")
            else:
                print("Producto no encontrado.")
        elif opcion == "2":
            vender_producto(nombre_usuario, rango)
        elif opcion == "3":
            codigo= print("Productos")
            mostrar_productos()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente nuevamente.")

def si_administrador():
    print("\nIngrese usuario y contraseña:")
    Usuario = input("Usuario: ")
    Contraseña = input("Contraseña: ")

    conexion = sqlite3.connect("administrador.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM administrador WHERE Usuario = ? AND Contraseña = ?", (Usuario, Contraseña))
    administrador = cursor.fetchone()
    conexion.close()
    return administrador

def si_gerentes():
    print("\nIngrese usuario y contraseña:")
    Usuario = input("Usuario: ")
    Contraseña = input("Contraseña: ")

    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM gerentes WHERE Usuario = ? AND Contraseña = ?", (Usuario, Contraseña))
    gerente = cursor.fetchone()
    conexion.close()
    return gerente

def si_empleados():
    print("\nIngrese usuario y contraseña:")
    Usuario = input("Usuario: ")
    Contraseña = input("Contraseña: ")

    conexion = sqlite3.connect("empleados.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados WHERE Usuario = ? AND Contraseña = ?", (Usuario, Contraseña))
    empleado = cursor.fetchone()
    conexion.close()
    return empleado

def administrador_no():
    print("\nCree un usuario y contraseña para administrador:")
    UsuarioD = input("Usuario: ")
    ContraseñaD = input("Contraseña: ")

    conexion = sqlite3.connect("administrador.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO administrador (Usuario, Contraseña) VALUES (?, ?)", (UsuarioD, ContraseñaD))
        conexion.commit()
        print("Su usuario y contraseña se ha guardado exitosamente.")
    except sqlite3.IntegrityError:
        print("Error al guardar usuario y contraseña, intente de nuevo.")
    finally:
        conexion.close()
    main()

def main():
    crear_tabla_gerentes()
    crear_tabla_empleados()
    crear_tabla_administrador()
    crear_tabla_ventas()
    limpiar()

    conexion = sqlite3.connect("administrador.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM administrador")
    hay_administrador = cursor.fetchall()
    conexion.close()

    if not hay_administrador:
        administrador_no()
        return

    print("\nSeleccione su tipo de usuario:")
    print("1. Administrador")
    print("2. Gerente")
    print("3. Empleado")
    tipo = input("Opción: ")

    if tipo == "1":
        usuario = si_administrador()
        if usuario:
            nombre_usuario = usuario[1]
            rango = "Administrador"
            menu_administradordueño(nombre_usuario, rango)
        else:
            print("Usuario o contraseña incorrectos.")
    elif tipo == "2":
        gerente = si_gerentes()
        if gerente:
            nombre_usuario = gerente[1]
            rango = "Gerente"
            menu_gerente(nombre_usuario, rango)
        else:
            print("Usuario o contraseña incorrectos.")
    elif tipo == "3":
        empleado = si_empleados()
        if empleado:
            nombre_usuario = empleado[1]
            rango = "Empleado"
            menu_empleados(nombre_usuario, rango)
        else:
            print("Usuario o contraseña incorrectos.")
    else:
        print("Opcion no valida.")


if __name__ == "__main__":
    main()

    