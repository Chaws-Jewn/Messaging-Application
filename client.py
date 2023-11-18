import socket, threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

root = tk.Tk()
root.geometry("700x800")
root.resizable(0,0)

DARK_OCEAN = "#1A5276"
OCEAN = "#1F618D"
DARK_BLUE = "#154360"

BTN_FONT = ""
LABEL_FONT = ("Amasis MT Pro Black", 25)
MSG_FONT = ("Arial", 20)

# Send message, reset entry
def send_message():
    message = message_entry.get()
    client.sendall(message.encode("utf-8"))
    message_entry.delete(0, len(message))

# Send message keybind <Return>
def send_message_key(event):
    send_message()

# Infinite loop for receiving messages from server
def receive_messages():
    while True:
        message = client.recv(1024).decode("utf-8")
        message_area.config(state=tk.NORMAL)
        message_area.insert(tk.END, message + '\n')
        message_area.config(state=tk.DISABLED)

# Create username before joining server
def create_username():
    username_entry.config(state= "disabled")
    join_chat.config(state= "disabled")
    connect_to_server(username_entry.get())

def create_username_key(event):
    create_username()

# Error on getting username, allow resubmission of username
def enter_new_username():
    username_entry.config(state= tk.NORMAL)
    username_entry.delete(0, len(username_entry.get()))
    username_entry.focus_set()
    join_chat.config(state= tk.NORMAL)

# Server connection
def connect_to_server(username):
    global client
    server_address = ("127.0.0.1", 5555)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(server_address)
        check_username(username)
    except Exception as e:
        print(f"Error: {e}")

# Check matching username on server
def check_username(username):
    try:
        client.sendall(username.encode("utf-8"))
        server_response = client.recv(1024).decode("utf-8")
        if server_response == "success":
            # After success on sending username
            message = f"{client.recv(1024).decode("utf-8")}"
            message_area.config(state=tk.NORMAL)
            message_area.insert(tk.END, message + '\n')
            message_area.config(state=tk.DISABLED)
            message_entry.config(state=tk.NORMAL)
            send_message_btn.config(state=tk.NORMAL)
            message_entry.focus_set()
            root.bind("<Return>", func= send_message_key)
            threading.Thread(target=receive_messages).start()
            threading.Thread(target=send_message).start()
        
        elif server_response == "failed":
            warning = messagebox.showwarning(title= "Username warning", message= "Username has already been used. Please choose another.")
            enter_new_username()
        
    except Exception as e:
        print(f"Error: {e}")


# UI configuration
root.configure(background= DARK_BLUE)
title = tk.Label(text= "Chat Room", font= LABEL_FONT, width= 10, foreground= "white", background= DARK_BLUE).grid(row=0, column=0, columnspan= 3, pady= (10, 0))
username_box = tk.Label(text= "Username: ", font= MSG_FONT, width= 10, foreground= "white", background= OCEAN).grid(row=1, column=0, padx= (10, 0), pady= 3)
username_entry = tk.Entry(justify= "right", font= MSG_FONT, width= 25, foreground= "white", background= OCEAN, border= 5)
username_entry.grid(row=1, column=1, pady= 3)
join_chat = tk.Button(text= "Join", font= ("Arial", 15), command= create_username, foreground= "white", background= OCEAN, border= 5)
join_chat.grid(row= 1, column= 2, padx= (0, 15))

message_area = scrolledtext.ScrolledText(root, font= MSG_FONT, bg= OCEAN, fg= "white", width=43, height= 18, border= 5)
message_area.grid(row=2, column=0, columnspan= 3, padx= 10, pady= 20)
message_area.config(state=tk.DISABLED)

message_entry = tk.Entry(state= tk.DISABLED, justify= "right", font= MSG_FONT, width= 35, foreground= "white", background= OCEAN, border= 5)
message_entry.grid(row=3, column=0, columnspan= 2, pady= (10,0))
send_message_btn = tk.Button(state=tk.DISABLED, text= "Send", font= ("Arial", 15), command= send_message, foreground= "white", background= OCEAN, border= 5)
send_message_btn.grid(row= 3, column= 2, pady= (10, 0), padx= (0, 15))

username_entry.focus_set()
root.bind("<Return>", func= create_username_key)

root.mainloop()
