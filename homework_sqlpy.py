import psycopg2


def remove_junk():
    cur.execute('''
        DROP TABLE phones;
        DROP TABLE clients;
        ''')


def create_table():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(50) UNIQUE
    );
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id),
        phone_number VARCHAR(50)
    );
    ''')
    conn.commit()


def add_client(first_name, last_name, email):
    cur.execute('''
    INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s)
    ''', (first_name, last_name, email))
    conn.commit()


def add_phone(client_id, phone_number):
    cur.execute('INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)', (client_id, phone_number))
    conn.commit()


def update_client(client_id, first_name=None, last_name=None, email=None):
    if first_name:
        cur.execute('UPDATE clients SET first_name = %s WHERE id = %s', (first_name, client_id))
    if last_name:
        cur.execute('UPDATE clients SET last_name = %s WHERE id = %s', (last_name, client_id))
    if email:
        cur.execute('UPDATE clients SET email = %s WHERE id = %s', (email, client_id))
    conn.commit()


def delete_phone(phone_id):
    cur.execute('DELETE FROM phones WHERE id = %s', (phone_id,))
    conn.commit()


def delete_client(client_id):
    cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
    conn.commit()


def find_client(first_name=None, last_name=None, email=None, phone_number=None):
    if first_name:
        cur.execute('''SELECT * FROM clients WHERE first_name = %s
        ''', (first_name,))
    elif last_name:
        cur.execute('''
        SELECT * FROM clients WHERE last_name = %s
        ''', (last_name,))
    elif email:
        cur.execute('''
        SELECT * FROM clients WHERE email = %s
        ''', (email,))
    elif phone_number:
        cur.execute('''
        SELECT * FROM clients JOIN phones ON clients.id = phones.client_id WHERE phone_number = %s
        ''', (phone_number,))
    print(cur.fetchall())


password = ''
print('password?')
password = input(password)
with psycopg2.connect(database="homework_sqlpy", user="postgres", password=password) as conn:
    cur = conn.cursor()
    remove_junk()
    create_table()
    add_client('Gennadiy', 'Petrov', 'genp@mail.ru')
    add_phone(1, 8800553535)
    update_client(1, 'Gennadiy', 'Petrov', 'genpet@gmail.com')
    delete_phone(1)
    # delete_client(1)
    find_client(None, None, 'genpet@gmail.com', None)
    cur.close()
conn.close()
