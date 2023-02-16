import socket
import json
import threading
from . import helpers

def send(client,channel,data={}):
    data.update({"channel":channel})
    helpers.send_websocket_data(client,json.dumps(data))

def recv(client):
    return json.loads(helpers.receive_websocket_data(client))

class Client:
      def __init__(self) -> None:
          self.channels = {}

      def channel(self,channel_name):
          def get_func(func):
              self.channels.update({channel_name:func})       
          return get_func

      def handle_server(self,client):
          try:
            while 1:
              data = recv(client)
              print(data)
              helpers.auto_get_args({"client":client,"data":data})(self.channels[data["channel"]])()
          except Exception as e:
              print(e)
              exit()
       
      def createClient(self,host="localhost",port=1234):
          client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
          client.connect((host,port))
          helpers.upgrade_websocket_connection(client_socket=client)
          threading.Thread(target=self.handle_server,args=[client]).start()
          return client

