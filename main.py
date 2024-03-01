import sys
import os
import client

def __main__(self, *args):
    #args가 없으면 헬프 출력
    command = args[1]
    
    if command == "help":
        help()
    elif command == "online_user":
        client.Client()
    elif command == "connect":
        client.Client()
    elif command == "disconnect":
        client.Client()
    elif command == "talk":
        client.Client()
    elif command == "logoff":
        client.Client()
    else:
        client.Client('help')