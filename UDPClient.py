import requests

fs_ip = 'localhost'
fs_port = 9090

data = {
    'hostname': 'fibonacci.com',
    'ip': '172.18.0.1',
    'as_ip': '172.18.0.1',
    'as_port': 53533
}

response = requests.put(f'http://{fs_ip}:{fs_port}/register', json=data)
print(response.status_code, response.text)
