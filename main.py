from os import system, path, mkdir, getcwd
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime, timedelta
from fake_useragent import UserAgent

class cs:
    INFO = '\033[93m'
    GREEN = '\033[92m'
    END = '\033[0m'

User_Agent = f'{UserAgent().random}'

_ = system("cls")
name = input(f"{cs.INFO}Name: ")
age = input("Age: ")
offset = input("Offset: ")
now = datetime.now()
start = int((now - timedelta(days=int(age)*30)).month)
print(f"Search from: 01.{start:02}{cs.END}")

def parse(name, day, month, offset):
    HEADERS = {
        'User-Agent': User_Agent
    }
    url = f"https://telegra.ph/{name}-{month}-{day}{offset}"
    response = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')  
    items = soup.findAll('img')
    photos = []
    print(f"SEARCH   | Start | {day}.{month}{offset}")
    for item in items:
        src = item.get('src')
        if not "https" in src:
            photos.append(f"https://telegra.ph{src}")
    if photos:
        print(f"{cs.GREEN}DOWNLOAD | Start | {day}.{month}{offset}{cs.END}")
        if not path.isdir(f"{getcwd()}\\images"):
            mkdir(f"{getcwd()}\\images")
        if not path.isdir(f"{getcwd()}\\images\\{name}"):
            mkdir(f"{getcwd()}\\images\\{name}")
        if not path.isdir(f"{getcwd()}\\images\\{name}\\{day}_{month}_{offset[1:]}"):
            mkdir(f"{getcwd()}\\images\\{name}\\{day}_{month}_{offset[1:]}")
        for i in range(len(photos)):
            response = requests.get(photos[i], headers = HEADERS)
            with open(f"images/{name}/{day}_{month}_{offset[1:]}/{month}_{day}_{offset[1:]}_{i}.jpg", "wb") as file:
                file.write(response.content)
        print(f"{cs.GREEN}DOWNLOAD |  End  | {day}.{month}{offset}{cs.END}")

def main():
    print("")
    for _month in range(start, now.month):
        for _day in range(1, 31):
            for _offset in range(1, int(offset) + 1):
                if _offset == 1:
                    parse(name, f"{_day:02}", f"{_month:02}", "")
                else:
                    parse(name, f"{_day:02}", f"{_month:02}", f"-{_offset}")

if __name__ == "__main__":
    main()