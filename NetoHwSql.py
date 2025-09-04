import psycopg2

def create_db(cursor):
    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS client(
                 id SERIAL PRIMARY KEY,
                 name VARCHAR(255),
                 email VARCHAR(255) UNIQUE,
                 phone_number VARCHAR(255) UNIQUE
            );
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                phone VARCHAR(255) UNIQUE
            );
            CREATE TABLE IF NOT EXISTS client_phone(
                client_id integer not null references client(id),
                phone_id integer not null references phones(id),
                constraint pk primary key (client_id, phone_id)
            );
             """)
    cursor.commit()

def add_client(cursor, client_id, name, email, phone_id, phone_number=None):
    if phone_number is None:
        cursor.execute(f"""
            INSERT INTO client(name, email, phone_number) 
            VALUES('{name}', '{email}', '{phone_number}'
            );
            """)
    else:
        cursor.execute(f"""
                INSERT INTO client(name, email, phone_number) 
                VALUES('{name}', '{email}', '{phone_number}'
                );
                INSERT INTO phones(phone_id, phone_number)
                VALUES('{phone_number}'
                ); 
                INSERT INTO client_phone(client_id, phone_id)
                VALUES('{client_id}', '{phone_id}'
                );
                """)
    cursor.commit()

def add_phone_number(cursor, client_id, phone_id, phone_number):
    cursor.execute(f"""
                INSERT INTO phones(phone_id, phone_number)
                VALUES('{phone_number}'
                ); 
                INSERT INTO client_phone(client_id, phone_id)
                VALUES('{client_id}', '{phone_id}'
                );
                """)
    cursor.commit()
def change_client(cursor, client_id, name = None, email = None, phone_number = None):
    cursor.execute(f"""
            UPDATE client SET name=%s WHERE id=%s;
        """, (name, client_id))
    cursor.execute(f"""
                UPDATE client SET email=%s WHERE id=%s;
            """, (email, client_id))
    cursor.execute(f"""
                UPDATE client SET phone_number=%s WHERE id=%s;
            """, (phone_number, client_id))
    cursor.commit()

def delete_phone(cursor, phone_number, client_id = None):
    cursor.execute(f"""
        DELETE FROM phones WHERE phone_id=%s;
        """, (phone_number))
    cursor.commit()

def delete_client(cursor, client_id):
    cursor.execute(f"""
        DELETE FROM phones WHERE client_id=%s;
        """, (client_id))
    cursor.commit()

def find_client(cursor, name=None, email=None, phone_number=None):
    cursor.execute(f"""
        SELECT name FROM client WHERE name=%s OR email=%s OR phone_number=%s;
        """, (name, email, phone_number))
    return cursor.fetchone()

with psycopg2.connect(database='netology_db', user='postgres',password='Sambrerra') as conn:
    with conn.cursor() as cur:
        # cur.execute("""
        # DROP TABLE CLIENT;
        # DROP TABLE PHONES;
        # DROP TABLE CLIENT_PHONE;
        # """)
        create_db(cur)
        add_client(cur, 1, 'Dasha', 'Dasha@mail', 1, '+71231231212' )
        add_client(cur, 2, 'NeDasha', 'NeDasha@mail', 2, '+74564564545' )
        add_phone_number(cur, 1, 3, '+75555')
        change_client(cur, 1, 'Dadasha', 'Dasha@mail', 1)
        delete_phone(cur, 3, 1)
        delete_client(cur, 2)
        find_client(cur, 'Dasha')
conn.close()

      
