import socket
import random
import hashlib

chain = ["a"]


def run():
    nonce = ''
    nonce2 = ''
    hvalue = ''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # 서버 연결 시도
        s.connect(('127.0.0.1', 4000))

        # 넌스 교환 단계
        data = s.recv(1024)
        if not data:
            s.close()
            exit
        nonce2 = data.decode()
        print("받은 NONCE값 : " + nonce2)
        print(" ")
        nonce = str(create_nonce())
        line = nonce
        s.sendall(line.encode())
        if not line:
            s.close()
            exit

        # 제네시스 블록 생성
        hvalue = create_genesis(nonce, nonce2)

        # 메시지 교환 단계
        while True:
            data = s.recv(1024)
            if not data:
                break
            print("받은 메시지 : " + data.decode())
            # 무결성 검증단계
            if hvalue == data.decode().split("/")[1]:
                hvalue = create_next(data.decode().split("/")[0], hvalue)
            else:
                print("공격 또는 오류가 발생하였습니다!!")
                print(" ")

            line = input("보낼 메시지 : ")
            send_msg = line + "/" + hvalue
            s.sendall(send_msg.encode())
            # 서버가 빈 데이터를 받고 연결을 종료할 수 있도록 함
            if not line:
                break
            hvalue = create_next(line, hvalue)
        s.close()


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
    run()
