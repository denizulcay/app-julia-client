import requests

session = requests.session()
response = session.get('http://127.0.0.1:5000')
print(response.text)

session.request(
    stream=
)