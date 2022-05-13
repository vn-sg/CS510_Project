import requests

url = 'http://127.0.0.1:5000/getScore'
myobj = "hello world"

x = requests.post(url, json = myobj)

print(x.content)