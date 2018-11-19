import socket
import random
import hashlib
import sys

chain = ["a"]


def run_server(port=4000):
    host = ''
    nonce = ''
    nonce2 = ''
    hvalue = ''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # 서버 리스닝
        s.bind((host, port))
        s.listen(1)
        print("서버가 시작되었습니다!!")
        print("---------------------")

        # 서버 연결 대기
        conn, addr = s.accept()
        print("서버가 연결되었습니다!!")
        print("---------------------")

        # 넌스 생성
        print("자동으로 넌스를 생성하였습니다")
        print("---------------------")
        nonce = str(create_nonce())

        # 넌스 교환
        line = nonce
        conn.sendall(line.encode())
        data = conn.recv(1024)
        print("받은 NONCE : " + data.decode())
        print(" ")
        nonce2 = data.decode()

        # 제네시스 블록 생성
        hvalue = str(create_genesis(nonce, nonce2))

        # 메시지 전송 단계
        while True:
            command = input('Command : ')
            if command == "send msg":         # 메시지 보내기
                line = input("보낼 메시지 : ")		# 평문 입력
                send_msg = line + "/" + hvalue
                conn.sendall(send_msg.encode())
                if not line:
                    break
                hvalue = create_next(line, hvalue)
                data = conn.recv(1024)
                if not data:
                    break
                print("받은 메시지 : " + data.decode())
                # 무결성 검증단계
                if hvalue == data.decode().split("/")[1]:
                    hvalue = create_next(data.decode().split("/")[0], hvalue)
                else:
                    print("공격 또는 오류가 발생하였습니다!!")
                    print(" ")

            else:
                print("올바른 명령이 아닙니다.")
                print(" ")

        conn.close()


def create_nonce():
    nonce = random.randrange(1000000, 2000000)
    return nonce


def create_genesis(nonce, nonce2):
    block = {
        "msg": "genesis",
        "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
        "nonce": int(nonce)+int(nonce2)
    }

    hvalue = hashlib.sha256()
    hvalue.update(str(block).encode())
    chain.append(hvalue.hexdigest())
    print(str(block))
    print("제네시스 블록의 해시값 : " + hvalue.hexdigest())
    print(" ")
    return hvalue.hexdigest()


def create_next(msg, prev_hash):
    block = {
        "msg": msg,
        "prev_hash": prev_hash,
        "nonce": 0
    }

    hvalue = hashlib.sha256()
    hvalue.update(str(block).encode())
    chain.append(hvalue.hexdigest())
    print(str(block))
    print(str(len(chain)-1) + "번째 블록의 해시값 : " + hvalue.hexdigest())
    print(" ")
    return hvalue.hexdigest()


if __name__ == '__main__':
    run_server()
