import requests
from bs4 import BeautifulSoup
from config import URL, FILE_NAME
import csv
import create_db
from create_db import ec


def get_html(url):
    page = requests.get(URL)
    return page


def get_content(html):
    soup = BeautifulSoup(html.content, "html.parser")
    items = soup.find_all("div", class_="_3DNsL _3yOEq")

    cards = []

    for item in items:
        cards.append(
            {
                "name": item.find("div", class_="_1bfj5").find("h3").get_text(strip=True).split(","),
                "price": item.find("div", class_="_24XLO").find("span", class_="_2-l9W").get_text(strip=True).replace(
                    ",", ".")
            }
        )

    return cards


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        item = get_content(html)
        for i in item:
            i["price"] = i["price"][:-1] + "UAH"
        save_in_db(item)
        save_doc(item, FILE_NAME)
    else:
        print("Error, we dont get html page")


def save_in_db(list_items):
    for i in list_items:
        record_in_tab = f"""INSERT INTO price(country, region, price, currency)
                            VALUE("{(i["name"][0])}", "{i["name"][-1].strip()}", {i["price"][:-3]}, "{i["price"][-3:]}");
                         """
        create_db.execute_query(ec, record_in_tab)


def save_doc(list_items, path):
    with open(path, "w", encoding="utf-16") as file:
        writer = csv.writer(file)
        writer.writerow(["country", "region", "price", "currency"])
        for i in list_items:
            writer.writerow([i["name"][0], i["name"][-1].strip(), i["price"][:-3], i["price"][-3:]])


if __name__ == '__main__':
    parser()
