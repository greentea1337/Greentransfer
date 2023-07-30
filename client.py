import socket
import os
import hasherclient

HOST = '127.0.0.1'  
PORT = 10000

bufsize = 128000

download_folder = "downloads"

if not os.path.exists(download_folder):
  os.mkdir(download_folder)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  while True:
    filename = input("Введите имя файла на сервере: ")
    if not filename:
      break

    s.send(filename.encode())

    try:
      filesize = int(s.recv(bufsize).decode())
      full_path = os.path.join(download_folder, filename)

      bytes_read = 0
      with open(full_path, 'wb') as f:
        while bytes_read < filesize:
          data = s.recv(bufsize)
          if not data:
            break
            
          hash = hasherclient.hash_chunk(data)
          print(f"Получен хеш чанка: {hash}")
            
          f.write(data)
          bytes_read += len(data)

      print(f"Файл {filename} загружен в {download_folder}")

    except ValueError:
      print(f"Файл {filename} не найден на сервере")
    except ConnectionResetError:
      print("Соединение было разорвано, перезапускаем загрузку...")
      continue

print("Клиент закрыт")