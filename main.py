import requests
import json
import time
import random
from flask import jsonify
import datetime


host_url = "YOUR HOST URL"

def test_home():
    ts = time.time()
    url= host_url + "/home"
    resp = requests.get(url=url)
    if resp.status_code == 200:
        data = resp.json()
        print("Resp: ",data)
    else:
        print(resp.status_code)
    print(f"time: {time.time() - ts} (s)")


def test_get():
    ts = time.time()
    url = host_url + "/test-get"
    json_data = {"name":"CWKU3","id":1220189}
    json_data = json.dumps(json_data, ensure_ascii=False).encode('utf-8')
    resp = requests.get(url,data=json_data)
    if resp.status_code == 200:
        data = resp.json()
        print("Resp: ",data)
    else:
        print(resp.status_code)
    print(f"time: {time.time() - ts} (s)")


def test_post():
    ts = time.time()
    url = host_url + "/test-post"
    json_data = {"request_number":random.randint(1,100),
                "request_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    json_data = json.dumps(json_data, ensure_ascii=False).encode('utf-8')
    resp = requests.post(url,data=json_data)
    if resp.status_code == 200:
        data = resp.json()
        print("Resp: ",data)
    else:
        print(resp.status_code)
    print(f"time: {time.time() - ts} (s)")



if __name__ == '__main__':
    test_home()
    test_get()
    test_post()