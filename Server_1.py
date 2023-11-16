from socket import *
from _thread import *
import random


def checkParticipant(len):
    if len == 2:
        return True
    else:
        return False

def randomWords():
    words = ['physical', 'datalink', 'network', 'transport', 'applicaion',
             'bit', 'frame', 'datagram', 'segment', 'message',
             'socket', 'thread', 'server', 'client', 'programming']
    return words[random.randrange(0, 16)]

def checkChar(answer, data, doneChar):
    if data in doneChar:
        return "doneChar"

    if data in answer:
        return "correct"
    else:
        return "wrong"


def checkWord(answer, data):
    if answer == data:
        return "userwin"
    else:
        return "userlose"


def showBlank(answer,blankWord,data):
    answerList = list(answer)
    blankList = list(blankWord)

    length = len(answer)

    for i in range(0, length):
        if answerList[i] == data:
            blankList[i] = data

    blankWord = ''.join(blankList)

    return blankWord

def sendMessageForAll(data):
    # 결과 보내기
    for client in client_sockets:
        client.send(data.encode())


def checkBlank(blankWord):
    if "_" in blankWord:
        return False
    else:
        return True

# 접속한 클라이언트마다 새로운 스레드가 생성되어 통신
def threaded(client_socket, addr):
    # addr = host + port
    print('>>> 연결된 호스트: [', addr[0], ':', addr[1], "]")

    while True:  # 클라이언트가 접속을 끊을 때까지 반복합니다.
        try:
            # 유저가 입력한 문자 or 문자열
            data = client_socket.recv(1024)

            # 전역변수
            global blankWord
            global randomString
            global life
            global doneChar
            result = ""

            # answer와 유저가 입력한 데이터 비교
            print('>>> 유저가 입력한 문자(열): [ ' + addr[0], ':', addr[1], "]", data.decode())  #client로 부터 받은 데이터 보여주기

            data = data.decode()

            # 문자 or 문자열 체크
            if len(data) == 1:
                result = checkChar(randomString, data, doneChar)
            else:
                result = checkWord(randomString, data)

            doneChar = doneChar + data

            if result == "correct": # 하나만 맞췄을 때
                blankWord = showBlank(randomString, blankWord, data)
                sendMessageForAll(blankWord)
                if checkBlank(blankWord):
                    sendMessageForAll("WIN")
                    break
            elif result == "wrong": # 하나만 틀렸을 때
                life -= 1
                if life <= 0:
                    sendMessageForAll("GAME OVER")
                    break
                sendMessageForAll("남은 목숨 : {}".format(life))
            elif result == "userwin": # 전부 다 맞췄을 때
                sendMessageForAll("WIN")
                sendMessageForAll("정답은 " + randomString + "입니다")
                # sendMessageForAll(">>> 단어 맞추기에 성공했습니다")
                break
            elif result == "doneChar":
                sendMessageForAll("이미 입력한 문자입니다")
            else:
                sendMessageForAll("GAME OVER")
                break

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))


    client_socket.close()

# 전역 변수
client_sockets = []
randomString = ""
blankWord = ""
life = 0
doneChar = ""

if __name__ == '__main__':



    # 서버 IP 및 열어줄 포트
    HOST = '127.0.0.1'
    PORT = 9999

    # 서버 소켓 생성
    print('>>> 서버 실행')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('>>> 서버 대기 상태')

    try:
        while True:

            # client connection 체크 & 몇번 유저인지 반환
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)

            # 각 client의 thread 생성
            start_new_thread(threaded, (client_socket, addr))
            print(">>> 참가자 수 : ", len(client_sockets))

            userTurnData = '\n>>> 순서 안내: ' + \
                           "user" + str(client_sockets.index(client_socket) + 1) + "입니다"
            client_socket.send(userTurnData.encode("utf-8"))

            if (len(client_sockets) == 1):
                client_socket.send("\n참여자가 1명이니 잠시 기다려주세요".encode("utf-8"))

            if (len(client_sockets) == 2):
                print(">>> 게임 프로세스 시작하기")
                client_sockets[0].send("\n게임 시작\n".encode("utf-8"))
                client_sockets[1].send("\n게임 시작\n".encode("utf-8"))
                break

            #
            # else:
            #     raise Exception('2명만 참가해야 게임을 시작할 수 있습니다.')

        ### 여기서부터 게임 로직
        randomString = randomWords()
        life = len(randomString) - 1
        blankWord = "_" * len(randomString)
        doneChar = ""
        sendMessageForAll("랜덤 단어를 생성하였습니다. 차례에 맞추어 문자 or 단어를 입력해주세요")
        # client_sockets[0].send("랜덤 단어를 생성하였습니다. 차례에 맞추어 문자 or 단어를 입력해주세요".encode("utf-8"))
        # client_sockets[1].send("랜덤 단어를 생성하였습니다. 차례에 맞추어 문자 or 단어를 입력해 주세요".encode("utf-8"))

        while len(client_sockets) != 0:
            a=1



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
