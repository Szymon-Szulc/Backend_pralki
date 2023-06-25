import time

import tinytuya as tt
import requests

url = "http://localhost:3002/api/v1/"

def checks_sockets_remotly():
    devices = tt.deviceScan(True, 5, True, True, False, True)
    print(devices)
    obj = {
        "token": "test_token",
        "id": 0,
        "devices": devices
    }
    requests.post(url + "dorms_server", json=obj)

# checks_sockets_remotly()

def check_sockets():
    while True:
        resposne = requests.get(url + "dorms_server?did=1")
        machines = resposne.json()["machines"]
        devices = []
        for machine in machines:
            print(machine)
            machine_id = machine["mid"]
            ip = machine["ip"]
            localKey = machine["localKey"]
            try:
                d = tt.OutletDevice(machine_id, ip, localKey)
                d.set_version(3.3)
                d.set_socketRetryLimit(1)
                d.set_socketNODELAY(True)
                d.set_socketTimeout(0.5)
                status = d.status()
                print(status)

                if machine["lock"]:
                    if(status["dps"]["1"]):
                        d.turn_off()
                else:
                    d.turn_on()
                print("Error" in status)
                if "Error" in status:
                    # off
                    devices.append({
                        "id": machine["id"],
                        "turn_on": False
                    })
                else:
                    # on
                    devices.append({
                        "id": machine["id"],
                        "turn_on": True
                    })
            except:
                # off
                devices.append({
                    "id": machine["id"],
                    "turn_on": False
                })
        print(devices)
        obj = {
            "token": "test",
            "did": 1,
            "devices": devices
        }
        print(obj)
        headers = {'Content-Type': 'application/json'}
        requests.patch(url + "dorms_server", json=obj, headers=headers)
        time.sleep(1)


check_sockets()