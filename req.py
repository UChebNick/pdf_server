import requests

url = "http://127.0.0.1:8000/upload/pdf"

for i in range(1):
    files = {"file": open(r'C:\Users\cheba\Downloads\14. Функция y=sqrt(x).pdf', "rb")}

    response = requests.post(url, files=files)
    print(response.text)

