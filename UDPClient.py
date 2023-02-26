# I deleted my deployment on IBM Cloud so the IP address below will NOT work.
# But I included this file as an example.
import requests

fs_ip = '159.122.174.86'
fs_port = 30002

data = {
    'hostname': 'fibonacci.com',
    'ip': '159.122.174.86',
    'as_ip': '159.122.174.86',
    'as_port': 30001
}

response = requests.put(f'http://{fs_ip}:{fs_port}/register', json=data)
print(response.status_code, response.text)
