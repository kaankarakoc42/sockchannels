import socket
import json
import threading
from . import helpers

def recv(server):
    return json.loads(helpers.receive_websocket_data(server))
    

def send(server,channel,data={}):
    data.update({"channel":channel})
    helpers.send_websocket_data(server,json.dumps(data))

class Server:
      def __init__(self,host="localhost",port=1234) -> None:
          self.channels = {}
          self.bind_data = (host,port)
          self.memory = {}
          self.on_join = "join"
          self.on_left = "left"

      def channel(self,channel_name):
          def get_func(func):
              self.channels.update({channel_name:func})       
          return get_func

      def handle_client(self,server):
            helpers.handle_websocket_upgrade(server,request=server.recv(1024))
            data = recv(server)
            user_id = helpers.auto_get_args({"server":server,"data":data})(self.channels[self.on_join])()
            user_left = helpers.auto_get_args({"user_id":user_id})(self.channels[self.on_left])
            try:
              while True:
                    data = recv(server)
                    helpers.auto_get_args({"server":server,"data":data})(self.channels[data["channel"]])()
            except Exception as e:
                   print(e)
                   user_left()

      def mainloop(self):
          server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          server.bind(self.bind_data)
          server.listen()
          while True:
                server_handler,_=server.accept()
                threading.Thread(target=self.handle_client,args=[server_handler]).start()
