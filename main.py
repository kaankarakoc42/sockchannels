from sockchannels.server import Server,send
import pickledb

app = Server()
db = pickledb.load("./users.json",True)

@app.channel("join")
def join(server,data):
    app.memory[data["user_id"]]=server
    print(f"[!] {data['user_id']} user joined!")
    send(server,"join",{"status":True})
    db.set(data["user_id"],{"active":True})
    return data["user_id"]

@app.channel("left")
def left(user_id):
    del app.memory[user_id]
    db.set(user_id,{"active":False}) 
    print(f"[!] {user_id} user left and deleted!")

@app.channel("send_message")
def send_messeges(server,data):
    send(app.memory[data["target"]],"recv_messages",data)
    send(server,"send_message",{"status":True})
          

app.mainloop()
