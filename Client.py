# -*- coding: utf-8 -*-

import socket
from _thread import *


def recv_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            data = data.decode()
            print(data)

            global flag

            if data == "GAME OVER":
                flag = False
                print(">>> 패배하셨습니다.")
                exit()
            elif data == "WIN":
                flag = False
                print(">>> 승리하셨습니다.")
                exit()

            elif '_' in data:
                print("======================================")
                print(">>> 알파벳 혹은 단어를 입력하세요: ")


        except ConnectionResetError as e:
            print('에러는? : ', e)
            client_socket.close()
            break

##############################################################################################
flag = True
HOST = '127.0.0.1'  # 포트포워딩 후 서버를 실행시킬 컴퓨터의 IP주소로 변경 후 실행
PORT = 9999  # 사용자 지정 내부 포트

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('>>> Connect Server')

if __name__ == '__main__':
    print('>>> 클라이언트 실행')

    try:
        start_new_thread(recv_data, (client_socket,))
        while flag:
            message = input()
            client_socket.send(message.encode())
        print("!!게임이 끝났습니다!!")
        exit()

    except Exception as e:
        print('에러는? : ', e)
    finally:
        client_socket.close()
