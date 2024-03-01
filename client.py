from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import socket
import server


def main(self, *args):
    #args가 없으면 헬프 출력
    def help():
        print("""You can use many Command in this Program!!\n 
        - help: lookup commands (display all possible commands).\n
        - online_users: send a request to the regiServer, get back a list of all online peers and display them on the screen.\n
        - connect [ip] [port] : request to chat with peer with the given IP and port\n
        - disconnect [peer] : end your chat session with the listed peer\n
        - talk [peer] [message] : send a message to the peer that you've already initiated a chat with via the connect command\n
        - logoff : send a message (notification) to regiServer for logging off the chat system\n""")
    
    def send():

    def receive():

    def online_user():

    def connect(self, *args):
    
    def disconnect(sellf, *args):
    
    def talk(self, *args):

    def logoff(self):
    
    
    command = args[1]
    
    if command == "help":
        help()
    elif command == "online_user":
        online_user()
    elif command == "connect":

    elif command == "disconnect":

    elif command == "talk":

    elif command == "logoff":

    else:
        help()
    








