import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.constants import TOP
from PIL import Image, ImageTk
import tkinter.messagebox
from typing import Text
import pyrebase
import firebase_admin
from firebase_admin import auth, credentials
import client
from client import clientloop

cred = credentials.Certificate("chatroom-ad9f5-firebase-adminsdk-nfjmc-783a12fab7.json")
firebase_admin.initialize_app(cred)

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

        #-------Xử lý đăng nhập-------
def login():
    try:
        reg.destroy()
    except:
        pass

    global log
    log = Tk()
    log.title('Đăng Nhập')
    log.configure( bg='#222e42')
    log.geometry('500x600+550+100')
    log.resizable( False, False)

    Label( log, bg='#222e42', height=1).pack()

    #----------Create Logo-------------
    i = Image.open('img\logo.jpg')
    i = i.resize((250,200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(i)
    show = Label( log, image=img, height=100, width=150)
    show.pack()


    #----------Create Form------------
    frameLogin = Frame( log, bg='#1c2439')
    frameLogin.place( x=95, y=150, height=245, width=310)

    lbTitle = Label( frameLogin, text='ĐĂNG NHẬP TÀI KHOẢN', fg='white', bg='#1c2439', width=0, height=2, font=('Arial', 15, 'bold'))
    lbTitle.pack()


    lbEmail = Label( frameLogin, text='Email: ', fg='white', bg='#1c2439', font=('Arial', 10, 'bold'))
    lbEmail.place( x=10, y=60)

    ipEmail = Entry(frameLogin, width='28', bg='white', font=('Arial', 13, 'bold'))
    ipEmail.place( x=25, y=90)


    lbPass = Label( frameLogin, text='Password: ', fg='white', bg='#1c2439', font=('Arial', 10, 'bold'))
    lbPass.place( x=10, y=128)

    ipPass = Entry( frameLogin, show='*', width='28', bg='white', font=('Arial', 13, 'bold'))
    ipPass.place( x=25, y=155)


    def submit(*args):

        email = ipEmail.get()
        password = ipPass.get()

        try:
            global userUID
            user = ath.sign_in_with_email_and_password(email, password)
            getuser = ath.refresh(user['refreshToken'])
            userUID = getuser['userId']
            log.destroy()
            client.clientloop(userUID)
         
        except  Exception as e:
            #tkinter.messagebox.showwarning( title='Thông báo', message='Email hoặc mật khẩu không chính xác!')
            print(e)


    btnLog = Button( log, bd='4', text='Đăng Nhập', width=15, fg='white', bg='#d6ab00', font=('Arial', 13, 'bold'), command=submit)
    btnLog.place( x=170, y=380)


    Label( log, text='Chưa có tài khoản?', fg='white', bg='#1c2439', font=('Arial', 11, 'italic')).place( x=110, y=460)
    Button( log, bd='4', text='Đăng Ký Ngay', width=11, fg='white', bg='#0c90e8', font=('Arial', 11, 'bold'), command=register).place( x=260, y=455)

    log.bind('<Return>', submit)
    log.mainloop()



        #---Xử lý đăng ký tài khoản---
def register():

    try:
        log.destroy()
    except:
        pass

    global reg
    reg = Tk()
    reg.title('Đăng Ký')
    reg.configure( bg='#222e42')
    reg.geometry('500x600+550+100')
    reg.resizable( False, False)

    Label( reg, bg='#222e42', height=1).pack()

    #----------Create Logo-------------
    i = Image.open('img\logo.jpg')
    i = i.resize((250,200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(i)
    show = Label( reg, image=img, height=100, width=150)
    show.pack()


    #----------Create Form register------------
    frameLogin = Frame( reg, bg='#1c2439')
    frameLogin.place( x=95, y=150, height=320, width=310)

    lbTitle = Label( frameLogin, text='ĐĂNG KÝ TÀI KHOẢN', fg='white', bg='#1c2439', width=0, height=2, font=('Arial', 15, 'bold'))
    lbTitle.pack()


    lbEmail = Label( frameLogin, text='Email: ', fg='white', bg='#1c2439', font=('Arial', 10, 'bold'))
    lbEmail.place( x=10, y=60)

    ipEmail = Entry(frameLogin, width='28', bg='white', font=('Arial', 13, 'bold'))
    ipEmail.place( x=25, y=90)


    lbName = Label( frameLogin, text='Tên Người Dùng: ', fg='white', bg='#1c2439', font=('Arial', 10, 'bold'))
    lbName.place( x=10, y=128)

    ipName = Entry( frameLogin, width='28', bg='white', font=('Arial', 13, 'bold'))
    ipName.place( x=25, y=155)


    lbPass = Label( frameLogin, text='Password: ', fg='white', bg='#1c2439', font=('Arial', 10, 'bold'))
    lbPass.place( x=10, y=193)

    ipPass = Entry( frameLogin, show='*', width='28', bg='white', font=('Arial', 13, 'bold'))
    ipPass.place( x=25, y=220)

    def submit(*e):
        email = ipEmail.get()
        name = ipName.get()
        password = ipPass.get()
        try:
            user =  auth.create_user(uid=name, email=email, password=password)
            tkinter.messagebox.showinfo( title='Thông báo', message='Đăng ký thành công!')
            login()
        except:
            tkinter.messagebox.showwarning( title='Thông báo', message='Email đã được đăng ký!')


    btnReg = Button( reg, bd='4', text='Đăng Ký', width=15, fg='white', bg='#ed0f76', font=('Arial', 13, 'bold'), command=submit)
    btnReg.place( x=170, y=450)

    
        
    Label( reg, text='Đã có tài khoản?', fg='white', bg='#1c2439', font=('Arial', 11, 'italic')).place( x=120, y=505)
    Button( reg, bd='4', text='Đăng Nhập', width=11, fg='white', bg='#0c90e8', font=('Arial', 11, 'bold'), command=login).place( x=260, y=500)     


    reg.bind('<Return>', submit)
    reg.mainloop()
    
login()

from client import state
while True:
    if state==False:
        login()
        state = True
        continue
    print(':D')

    

