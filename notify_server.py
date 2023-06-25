import requests, json

def send_push_notification(to, title, body):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "host": "exp.host",
        "content-type": "application/json",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "user-agent": "Expo",
    }

    data = {
        "to": to,
        "title": title,
        "body": body,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.json())

send_push_notification("ExponentPushToken[xOCEDgKfrobajclKb1tZKi]" , "Pralka numer {} wolna!".format(1), "Pralka nr {} jest już wolna, chcesz ją zarezerwować?".format(1))