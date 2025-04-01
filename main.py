import sqlite3
import logging
from getpass import getpass

logging.basicConfig(
    filename='inventario.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    # init schema
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
                 sku INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 descripcion TEXT,
                 cantidad INTEGER NOT NULL,
                 precio REAL NOT NULL,
                 categoria TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 usuario TEXT PRIMARY KEY,
                 contraseña TEXT NOT NULL)''')
    
    # init user
    c.execute("INSERT OR IGNORE INTO usuarios VALUES ('admin', 'admin')")
    
    conn.commit()
    conn.close()

def auth():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Usuario: ")
    contraseña = getpass("Contraseña: ")

    c.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", 
              (usuario, contraseña))
    resultado = c.fetchone()

    if resultado is not None:
        logger.info(f'Ha iniciado sesión el usuario {usuario}')
    conn.close()
    return resultado is not None


def menu():
    while True:
        print("\n----------------------\n")
        print("1. Registrar usuario")
        print("2. Agregar producto")
        print("3. Ver todos los productos")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Actualizar stock")
        print("7. Buscar productos")
        print("8. Generar reporte")
        print("9. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            add_user()
        elif opcion == '2':
            add_producto()
        elif opcion == '3':
            get_productos()
        elif opcion == '4':
            continue
        elif opcion == '5':
            continue
        elif opcion == '6':
            print("\n-------------------")
            print("1. Ingresar stock")
            print("2. Vender stock")

            opcion = input("\nSeleccione una opción: ")
            if opcion == '1' or opcion == '2':
                update_stock(int(opcion))
            else:
                print("Opción inválida, intente nuevamente.")
                continue
        elif opcion == '7':
            continue
        elif opcion == '8':
            continue
        elif opcion == '9':
            break
        else:
            print("Opción inválida, intente nuevamente.")

# --------------------------------------------------

def add_user():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- REGISTRAR USUARIO ---")
    usuario = input("Nuevo usuario: ")
    contraseña = getpass("Nueva contraseña: ")
    
    c.execute('''INSERT INTO usuarios (usuario, contraseña)
              VALUES (?, ?)''', (usuario, contraseña))
    
    conn.commit()
    conn.close()
    logger.info(f'Se registró el usuario {usuario}')
    print("\nUsuario registrado exitosamente!")

def add_producto():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- AÑADIR PRODUCTO ---")
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    cantidad = int(input("Cantidad disponible: "))
    precio = float(input("Precio unitario: "))
    categoria = input("Categoría: ")
    
    c.execute('''INSERT INTO productos 
              (nombre, descripcion, cantidad, precio, categoria)
              VALUES (?, ?, ?, ?, ?)''',
              (nombre, descripcion, cantidad, precio, categoria))
    
    conn.commit()
    conn.close()
    logger.info(f'Se añadió el producto {nombre} con SKU {c.lastrowid}')
    print("\nProducto agregado exitosamente!")

def get_productos():
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM productos")
    productos = c.fetchall()
    
    print("\n--- PRODUCTOS ---")
    for producto in productos:
        print(f"SKU: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Stock: {producto[3]}")
        print(f"Precio: ${producto[4]}")
        print(f"Categoría: {producto[5]}")
        print("-----------------------")
    
    logger.info(f'Se consultaron los productos')
    conn.close()

def update_stock(type):
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    
    print("\n--- ACTUALIZAR STOCK ---")
    sku = int(input("SKU del producto: "))
    
    if type == 1:
        cantidad = int(input("Cantidad a ingresar: "))
        c.execute('''UPDATE productos SET cantidad = cantidad + ? WHERE sku = ?''', (cantidad, sku))
        log_msg = f'Se añadieron {cantidad} unidades al producto SKU {sku}'

    elif type == 2:
        cantidad = int(input("Cantidad a vender: "))
        c.execute('''UPDATE productos SET cantidad = cantidad - ? WHERE sku = ?''', (cantidad, sku))
        log_msg = f'Se vendieron {cantidad} unidades del producto SKU {sku}'

    conn.commit()
    conn.close()
    logger.info(log_msg)
    print("\nStock actualizado!")

if __name__ == "__main__":
    logging.basicConfig(filename='inventario.log', level=logging.INFO)
    init_db()
    
    if auth():
        menu()
    else:
        print("\nUsuario o contraseña incorrectos.")