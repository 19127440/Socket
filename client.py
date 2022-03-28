from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
from tkinter import messagebox
from types import BuiltinMethodType

def handle_receive(msg_receive):
    def register_unaccepted_UI():
        tkinter.messagebox.showinfo("REPORT", "Username has already been used.", master=report)
        report.destroy()

    def register_accepted_UI():
        tkinter.messagebox.showinfo("REPORT", "Register success.", master=report)
        report.destroy()

    def login_unaccepted_UI():
        tkinter.messagebox.showinfo("REPORT", "Wrong username or password.", master=report)
        report.destroy()

    def login_accepted_UI():
        tkinter.messagebox.showinfo("REPORT", "Log in success.", master=report)
        report.destroy()

    def quit_UI():
        send("{quit}")
        client_socket.close()
        tkinter.messagebox.showinfo("Shut down", "The server has shut you down!")
        report.destroy()

    #start handling
    report = tkinter.Tk()
    report.withdraw()
    split = msg_receive.split(":")
    command = split[0]

    if command == "LoginAccept":
        login_accepted_UI()
        receive_thread = Thread(target=receive)
        receive_thread.start()
        userUI_thread = Thread(target=userUI(split[1], split[2]))
        userUI_thread.start()

    elif command == "LoginUnAccept":
        login_unaccepted_UI()
        mainUI_thread = Thread(target=mainUI)
        mainUI_thread.start()

    elif command == "RegisterAccept":
        register_accepted_UI()
        mainUI_thread = Thread(target=mainUI)
        mainUI_thread.start()

    elif command == "RegisterUnAccept":
        register_unaccepted_UI()
        mainUI_thread = Thread(target=mainUI)
        mainUI_thread.start()

    elif command == "Find":
        report.destroy()
        data = split[2].split()
        subUI_thread = Thread(target=find_UI(data))
        subUI_thread.start()

    elif command == "{quit}":
        quit_UI()

def receive():
    msg = ""
    while True:
        try:
            if len(msg) != 0:
                msg_received = msg
                msg = ""
                handle_receive(msg_received)
            else:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
        except OSError:
            break
        finally:
            client_socket.close()

def send(str):
     client_socket.sendall(bytes(str, "utf8"))


def mainUI():
    def send_register(envent=None):
        str = "register "+username.get() + " " + password.get()
        print(str)
        send(str)
        mainUI.destroy()
    
    def send_login(envent=None):
        str = "login "+username.get() + " " + password.get()
        print(str)
        send(str)
        mainUI.destroy()

    def close(envent=None):
        send("{quit}")
        client_socket.close()
        tkinter.messagebox.showinfo("Close", "Socket had close!")
        mainUI.destroy()

    mainUI = tkinter.Tk()
    mainUI.geometry("300x150")
    mainUI.title("LOGIN")
    mainUI.configure(bg = "white")

    username = tkinter.StringVar()
    password = tkinter.StringVar()

    username_label = tkinter.Label(mainUI, text="Username:", bg="White").grid(row=0, column=0)
    username_entry = tkinter.Entry(mainUI, textvariable=username).grid(row=0, column=1)
    password_label = tkinter.Label(mainUI, text="Password:", bg="white").grid(row=1, column=0)
    password_entry = tkinter.Entry(mainUI, textvariable=password, show='*').grid(row=1, column=1)
    register_button = tkinter.Button(mainUI, text="Register", fg="blue", width='7', command=send_register).grid(row=0, column=2)
    login_button = tkinter.Button(mainUI, text="Login", fg="green", width='7', command=send_login).grid(row=1, column=2)
    close_button = tkinter.Button(mainUI, text="Exit", fg="red", width='7', command=close).grid(row=2, column=1)
    mainUI.protocol("WM_DELETE_WINDOW", close)
    mainUI.mainloop()

def userUI(username, password):
    def send_find(envent=None):
        str = "find " + info.get()
        print(str)
        send(str)
    
    def close(envent=None):
        str = "quit " + username + " " + password
        send(str)
        userUI.destroy()

    userUI = tkinter.Tk()
    userUI.geometry("400x200")
    userUI.title("USER")
    userUI.configure(bg="white")

    info = tkinter.StringVar()

    find_label = tkinter.Label(userUI, text="Enter brand:", bg="white").grid(row=0, column=0)
    find_entry = tkinter.Entry(userUI, textvariable=info).grid(row=0, column=1)
    find_button = tkinter.Button(userUI, text="Find", fg="blue", width='7', command=send_find).grid(row=0, column=2)
    close_button = tkinter.Button(userUI, text="Close", fg="red", width='7', command=close).grid(row=2, column=1)
    userUI.protocol("WM_DELETE_WINDOW", close)
    userUI.mainloop()

def find_UI(data):
    def close(event=None):
        findUI.destroy()
    findUI = tkinter.Tk()
    findUI.geometry("600x100")
    findUI.title("SEARCH")
    row1 = tkinter.Entry(findUI, width=20, fg='blue', font=('Times New Roman',12,'bold'))
    row1.grid(row=1, column=1)
    row1.insert(tkinter.END, "Company: " + data[0])
    row2 = tkinter.Entry(findUI, width=20, fg='blue', font=('Times New Roman',12,'bold'))
    row2.grid(row=1, column=2)
    row2.insert(tkinter.END, "Brand: " + data[1])
    row3 = tkinter.Entry(findUI, width=15, fg='blue', font=('Times New Roman',12,'bold'))
    row3.grid(row=1, column=3)
    row3.insert(tkinter.END, "Sell: " + data[2])
    row4 = tkinter.Entry(findUI, width=15, fg='blue', font=('Times New Roman',12,'bold'))
    row4.grid(row=1, column=4)
    row4.insert(tkinter.END, "Buy: " + data[3])
    close_button = tkinter.Button(findUI, text="Close", fg="red", width='7', command=close).grid(row=10, column=1)
    findUI.mainloop()
'''data = 'a b c d'
data = data.split()
find_UI(data)'''

def HOST_close():
    HOST_screen.destroy()

HOST_screen = Tk()
HOST_screen.geometry("250x100")
HOST_screen.title("HOST")

global HOST

HOST = StringVar()
PORT = 3456
HOST_label = Label(HOST_screen, text="HOST:").grid(row=0, column=0)
HOST_entry = Entry(HOST_screen, textvariable=HOST).grid(row=0, column=1)  
HOST_button = Button(HOST_screen, text="Enter", fg="blue",width='7', command=HOST_close).grid(row=1, column=1)
HOST_screen.mainloop()

BUFSIZ = 1024
ADDR = (HOST.get(), PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

UI_thread = Thread(target=mainUI)
UI_thread.start()