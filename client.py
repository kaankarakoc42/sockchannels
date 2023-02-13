import socket
import json
import threading
 
channels = {}

def channel(channel_name):
    def get_func(func):
           channels.update({channel_name:func})       
    return get_func

def send(client,channel,data={}):
    data.update({"channel":channel})
    client.send(json.dumps(data).encode("utf8"))

def recv(client):
    data = client.recv(1024).decode("utf8")
    return json.loads(data)

def handle_server(client):
    try:
     while 1:
       data = recv(client)
       channels[data["channel"]](client,data)
    except Exception as e:
       print(e)
       exit()
       
def createClient():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("localhost",1234))
    threading.Thread(target=handle_server,args=[client]).start()
    return client

if __name__ == "__main__":
    @channel("ping")
    def test(client,data):
        print("ping")
        send(client,"ping")

    @channel("pong")
    def send_back(client,data):
        print("pong")
        send(client,"pong")

    client = createClient()
    send(client,"pong")