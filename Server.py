

from socket import *
from _thread import *
import random

# word = list(word) 0
# correct = list(bool) 1
# p______


# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def threaded(client_socket, addr, word):
    # addr = host + port
    print('>> Connected by :', addr[0], ':', addr[1])

    while True: # 클라이언트가 접속을 끊을 때 까지 반복합니다.
        try:
            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data: #데이터가 없으면 disconnection
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            result = func(word, data) #string, char

            print('>> Received from ' + addr[0], ':', addr[1], data.decode()) #client로 부터 받은 데이터 보여주기

            # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
            for client in client_sockets :
                if client != client_socket :
                    client.send(data)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets :
        client_sockets.remove(client_socket)
        print('remove client list : ',len(client_sockets))



    client_socket.close()


def checkParticipant(len):
    if(len == 2):
        print("참가자 수: ", 2)
        return True
    else:
        return False

def randomWords():
    words = ['physical', 'datalink', 'network', 'transport', 'applicaion',
             'bit', 'frame', 'datagram', 'segment', 'message',
             'socket', 'thread', 'server', 'client', 'programming']
    return words[random.randrange(0, 16)]


if __name__ == '__main__':
    client_sockets = [] # 서버에 접속한 클라이언트 목록


    # 서버 IP 및 열어줄 포트
    HOST = '127.0.0.1'
    PORT = 9999

    # 서버 소켓 생성
    print('>> Server Start')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    try:
        while True:
            print('>> Wait')

            # connection 체크
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)



            # 참가자 수 확인 2가 맞으면 게임 실행
            if(checkParticipant(len(client_socket))):
                # 각 client의 thread 생성 # TODO 문구 확인하기
                word = randomWords();
                start_new_thread(threaded, (client_socket, addr, word))


                ###
                # 게임 실행되는 중!!!!#
                ###


            else:
                raise Exception('2명만 참가해야 게임을 시작할 수 있습니다.')


    except Exception as e:
        print('에러는? : ', e)
    finally:
        server_socket.close()





###################################################################################################################333333

# from socket import *
#
# HOST = "127.0.0.1"
# PORT = 12346
#
# s = socket(AF_INET, SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# print("1. 서버가 대기중입니다")
#
# while(True):
#     conn, addr = s.accept()
#     print("3. {} has been connected".format(addr))
#
#
#     data = conn.recv(1024)
#     print("5. 받은 데이터 :", data.decode("utf-8"))
#
#     if not data:
#         s.send("I am a server".encode("utf-8"))
#         break
#     conn.sendall("클라이언트야, ".encode("utf-8")+data)



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
