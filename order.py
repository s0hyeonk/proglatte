import sqlite3

def connect_db():
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            menu_name TEXT,
            quantity INTEGER,
            price INTEGER,
            order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_order(menu_name, quantity, price):
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (menu_name, quantity, price)
        VALUES (?, ?, ?)
    """, (menu_name, quantity, price))
    conn.commit()
    conn.close()

def get_all_orders():
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT menu_name, quantity, price, order_time FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_orders():
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders")
    conn.commit()
    conn.close()
