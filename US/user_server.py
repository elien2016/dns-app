from flask import Flask, request, abort
from socket import *
import requests
app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Bad request
    if any(v is None for v in [hostname, fs_port, number, as_ip, as_port]):
        abort(400)

    # OK request
    sock = socket(AF_INET, SOCK_DGRAM) # get fs ip
    message = f'TYPE=A\nNAME={hostname}\n'
    sock.sendto(message.encode(), (as_ip, int(as_port)))
    bytes, _ = sock.recvfrom(2048)
    sock.close()
    res = bytes.decode()
    if 'success' in res:
        data = res.split(': ')[1]
        data_dict = {}
        for line in data.splitlines():
            key, value = line.split('=')
            data_dict[key] = value
        fs_ip = data_dict.get('VALUE')
        result = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci', params={'number': number}) # make request to fs
        return result.text, result.status_code
    else:
        return res, 400

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
