import sqlite3
import base64
import binascii

try:
    conn = sqlite3.connect('grafana.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print("Erro ao abrir o banco de dados:", e)
    exit()

try:
    hash_file = open('hashes.txt', 'w')
except IOError as e:
    print("Erro ao criar o arquivo hashes.txt:", e)
    exit()

try:
    cursor.execute("SELECT email, password, salt, is_admin FROM user")
    rows = cursor.fetchall()
except sqlite3.Error as e:
    print("Erro ao consultar os usuários:", e)
    exit()

# Iterar sobre os resultados da consulta
for row in rows:
    email, password, salt, is_admin = row

    try:
        decoded_hash = bytes.fromhex(password)
        hash_64 = base64.b64encode(decoded_hash).decode('utf-8')
        salt_64 = base64.b64encode(salt.encode('utf-8')).decode('utf-8')
        hash_file.write("sha256:10000:" + salt_64 + ":" + hash_64 + "\n")
    except (binascii.Error, IOError) as e:
        print("Erro ao processar senha:", e)
        exit()

hash_file.close()
conn.close()

print("Hashes gerados com sucesso!")
