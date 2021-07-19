import requests
import time
import subprocess
import signal

print("----------measuring startup time--------------")
startup_start = time.time()
p = subprocess.Popen(["docker", "run", "-p", "5000:5000", "osless-py"])
while True:
    try:
        r = requests.get("http://127.0.0.1:5000/")
        if r.status_code == 200:
            break
    except:
        pass
    time.sleep(0.05)
startup_end = time.time()
print(f'startup time : {startup_end - startup_start}')
print("----------measuring request time------------")
avg = 0.0
for _ in range(10):
    request_start = time.time()
    r = requests.get("http://127.0.0.1:5000/")
    request_end = time.time()
    avg += request_end - request_start
avg /= 10
print(f'average request time {avg}')
p.send_signal(signal.SIGINT)
