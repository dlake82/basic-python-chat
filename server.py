from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject

# self.parent : 부모윈도우를 저장하는 변수
# self.bListen : 서버 소켓이 리슨(접속 대기) 상태인지 아닌지 저장
# self.client : 접속한 클라이이언트들을 저장할 리스트 변수
# self.ip : 접속한 클라이언트의 IP주소를 저장할 변수
# self.thread : 리슨 및 클라이언트 접속시 마다 생성되는 실행흐름 저장 리스트
# self.conn, self.recv : 클라이언트 접속, 데이터 수신시 보내는 시그널

# 시그널 객체
class Signal(QObject):
    conn_signal = pyqtSignal()
    recv_signal = pyqtSignal(str)

# 서버 소켓
class ServerSocket: 
    def __init__(self, parent):
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []

        self.conn = Signal()
        self.recv = Signal()

        self.conn.conn_signal.connect(self.parent.updateClient)
        self.recv.recv_signal.connect(self.parent.updateMsg)

    # 객체 삭제
    def __del__(self):
        self.stop()
    
    # 서버 시작
    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)

        # 서버 바인드
        try:
            self.server.bind((ip,port))
        # 바인드 에러
        except Exception as e:
            print("Bind Error: ", e)
            return False
        # 에러가 없을 시 서버 대기를 True로 변경
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
            print("Server Listening...")

        return True

    # ServerSocket 클래스 객체 파괴
    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    # 서버 대기
    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error: ', e)
                break
            else:
                self.clients.append(client)
                self.ip.append(addr)
                self.conn.conn_signal.emit()
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

            self.removeAllClients()
            self.server.close()

    # 받기
    def receive(self, addr, client):
        while True:
            try:
                # pyqtSignal(str)
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else: 
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.send(msg)
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]: ', addr, msg)

        self.removeClient(addr, client)
        
    # 메세지 전송
    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Send() Error : ',e)

    # 클라이언트 제거
    def removeClient(self, addr, client):
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        self.conn.conn_signal.emit()

        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del(self.threads[i])
            i+=1

        self.resourceInfo()
    
    # 모든 클라이언트 제거
    def removeAllClients(self):
        for c in self.clients:
            c.close()

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()
        
        self.conn.conn_sigmal.emit()
        
        self.resourceInfo()


    # 리소스 정보 받기
    def resourceInfo(self):
        print("Number of Client ip|t: ", len(self.ip))
        print("Number of Client socket|t: ", len(self.clients))
        print("Number of Client thread|t: ", len(self.threads))
            


    