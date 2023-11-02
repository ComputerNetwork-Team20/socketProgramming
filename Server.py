
from socket import *

HOST = "127.0.0.1"
PORT = 12346

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("1. 서버가 대기중입니다")

while(True):
    conn, addr = s.accept()
    print("3. {} has been connected".format(addr))

    data = conn.recv(1024)
    print("5. 받은 데이터 :", data.decode("utf-8"))

    if not data:
        s.send("I am a server".encode("utf-8"))
        break
    conn.sendall("클라이언트야, ".encode("utf-8")+data)













# from socket import *
#
# host = "127.0.0.1"
# port = 12345
#
# serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.bind((host,port))
# serverSocket.listen(1)
# print("대기중입니다")
#
# connectionSocket, addr = serverSocket.accept()
# print(str(addr), "에서 접속되었습니다.")
#
# data = connectionSocket.recv(1024) #데이터 최대 수신 1024
# print("받은 데이터 :", data.decode("utf-8"))
#
#
# connectionSocket.send("I am a server".encode("utf-8"))
# print("메시지를 보냈습니다.")
#
# serverSocket.close()
