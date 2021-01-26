import requests, time

URL ="http://127.0.0.1:5000/notification"

while True:
    r = requests.get(url = URL)
    try:
        data = r.json()
        print(data)
    except:
        pass
    time.sleep(60)