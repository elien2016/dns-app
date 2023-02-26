import requests

fs_ip = 'localhost'
fs_port = 9090

data = {
    'hostname': 'fibonacci.com',
    'ip': 'localhost',
    'as_ip': 'localhost',
    'as_port': 53533
}

response = requests.put(f'http://{fs_ip}:{fs_port}/register', json=data)
print(response.status_code, response.text)
