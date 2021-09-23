import random
import os
import psycopg2
import re

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


try:
    database_url = os.environ.get('DATA_BASE_URL')
except:
    database_url = os.environ.get('DATABASE_URL')

user = re.search('//(.*):', database_url).group(1).split(':')[0].strip()
pwd = re.search(':(.*)@', database_url).group(1).split(':')[1].strip()
host = re.search('@(.*):', database_url).group(1).strip()
database = re.search(r'\d\d\d\d/(.*)', database_url).group(1).strip()

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=pwd
)


def create_table():
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS saved_passwords (
        chat_id VARCHAR(255)
        pwd VARCHAR(255)
        info VARCHAR(255)
        username VARCHAR(255)
        saved_at VARCHAR(255)
    )
    """)
    conn.commit()
    cur.close()


def insert(user_id, pwd, info, username, saved_at):
    cur = conn.cursor()
    cur.execute(
        f"insert into saved_passwords (chat_id, pwd, info, username, saved_at) values ({user_id}, '{pwd}', '{info}', '{username}', '{saved_at}')")
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
