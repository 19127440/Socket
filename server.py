from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import database
from tkinter import *
from tkinter import messagebox
from database import *

def insert(my_msg):
    msg_list.insert(tkinter.END, my_msg)

def receive(client):
    msg = ""
    while True:
        try:
            if msg == "{quit}":
                insert("%s:%s left." % addresses[client])
                del addresses[client]
                client.close()
                break
            if len(msg) != 0:
                handle_client(client, msg)
                msg = ""
            else:
                msg = client.recv(BUFSIZ).decode("utf8")
        except OSError:
            break

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        insert("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=receive, args=(client,)).start()

def read_file():
    with open('users.txt', 'r') as f:
        list = f.readlines() 
    return list

def write_file(s):
    with open('users.txt', 'w') as f:
        f.write(s)

def register(usename, password):
    list = read_file()
    for i in list:
        temp = list[i].split()
        if(usename == temp[0]):
            return 0
    s = usename + ' ' + password + '\n'
    write_file(s)
    return 1

def login(usename, password):
    list = read_file()
    for i in list:
        temp = i.split()
        temp[1] = temp[1].rstrip ('\n')
        if(usename == temp[0] and password == temp[1]):
            return 1
    return 0

def handle_client(client, msg):
    split = msg.split()
    header = split[0]
    if header == "find":
        info = split[1]
        company, brand, sell, buy = search(info)
        data = "Find:" + company + " " + brand + " " + sell + " " + buy
        client.send(bytes(data, "utf8"))
    else:
        try:
            username = split[1]
            password = split[2]
            if header == "register":
                if register(username, password) == 1:
                    insert("%s:%s " % addresses[client]+"register username: "+ username + " and password: " + password + " success.")
                    client.send(bytes("RegisterAccept", "utf8"))
                elif register(username, password) == 0:
                    insert("%s:%s " % addresses[client]+"register username: "+ username + " and password: " + password + " fail.")
                    client.send(bytes("RegisterUnAccept", "utf8"))
            elif header == "login":
                if login(username, password) == 0:
                    insert("%s:%s " % addresses[client]+"log in username: "+ username + " and password: " + password + " fail.")
                    client.send(bytes("LoginUnAccept", "utf8"))
                elif login(username, password) == 1:
                    insert("%s:%s " % addresses[client]+"log in username: "+ username + " and password: " + password + " success.")
                    client.send(bytes("LoginAccept:" + username + ":" + password, "utf8"))
        except:
            if header == "register":
                client.send(bytes("RegisterUnAccept", "utf8"))
            if header == "login":
                client.send(bytes("LoginUnAccept", "utf8"))

def broadcast():
    global addresses
    for clients in addresses:
        clients.send(bytes("{quit}","utf8"))

#Host UI
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

clients = {}
addresses = {}

BUFSIZ = 1024
ADDR = (HOST.get(),PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    def on_closing(event=None):
        top.destroy()
        SERVER.close()

    top = tkinter.Tk()
    top.title("Manager")
    top.geometry("600x300")
    messages_frame = tkinter.Frame(top)

    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    close_button = tkinter.Button(top, text="Close", fg="red", width='7', command=on_closing)
    close_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    SERVER.listen()
    insert("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    top.mainloop()
    ACCEPT_THREAD.join()
    SERVER.close()