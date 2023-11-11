from socket import *
from _thread import *
import random

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

def checkChar(answer, data):
    if data in answer:
        return "correct"
    else:
        return "wrong"


def checkWord(answer, data):
    if answer == data:
        return "userwin"
    else:
        return "userlose"


def showBlank(answer, blankWord, data):
    answerList = list(answer)
    blankList = list(blankWord)

    length = len(answer)

    for i in range(0, length):
        if answerList[i] == data:
            blankList[i] = data

    blankWord = ''.join(blankList)

    return blankWord

# 접속한 클라이언트마다 새로운 스레드가 생성되어 통신
def threaded(client_socket, addr, answer, life):
    # addr = host + port
    print('>>> 연결된 호스트: [', addr[0], ':', addr[1], "]")

    while True: # 클라이언트가 접속을 끊을 때 까지 반복합니다.
        try:
            # 유저가 입력한 문자 or 문자열
            data = client_socket.recv(1024)

            # if not data: #데이터가 없으면 disconnection -> 데이터가 없을 일은 없을 것 같아서?
            #     print('>>> 연결이 끊긴 호스트: [' + addr[0], ':', addr[1], "]")
            #     break

            # answer와 유저가 입력한 데이터 비교 TODO 함수명, 변수명 수정하기
            print('>>> 유저가 입력한 문자(열): [ ' + addr[0], ':', addr[1], data.decode(), "]")  # client로 부터 받은 데이터 보여주기

            # blankWord= "_" * len(answer)
            #
            # result = ""
            #
            # #사용자가 입력한게 문자냐 단어냐 구분
            # if len(data) == 1:
            #     result = checkChar(answer, data)
            # else:
            #     result = checkWord()
            #
            #
            # if result == "correct":
            #     print("문자 하나 맞춤 빈칸공개한다")
            #     showBlank = showBlank(answer, blankWord, data)
            #     print("근데 단어 다맞췄으면 유저 승리")
            # elif result == "wrong":
            #     print("목숨감소해야함")
            #     print("목숨 다떨어지면 유저 패배")
            # elif result == "userwin":
            #     print("단어맞춤 유저승리")
            # else:
            #     print("단어틀림 유저패배")
            #


            # 결과 보내기
            # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
            # TODO 본인을 포함한 모든 클라이언트에 중간 결과 공유
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






if __name__ == '__main__':
    client_sockets = [] # 서버에 접속한 클라이언트 목록


    # 서버 IP 및 열어줄 포트
    HOST = '127.0.0.1'
    PORT = 9999

    # 서버 소켓 생성
    print('>>> 서버 실행')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            print('>>> 서버 대기 상태')

            # clinent connection 체크 & 몇번 유저인지 반환
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)

            # 각 client의 thread 생성
            start_new_thread(threaded, (client_socket, addr))

            userTurnData = '>>> 순서 안내' + "\n" + \
                       "user" + str(client_sockets.index(client_socket)+1) + "입니다."
            server_socket.send(userTurnData.encode("utf-8"))

            # 참가자 수 확인 2가 맞으면 게임 실행
            if(checkParticipant(len(client_sockets))):
                server_socket.send("참여자가 2명이 되었으니 게임을 시작하도록 하겠습니다.".encode("utf-8"))
                #게임 메뉴 -> 예진

                #단어, 목숨 설정 및 안내하기
                answer = randomWords();
                life = len(answer) - 1;
                gameSettingData = ">>> 맞출 단어의 길이는 " + len(answer) + "이며, 목숨은 " + life + "개입니다.";
                server_socket.send(gameSettingData.encode("utf-8"))
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
