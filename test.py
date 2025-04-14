import requests

url = "http://localhost:5000"
data = {"message": "Hello, Logstash!"}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except requests.exceptions.RequestException as e:
    print("Error:", e)
