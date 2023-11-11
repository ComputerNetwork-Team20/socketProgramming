
import socket
from _thread import *


# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        try:
            data = client_socket.recv(1024) #블로킹 함수
            print("\nfrom server:" + data.decode())

            if(data=="GAME OVER"):
                exit()
        except ConnectionResetError as e:
            # print('>> Disconnected by ' + addr[0], ':', addr[1])
            print('에러는? : ', e)
            client_socket.close()
            break

##############################################################################################
HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 생성
client_socket.connect((HOST, PORT))  # 연결
print('>> Connect Server')

if __name__ == '__main__':
    print('>>> 클라이언트 실행')

    try:
        start_new_thread(recv_data, (client_socket,))

        # 입력 받는 루프
        while (True) :
            message = input('>>> 알파벳 혹은 단어를 입력하세요')  #블락 함수라서 여기서 client
            client_socket.send(message.encode())


    except Exception as e:
        print('에러는? : ', e)
    finally:
        client_socket.close()




# from socket import *
#
# HOST = "127.0.0.1"
# PORT = 12346
#
# s = socket(AF_INET, SOCK_STREAM)
# s.connect((HOST, PORT))
#
# print("2. 서버와의 연결이 확인됐습니다.")
#
# input_data = input("서버에 보낼 데이터를 입력해 주세요: ")
#
# #s.send("I am a client".encode("utf-8"))
# s.send(input_data.encode("utf-8"))
# print("4. 메시지를 전송했습니다.")
#
# data = s.recv(1024)
# print("6. Response: {}".format(data.decode("utf-8")))

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