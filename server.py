# server.py

import socket
import threading
import os
import logger  
import hasher

logger = logger.logger

bufsize = 128000

HOST = '127.0.0.1'
PORT = 10000

def handle_client(conn, addr):

    while True:
        filename = conn.recv(bufsize).decode()
        if filename == 'quit': 
            break

        if os.path.exists(filename):

            filesize = os.path.getsize(filename)
            conn.send(str(filesize).encode())

            with open(filename, 'rb') as f:
                sent = 0
                while sent < filesize:
                    data = f.read(bufsize)
                    hash = hasher.hash_chunk(data)
                    logger.debug(f"Хеш чанка: {hash}")
                    conn.send(data)
                    sent += len(data)

                    logger.debug(f'Отправлено {sent}/{filesize} байт, хеш чанка: {hash}')

        else:
            conn.send("FILE NOT FOUND".encode())
            
    conn.close()
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    logger.info(f'Сервер запущен по адресу {HOST}:{PORT}')
    
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) 
        thread.start()