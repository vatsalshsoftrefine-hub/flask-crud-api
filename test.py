import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://127.0.0.1:5000/register"

session = requests.Session()


def send_request(i):
    data = {
        "name": f"user{i}",
        "email": f"user{i}@gmail.com",
        "password": "1234",
        "phone": "9876543210",
        "gender": "male"
    }

    response = session.post(URL, json=data)
    return response.status_code


def main():
    start = time.time()

    total_requests = 10000

    with ThreadPoolExecutor(max_workers=200) as executor:
        results = list(executor.map(send_request, range(total_requests)))

    end = time.time()

    print("Success:", results.count(201))
    print("Time:", round(end - start, 2))


if __name__ == "__main__":
    main()