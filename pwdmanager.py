import random
import os
import psycopg2

small_alphabets = "abcdefghijklmnopqrstuvwxyz"
cap_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
symbols = "!@#%&"

universal_set = list(small_alphabets) + list(cap_alphabets) + list(numbers) + list(symbols)

def pwdgen(length=12, set=universal_set):
    password = ''
    for i in range(int(length)):
        x = random.choice(set)
        password += x
        
    return password


conn = psycopg2.connect(
    host = os.environ["DATABASE_HOST"],
    database = os.environ["DATABASE"],
    user = os.environ["DATABASE_USER"],
    password = os.environ["DATABASE_PASSWORD"]
)



def insert(user_id, pwd, info, username, saved_at):
    cur = conn.cursor()
    cur.execute(f"insert into saved_passwords (chat_id, password, info, username, saved_at) values ({user_id}, '{pwd}', '{info}', '{username}', '{saved_at}')")
    conn.commit()
    cur.close()


def read_all(user_id):
    cur = conn.cursor()
    cur.execute(f"select * from saved_passwords where chat_id={user_id}")
    rows = cur.fetchall()
    cur.close()
    
    return rows


def search(user_id, to_srch):
    cur = conn.cursor()
    cur.execute(f"select * from saved_passwords where chat_id={user_id}")
    rows = cur.fetchall()
    srch_rows = []
    for row in rows:
        if to_srch.lower() in row[2].lower():
            srch_rows.append(row)
    cur.close()
    
    return srch_rows
