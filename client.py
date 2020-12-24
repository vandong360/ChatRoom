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
from login import getuser, login
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
print(getuser['userId'])
 
def clientloop(userUID):
    
    def connect_Server():
        global c
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        HOST = "localhost"
        PORT = 1404
        c.connect((HOST, PORT))

        #dict
        mess = {"userUID": userUID, "message": "welcome!"}   
        c.send(str(mess).encode('utf-8'))
        global ct
        ct = c
        _thread.start_new_thread(recvMessage, (c,))

    def recvMessage(c):
        while True:
            mess = c.recv(1024).decode('utf-8')
            rep = mess.replace("'","\"")
            m = json.loads(rep)
            # write =  f'{m["userUID"]}: {m["message"]}'
            # txt = textArea.get(1.0, END)
            # textArea.delete(1.0, END)
            textArea.insert(END,m["userUID"]+": "+m["message"]+"\n")
            textArea.yview(END)

    #Tkinter GUI
    bg = 'white'
    dark = "#242526"

    clt = Tk()
    clt.title('Chat Screen')
    clt.configure( bg='#18191a')
    clt.geometry('800x600+400+100')
    clt.resizable( False, False)

    fUser = Frame(clt, bg=dark, width=300, height=600)
    fUser.pack(side=LEFT)

    fChat = Frame(clt, bg="#18191a", width=500, height=600)
    fChat.pack(side=RIGHT)

    #Chat Group
    textArea = ScrolledText( clt, width=68, height=31.5 ,font=('Arial', 10, 'bold'), wrap=WORD)
    textArea.place( x=300, y=30 )

    ipMess = Entry(fChat, width=35, font=('Arial', 14))
    ipMess.place( x=0, y=550, height=40)


    def sendMessage (*args):
        mess = ipMess.get()
        global c
        if mess.strip():
            mess = str({'userUID': userUID, 'message': mess})
            c.send(mess.encode('utf-8'))
        else:
            pass
        ipMess.delete(first=0, last=50)    
        
    btnSend = Button(fChat, text='Gửi', command=sendMessage)
    btnSend.place( x=400, y=550, width=85, height=40) 

    # #Menu Options

    def out():
        try:
            clt.destroy()
            login()
        except Exception as e:
            print(e)

    btnOut = Button(fUser, text='Đăng Xuất', command=out).pack()
    # i = Image.open('D:\Project Library\Python\ChatRoom\img\menu.png')
    # i = i.resize((50,50), Image.ANTIALIAS)
    # menuImg = ImageTk.PhotoImage(i)
    # menuBtn = Menubutton(fUser, image=menuImg, relief=RAISED)
   
    # menuBtn.menu = Menu(menuBtn)
    # menuBtn['menu'] = menuBtn.menu

    # menuBtn.menu.add_command(label = 'abc1', command = hi1)
    # menuBtn.menu.add_command(label = 'abc2', )
    # menuBtn.menu.add_command(label = 'amcmf',)

   # menuBtn.place( x=0, y=0)

    connect_Server()
    def closing():
        clt.destroy()

  #  clt.protocol('WM_DELETE_WINDOW', closing)


    clt.bind('<Return>', sendMessage)
    clt.mainloop()
 

clientloop("Văn Đông")

