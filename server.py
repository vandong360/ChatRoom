import pyrebase
import _thread
import socket
from typing import List, Tuple
import json

firebaseConfig = {
    'apiKey': "AIzaSyBkGks1-i7U4xZV29_5_lnhoP4eIPVmKLw",
    'authDomain': "chatroom-ad9f5.firebaseapp.com",
    'databaseURL': "https://chatroom-ad9f5.firebaseio.com",
    'projectId': "chatroom-ad9f5",
    'storageBucket': "chatroom-ad9f5.appspot.com",
    'messagingSenderId': "443266528031",
    'appId': "1:443266528031:web:98aa42679344dfa676b62a",
    'measurementId': "G-FT8YT1QEZZ"
}

firebase = pyrebase.initialize_app(firebaseConfig)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
HOST = "localhost"
PORT = 1404
server.bind((HOST, PORT))
server.listen(7)

clients = []
listUsers = []

def connectClient(c):
    while True:
        try:
            mess = c.recv(1024).decode('utf-8')
            m = mess.replace("'","\"")
            p = json.loads(m)

            userUID = p["userUID"]
            message = p["message"]
            state = p["state"]

            #Check trạng thái hoạt động gửi về client:
            if state == "Online":
                listUsers.append(userUID) 

            elif state == "Offline":
                clients.pop(clients.index(c))
                listUsers.remove(userUID)
                print(listUsers)
                print(len(clients))
            
            toSend = str( {'userUID': userUID, 'message': message, 'state':  state, 'listUser': listUsers} )
            sendToAll(toSend)
        except:
            pass
    
def sendToAll(mess):
    for ct in clients:
        ct.send(mess.encode('utf-8'))

while True:
   
    try:
        c, ad = server.accept()
        print('Kết nối thành công')
        print('Connected by', ad)
        clients.append(c)
        _thread.start_new_thread( connectClient, (c,))  
        print("Số client: "+str(len(clients)))
    except:
        continue