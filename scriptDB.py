import mysql.connector

def create_database():
    # Conexión al servidor MySQL (sin seleccionar base de datos)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""  # XAMPP por defecto
    )
    cursor = conn.cursor()

    # Crear base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS users_db")
    print("Base de datos 'users_db' verificada/creada.")

    cursor.close()
    conn.close()


def create_table():
    # Conexión a la base de datos recién creada
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="users_db"
    )
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            puesto VARCHAR(100),
            antiguedad VARCHAR(100),
            area VARCHAR(100)
        )
    """)
    print("Tabla 'users' verificada/creada.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
    create_table()
    print("Todo listo. Base de datos y tabla creadas correctamente.")
