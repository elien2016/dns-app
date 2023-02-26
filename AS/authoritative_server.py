from socket import *
import os

port = 53533
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('0.0.0.0', port))
while True:
    bytes, client_addr = sock.recvfrom(2048)
    message = bytes.decode()

    # Parse message
    data_dict = {}
    for line in message.splitlines():
        key, value = line.split('=')
        data_dict[key] = value

    type = data_dict.get('TYPE')
    hostname = data_dict.get('NAME')
    ip = data_dict.get('VALUE')

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'records', hostname)

    if ip is None: # DNS query
        if hostname is None or type is None:
            sock.sendto('FORMERR'.encode(), client_addr)
        else:
            try:
                with open(filename, 'r') as file:
                    file_contents = file.read()
                sock.sendto(f'success: {file_contents}'.encode(), client_addr)
            except FileNotFoundError:
                sock.sendto('failure: not found'.encode(), client_addr)
            except Exception as e:
                sock.sendto(f'failure: {str(e)}'.encode(), client_addr)
    else: # registration
        if hostname is None or ip is None or hostname == 'None' or ip == 'None':
            sock.sendto('failure'.encode(), client_addr)
        else:
            with open(filename, 'w+') as file:
                file.write(message)
            sock.sendto('success'.encode(), client_addr)
