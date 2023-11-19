# -*- coding: utf-8 -*-

from socket import *
from _thread import *
import random
import time

def checkParticipant(len):
    if len == 2:
        return True
    else:
        return False


def randomWords():
    words = ['physical', 'datalink', 'network', 'transport', 'application',
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
    for client in client_sockets:
        client.send(data.encode())
    time.sleep(0.1)


def checkBlank(blankWord):
    if "_" in blankWord:
        return False
    else:
        return True

# 접속한 클라이언트마다 새로운 스레드가 생성되어 통신
def threaded(client_socket, addr):
    print('>>> 연결된 호스트: [', addr[0], ':', addr[1], "]")

    while True:
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
                if checkBlank(blankWord):
                    sendMessageForAll("정답: {}".format(blankWord))
                    sendMessageForAll("WIN")
                    break
                sendMessageForAll("맞았습니다. 남은 목숨 : {}".format(life))
                sendMessageForAll("정답: {}".format(blankWord))
            elif result == "wrong": # 하나만 틀렸을 때
                life -= 1
                sendMessageForAll("틀렸습니다. 남은 목숨 : {}".format(life))
                if life <= 0:
                    sendMessageForAll("정답: {}".format(randomString))
                    sendMessageForAll("GAME OVER")
                    break
                sendMessageForAll("정답: {}".format(blankWord))
            elif result == "userwin": # 전부 다 맞췄을 때
                sendMessageForAll("정답: {}".format(randomString))
                sendMessageForAll("WIN")
                break
            elif result == "doneChar": # 이미 입력한 문자
                sendMessageForAll("이미 입력한 문자입니다. 남은 목숨 : {}".format(life))
                sendMessageForAll("정답: {}".format(blankWord))
            else: #단어를 틀렸을 때
                life = 0
                sendMessageForAll("틀렸습니다. 남은 목숨 : {}".format(life))
                sendMessageForAll("정답: {}".format(randomString))
                sendMessageForAll("GAME OVER")
                break

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))


    client_socket.close()


##############################################################################################
client_sockets = []
randomString = ""
blankWord = ""
life = 0
doneChar = ""

if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 9999

    print('>>> 서버 실행')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('>>> 서버 대기 상태')

    try:
        while True:

            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)

            start_new_thread(threaded, (client_socket, addr))
            print(">>> 참가자 수 : ", len(client_sockets))

            userTurnData = '>>> 순서 안내: ' + \
                           "user" + str(client_sockets.index(client_socket) + 1) + "입니다"
            client_socket.send(userTurnData.encode("utf-8"))

            if len(client_sockets) == 1:
                client_socket.send("참여자가 1명이니 잠시 기다려주세요".encode("utf-8"))

            if len(client_sockets) == 2:
                print(">>> 게임 프로세스 시작하기")
                menu = "##############################<—행멘 게임 메뉴얼—>#############################\n" + "\t1. 2인 1팀으로 진행합니다.\n " + "\t2. 2명이 접속하면 게임을 시작합니다.\n" + "\t3. 영어 단어는 랜덤으로 선정되며, 목숨은 단어 길이-1 입니다.\n" + "\t4. USER 1,2가 번갈아 가며 게임을 진행하게 됩니다.\n" + "\t5. 자신의 차례에 알파벳 하나를 입력해 게임을 계속 진행하거나,\n\t단어 전체를 입력해 정답을 맞추어 주세요.\n" + "\t6. 입력한 단어가 정답이면 SUCCESS, 틀리면 FAIL로 게임이 중단됩니다.\n" + "##################################<—THE END->###################################\n"
                sendMessageForAll(menu)
                break

        # 게임 로직
        randomString = randomWords()
        life = len(randomString) - 1
        blankWord = "_" * len(randomString)
        doneChar = ""
        sendMessageForAll("!!게임 시작!!\n랜덤 단어를 생성하였습니다. 차례에 맞추어 문자 또는 단어를 입력해주세요")
        sendMessageForAll("정답: {}".format(blankWord))

        while len(client_sockets) == 2:
            a=1


    except Exception as e:
        print('에러는? : ', e)
    finally:
        server_socket.close()

