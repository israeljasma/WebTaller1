import socket
import os
import json

print("Servidor HTTP")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9100))
s.listen(1)

while True:

    client_connection, client_address = s.accept()
    request = client_connection.recv(1024)
    request_lines = request.decode().split("\r\n")
    request_line_0 = request_lines[0]
    items_line_0 = request_line_0.split(" ")
    request_path = items_line_0[1]
    filesystem_path = "./documentRoot/%s" % request_path
    
    #diccionario
    headers = {}
    i=1
    while request_lines[i]:

        primer_header = request_lines[i]
        nombre_header, valor_header = primer_header.split(":", 1)

        headers[nombre_header] = valor_header

        request_echo_header = {}
        request_echo_header["method"] = items_line_0[0]
        request_echo_header["headers"] = headers
        request_echo_json = json.dumps(request_echo_header)
        
        i = i+1

    if os.path.isfile(filesystem_path):

        file = open(filesystem_path, "r")
   
        client_connection.sendall("HTTP/1.1 200 OK\r\n".encode())
        client_connection.sendall("X-RequestEcho: %s\r\n\r\n".encode() % request_echo_json)
        client_connection.sendall("CONTENIDO: \n\r %s\n\r\n\r".encode() % file.read())

        file.close()
    else:
        client_connection.sendall("HTTP/1.1 404 Not Found".encode())

    client_connection.close()