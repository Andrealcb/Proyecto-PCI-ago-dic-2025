import sqlite3
import os

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
        print("El código ingresado ya existe. Intente nuevamente con un código único.")
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

def vender_producto():
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
        print(f"Código: {producto[2]}")
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

def menu_gerentes():
    
    crear_tabla()
    limpiar()
    while True:
        
        print("\nSeleccione una opción:")
        print("1. Agregar producto")
        print("2. Buscar producto por código:")
        print("3. Modificar producto")
        print("4. Eliminar producto")
        print("5. Vender producto")
        print("6. Mostrar productos")
        print("7. Salir")
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
            vender_producto()
        elif opcion == "6":
            codigo= print("Productos")
            mostrar_productos()
        elif opcion == "7":
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
            vender_producto()
        elif opcion == "3":
            codigo= print("Productos")
            mostrar_productos()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intente nuevamente.")



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

def no_usuarios():
    print("\nCree un usuario y contraseña para gerente:")
    UsuarioG = input("Usuario: ")
    ContraseñaG = input("Contraseña: ")

    conexion = sqlite3.connect("gerentes.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO gerentes (Usuario, Contraseña) VALUES (?, ?)", (UsuarioG, ContraseñaG))
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

     limpiar()

     conexion = sqlite3.connect("gerentes.db")
     cursor = conexion.cursor()
     cursor.execute("SELECT * FROM gerentes")
     hay_gerentes = cursor.fetchall()
     conexion.close()

     if not hay_gerentes:
        no_usuarios()
        return
     usuario = si_gerentes()
     if usuario:
        menu_gerentes()
     else:
        empleado = si_empleados()
        if empleado:
            menu_empleados()
        else:
            print("Usuario o contraseña incorrectos.")

if __name__ == "__main__":
    main()

    