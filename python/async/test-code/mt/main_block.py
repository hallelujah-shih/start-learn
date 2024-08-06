import time
import requests
from concurrent.futures import ThreadPoolExecutor
from util import timed


def get_status_code(url: str) -> int:
    resp = requests.get(url)
    return resp.status_code


@timed
def main():
    with ThreadPoolExecutor() as executor:
        urls = ["https://www.knownsec.com/" for _ in range(100)]
        results = executor.map(get_status_code, urls)
        print("results:", list(results))


if __name__ == '__main__':
    main()
