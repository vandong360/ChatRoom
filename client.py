import tkinter
from tkinter import *
import pyrebase
from tkinter.scrolledtext import *
from tkinter import filedialog
from tkinter.constants import TOP
import tkinter.messagebox
from PIL import Image, ImageTk
import socket
import login
from login import login, userUID
import _thread
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
ath = firebase.auth()
rdb = firebase.database()

#getuser = ath.refresh(user['refreshToken'])    
#xử lý get chat history
chatList = rdb.child("message").get()


def clientloop(userUID):
    
    def connect_Server():
        global c
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        HOST = "localhost"
        PORT = 1404
        c.connect((HOST, PORT))

        #dict
        mess = {"userUID": userUID, "message": ""}   
        c.send(str(mess).encode('utf-8'))
        global ct
        ct = c
        _thread.start_new_thread(recvMessage, (c,))


    #Hàm nhận message từ server
    def recvMessage(c):
        while True:
            mess = c.recv(1024).decode('utf-8')
            rep = mess.replace("'","\"")
            m = json.loads(rep)
            if m["message"] != "":
                textArea.insert(END,m["userUID"]+": "+m["message"]+"\n")
                textArea.yview(END)


    #Hàm xử lý đăng xuất
    def out():
        try:
            clt.destroy()
            login()
        except Exception as e:
            print(e)


    #Hàm xử lý gửi mess đang nhập đến server
    def sendMessage (*args):
        mess = ipMess.get()
        global c

        if mess.strip():
            data = {userUID: mess}
            rdb.child("message").push(data) 
            mess = str({'userUID': userUID, 'message': mess})
            c.send(mess.encode('utf-8'))  
        else:
            pass
        ipMess.delete(first=0, last=50) 


    #Tkinter GUI
    bg = 'white'
    dark = "#242526"

    clt = Tk()
    clt.title(userUID)
    clt.configure( bg="black")
    clt.geometry('800x600+400+100')
    clt.resizable( False, False)

    fUser = Frame(clt, bg=dark, width=298, height=600)
    fUser.pack(side=LEFT)

    fChat = Frame(clt, bg=dark, width=500, height=600)
    fChat.pack(side=RIGHT)

    fonline = Frame(fUser, bg="#232f34", width=270, height=480).place( x=15, y=110 )

    #Chat Group
    Label(fChat, text="Chat Room", fg="#6bb0ea", bg=dark, font=('Arial', 15, 'bold')).place(x=185, y=3)
    textArea = ScrolledText( fChat, width=68, height=27 ,font=('Arial', 13, 'bold'), wrap=WORD)
    textArea.place( x=0, y=30 )
    
    #vòng lặp in ra đoạn chat trước đó
    for message in chatList.each():
        
        m = message.val()
        for key, value in m.items():
            textArea.insert(END, key+": "+value+"\n")


    ipMess = Entry(fChat, width=35, font=('Arial', 14))
    ipMess.place( x=0, y=550, height=40)
        
    btnSend = Button(fChat, text='Gửi', fg="black", bg="#6bb0ea", command=sendMessage)
    btnSend.place( x=400, y=550, width=85, height=40) 

    #User GUI
    i = Image.open("img\logoUs.png")
    i = i.resize((50,50), Image.ANTIALIAS)
    img =ImageTk.PhotoImage(i)     

    Label( fUser, image=img, height=50, width=50, bg= dark).place(x=3, y=20)
    Label( fUser, text=userUID, fg="#6bb0ea", bg= dark,font=('Arial', 18, 'bold')).place(x=100, y=30)
    btnOut = Button(fUser, text='Đăng Xuất', fg="#6bb0ea", bg="#232f34", command=out).place( x=0, y=80)
    

    


    connect_Server()
    def closing():
        clt.destroy()

    #clt.protocol('WM_DELETE_WINDOW', closing)

    clt.bind('<Return>', sendMessage)
    clt.mainloop()

clientloop(userUID)

