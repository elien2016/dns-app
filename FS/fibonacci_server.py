from flask import Flask, request, abort
from socket import *
app = Flask(__name__)

def fib(n):
    if n <= 1:
        return n
    
    memo = [None] * (n+1)
    memo[0] = 0
    memo[1] = 1

    for i in range(2, n+1):
        memo[i] = memo[i-1] + memo[i-2]
    
    return memo[n]

@app.route('/register', methods=['PUT'])
def register():
    if request.is_json:
        data = request.get_json()
        print(data)
        hostname = data.get('hostname')
        ip = data.get('ip')
        as_ip = data.get('as_ip')
        as_port = data.get('as_port')
        if any(v is None for v in [hostname, ip, as_ip, as_port]):
            return 'failure', 400

        sock = socket(AF_INET, SOCK_DGRAM)
        message = f'TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n'
        sock.sendto(message.encode(), (as_ip, as_port))
        bytes, _ = sock.recvfrom(2048)
        sock.close()

        res = bytes.decode()
        if res == 'success':
            return 'success', 201
        else:
            return 'failure', 400
    else:
        abort(400)

@app.route('/fibonacci')
def fibonacci():
    number = request.args.get('number')
    if number is None:
        abort(400)
    else:
        if number.isdecimal():
            return str(fib(int(number)))
        else:
            return 'bad format', 400
            
app.run(host='0.0.0.0',
        port=9090,
        debug=True)
