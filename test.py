import tkinter
from tkinter import *
from tkinter.scrolledtext import *
import json


def send(*args):
    m = etry.get()
    TextBox.insert(END, "you: "+m)

window = Tk()

window.wm_title("Scroll From Bottom")
TextBox = ScrolledText(window, height='10', width='45', wrap=WORD)
TextBox.pack()
etry = Entry(window, width=35, font=('Arial', 14)).pack()
btn = Button(window, text='Gửi', command=send).pack()

name = ""
mess = {"userUID": name, "mess": "welcome!"}
m = json.dumps(mess)
y = json.loads(m)
t = 0
to_write = f'{y["userUID"]}: {y["mess"]}'
while t < 5:
    x = TextBox.get(1.0, END)
    TextBox.delete(1.0, END)
   # TextBox.insert(END,x+to_write+"\n")
   # TextBox.yview(END)
    t+=1
TextBox.configure(state='disabled')


window = mainloop()