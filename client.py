import tkinter
from tkinter import *
import pyrebase
from tkinter.scrolledtext import *
from tkinter import filedialog
from tkinter.constants import TOP
import tkinter.messagebox
from PIL import Image, ImageTk
import socket
import _thread
from typing import List, Tuple
import json


config = {
    'apiKey': "AIzaSyBkGks1-i7U4xZV29_5_lnhoP4eIPVmKLw",
    'authDomain': "chatroom-ad9f5.firebaseapp.com",
    'databaseURL': "https://chatroom-ad9f5.firebaseio.com",
    'projectId': "chatroom-ad9f5",
    'storageBucket': "chatroom-ad9f5.appspot.com",
    'messagingSenderId': "443266528031",
    'appId': "1:443266528031:web:98aa42679344dfa676b62a",
    'measurementId': "G-FT8YT1QEZZ"
}

fb = pyrebase.initialize_app(config)
ath = fb.auth()
rdb = fb.database()

#xử lý get chat history
chatList = rdb.child("message").get()
global state


def clientloop(userUID):

    def connect_Server():
        global c
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        HOST = "localhost"
        PORT = 1404
        c.connect((HOST, PORT))

        #dict
        mess = {"userUID": userUID, "message": "", "state": "Online"}   
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
                

            if m["state"] == "Online":
                lstUser.configure(state='normal')
                lstUser.delete(1.0, END)
                for x in m["listUser"]:       
                    lstUser.insert(INSERT, x+"\n")
                    lstUser.yview(END)
                print("onl")
                lstUser.configure(state='disabled')
                

            elif m["state"] == "Offline":
                lstUser.configure(state='normal')
                lstUser.delete(1.0, END)
                for a in m["listUser"]: 
                    lstUser.insert(INSERT, a+"\n")
                    lstUser.yview(END)
                print("off")
                lstUser.configure(state='disabled')


            if m["message"] != "":
                textArea.configure(state='normal')
                textArea.insert( END, m["userUID"]+": "+m["message"]+"\n")
                textArea.yview(END)
                textArea.configure(state='disabled')

    #Hàm xử lý đăng xuất
    def out(*args):
        try: 
            global state
            state = False
            m = str({"userUID": userUID, "message": "", "state": "Offline"})
            c.send(m.encode('utf-8'))
        except Exception as e:
            print(e)


    #Hàm xử lý gửi mess đang nhập đến server
    def sendMessage (*args):
        mess = ipMess.get()
        global c

        if mess.strip():
            data = {userUID: mess}
            rdb.child("message").push(data) 
            mess = str({'userUID': userUID, 'message': mess, 'state': 'None'})
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

    #Chat Group
    Label(fChat, text="Chat Room", fg="#6bb0ea", bg=dark, font=('Arial', 15, 'bold')).place(x=185, y=3)
    textArea = ScrolledText( fChat, width=68, height=27 ,font=('Arial', 13, 'bold'), wrap=WORD)
    textArea.place( x=0, y=30 )
    
    #vòng lặp in ra đoạn chat trước đó
    for message in chatList.each():
        
        m = message.val()
        for key, value in m.items():
            textArea.insert(END, key+": "+value+"\n")


    textArea.configure(state='disabled')

    ipMess = Entry(fChat, width=35, font=('Arial', 14))
    ipMess.place( x=0, y=550, height=40)
        
    btnSend = Button(fChat, text='Gửi', fg="black", bg="#6bb0ea", command=sendMessage)
    btnSend.place( x=400, y=550, width=85, height=40) 


    #User GUI
    i = Image.open("img\logoUs.png")
    i = i.resize((50,50), Image.ANTIALIAS)
    img =ImageTk.PhotoImage(i)     

    Label( fUser, image=img, height=50, width=50, bg= dark).place(x=5, y=20)
    Label( fUser, text=userUID, fg="#6bb0ea", bg= dark, font=('Arial', 18, 'bold')).place(x=100, y=30)
    btnOut = Button(fUser, text='Đăng Xuất', fg="#6bb0ea", bg="#232f34", command=out).place( x=0, y=80)
    
    Label( fUser, text='Danh sách Online', fg="white", bg="#232f34", font=('Arial', 15, 'bold')).place( x=60 , y=110)
    lstUser = ScrolledText( fUser, width=20, fg="#6bb0ea", bg="#232f34",height=18 ,font=('Arial', 16, 'bold'), wrap=WORD)
    lstUser.place( x=15, y=145 )
    lstUser.configure(state='disabled')



    def on_closing(*args):
        clt.destroy()
        m = str({"userUID": userUID, "message": "", "state": "Offline"})
        c.send(m.encode('utf-8'))

    clt.protocol("WM_DELETE_WINDOW", on_closing)

    connect_Server()
    clt.bind('<Return>', sendMessage)
    clt.mainloop()


