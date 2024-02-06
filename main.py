import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE IF EXISTS clients;
                    DROP TABLE IF EXISTS phones;
                    """)
        
        cur.execute("""CREATE TABLE IF NOT EXISTS clients(
                    client_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(40) NOT NULL,
                    email VARCHAR(40) NOT NULL UNIQUE
                    );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS phones(
                    phone_id SERIAL PRIMARY KEY,
                    phone VARCHAR(40),
                    client_id INTEGER REFERENCES clients(client_id)
                    );""")
   

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO clients (first_name, last_name, email) 
                    VALUES (%s, %s, %s) RETURNING client_id, first_name, last_name, email;""", (first_name, last_name, email))
        print(f'client_added: {cur.fetchall()}')


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phones (client_id, phone) VALUES (%s, %s)""", (client_id, phone))
        print(f'phone_added')


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("""UPDATE clients SET first_name=%s WHERE client_id=%s""", (first_name, client_id))
        if last_name:
            cur.execute("""UPDATE clients SET last_name=%s WHERE client_id=%s""", (last_name, client_id))
        if email:
            cur.execute("""UPDATE clients SET email=%s WHERE client_id=%s""", (email, client_id))
        if phone:
            cur.execute("""UPDATE phones SET phone=%s WHERE client_id=%s""", (phone, client_id))
        cur.execute("""SELECT * FROM clients;""")
        print(f'client_changed')


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE client_id=%s AND phone=%s""", (client_id, phone))
        cur.execute("""SELECT * FROM phones;""")
        print(f'phone_deleted')


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE client_id=%s""", (client_id,))
        cur.execute("""DELETE FROM clients WHERE client_id=%s""", (client_id,))
        print(f'client_deleted')


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, email, phone FROM clients AS c
                FULL JOIN phones AS p ON p.client_id = c.client_id
                WHERE (first_name = %s OR last_name = %s OR email = %s OR phone = %s); """, (first_name, last_name, email, phone))
            print(f'find_client {cur.fetchall()}')






if __name__ == "__main__":

    with psycopg2.connect(database="hw_clients_db", user="postgres", password="password") as conn:
        create_db(conn)
        add_client(conn, 'John', 'Doe', '1@example.com')
        add_client(conn, 'Ann', 'Doe', '2@example.com')
        add_client(conn, 'Mike', 'Zhukov', '3@example.com')
        add_client(conn, 'Liza', 'Romanova', '4@example.com')
        add_client(conn, 'Vlad', 'Ivanov', '5@example.com')
        add_client(conn, 'Alex', 'Petrov', '6@example.com')
        add_client(conn, 'Gans', 'Lupin', '7@example.com')
        add_client(conn, 'Lionel', 'Messi', '8@example.com')
        add_phone(conn, 1, '8-800-555-35-35')
        add_phone(conn, 1, '8-800-555-35-36')
        add_phone(conn, 2, '8-800-555-35-12')
        add_phone(conn, 3, '8-800-555-35-13')
        add_phone(conn, 4, '8-800-555-35-14')
        add_phone(conn, 5, '8-800-555-35-15')
        add_phone(conn, 6, '8-800-555-35-16')
        add_phone(conn, 7, '8-800-555-35-17')
        add_phone(conn, 8, '8-800-555-35-18')
        add_phone(conn, 1, '8-800-555-35-19')
        add_phone(conn, 2, '8-800-555-35-20')
        add_phone(conn, 3, '8-800-555-35-21')
        change_client(conn, 1, first_name='Harry', last_name='Potter')
        delete_phone(conn, 1, '8-800-555-35-35')
        delete_client(conn, 1)
        add_phone(conn, 5, '8-800-555-35-77')
        find_client(conn, first_name='Vlad')

             

    conn.close()