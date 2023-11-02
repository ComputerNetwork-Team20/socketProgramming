
from socket import *

HOST = "127.0.0.1"
PORT = 12346

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

print("2. 서버와의 연결이 확인됐습니다.")

input_data = input("서버에 보낼 데이터를 입력해 주세요: ")

#s.send("I am a client".encode("utf-8"))
s.send(input_data.encode("utf-8"))
print("4. 메시지를 전송했습니다.")

data = s.recv(1024)
print("6. Response: {}".format(data.decode("utf-8")))










# # tcpclient.py
# from socket import *
#
# ip = "127.0.0.1"
# port = 12345
#
#
# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((ip,port))
#
# print("연결 확인됐습니다.")
# clientSocket.send("I am a client".encode("utf-8"))
#
# print("메시지를 전송했습니다.")
# data = clientSocket.recv(1024)
#
#
# print("받은 데이터 : ", data.decode("utf-8"))
# clientSocket.close() #연결 종료
