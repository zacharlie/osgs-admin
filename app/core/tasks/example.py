import requests
import time


def time_consuming_request(url: str = "https://wikipedia.org"):
    resp = requests.get(url)
    total = 0
    for i, elem in enumerate(resp.text.split()):
        time.sleep(1)
        print(f"{i}: {elem}")
        total += 1
    return total
