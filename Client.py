# -*- coding: utf-8 -*-

import socket
from _thread import *


# 서버로부터 메세지를 받는 메소드
def recv_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)  # 블로킹 함수
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
HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 생성
client_socket.connect((HOST, PORT))  # 연결
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
