import socket
import json
import threading

channels = {}

def channel(channel_name):
    def get_func(func):
           channels.update({channel_name:func})       
    return get_func

def recv(server):
    return json.loads(server.recv(1024).decode("utf8"))

def send(server,channel,data={}):
    data.update({"channel":channel})
    server.send(json.dumps(data).encode("utf8"))


def handle_client(server):
    try:
     while True:
         data = recv(server)
         channels[data["channel"]](server,data)
    except Exception as e:
        print(e)
        


def mainloop():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("localhost",1234))
    server.listen()
    while True:
        server_handler,_=server.accept()
        threading.Thread(target=handle_client,args=[server_handler]).start()

if __name__ == "__main__":
    import time
    @channel("pong")
    def send_back(server,data):
        print("pong")
        send(server,"ping")
        time.sleep(0.4)

    @channel("ping")
    def send_back(server,data):
        print("ping")
        send(server,"pong")
        time.sleep(0.4)
    mainloop()