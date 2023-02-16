import hashlib
import base64

def handle_websocket_upgrade(client_socket,request):
    headers = request.split(b'\r\n')
    headers_dict = {}
    for header in headers:
        header_parts = header.split(b': ')
        if len(header_parts) == 2:
            headers_dict[header_parts[0].decode()] = header_parts[1].decode()
    key = headers_dict['Sec-WebSocket-Key']
    accept_key = base64.b64encode(hashlib.sha1(key.encode() + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())
    
    # Send the server's upgrade response
    response = b'HTTP/1.1 101 Switching Protocols\r\n'
    response += b'Upgrade: websocket\r\n'
    response += b'Connection: Upgrade\r\n'
    response += b'Sec-WebSocket-Accept: ' + accept_key + b'\r\n\r\n'
    client_socket.sendall(response)

def receive_websocket_data(client_socket):
    data = client_socket.recv(1024)
    if len(data) < 6:
        return None
    payload_len = data[1] & 127
    if payload_len == 126:
        payload_len = int.from_bytes(data[2:4], byteorder='big')
        mask_index = 4
    elif payload_len == 127:
        payload_len = int.from_bytes(data[2:10], byteorder='big')
        mask_index = 10
    else:
        mask_index = 2
    masks = [b for b in data[mask_index:mask_index+4]]
    data_index = mask_index + 4
    decoded = b''
    for i in range(payload_len):
        decoded += bytes([data[data_index+i] ^ masks[i % 4]])
    return decoded.decode()

def send_websocket_data(client_socket, data):
    encoded = bytearray()
    encoded.append(129)
    if len(data) <= 125:
        encoded.append(len(data))
    elif len(data) <= 65535:
        encoded.append(126)
        encoded.extend(len(data).to_bytes(2, byteorder='big'))
    else:
        encoded.append(127)
        encoded.extend(len(data).to_bytes(8, byteorder='big'))
    encoded.extend(data.encode())
    client_socket.sendall(encoded)

def upgrade_websocket_connection(client_socket):
    pass

def auto_get_args(defaults):
    def finner(func):
        args = func.__code__.co_varnames[:func.__code__.co_argcount]
        keys = defaults.keys()
        def sinner():
            r = []
            for i in args:
                if i in keys:
                    r.append(defaults[i])
                else:
                    r.append(None) 
            return func(*r)
        return sinner
    return finner
