import requests
from bs4 import BeautifulSoup
import csv
from config import URL, HEADER, file_name


def get_html(url, params=""):
    """ Функція, яка повертає html сторінку по url і params, які ми передамо їй"""
    r = requests.get(url, headers=HEADER, params=params)
    return r


def get_content(html) -> list:
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all('div', class_="sc-182gfyr-0 jmBHNg")
    cards = []

    for item in items:
        cards.append(
            {
                "title": item.find('a', class_="cpshbz-0 eRamNS").get_text(strip=True),
                "link_product": item.find('div', class_="be80pr-16 be80pr-17 kpDSWu cxzlon").find("a").get('href'),
                "name_bank": item.find('span', class_="be80pr-21 dksWIi").get_text(strip=True),
                "card_img": item.find('img', class_="be80pr-10 jIGseK").get("src")
            }
        )

    return cards


def save_doc(items, path):
    with open(path, "w", newline="", encoding="utf-16") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(['Name card', 'Link card', 'Name_bank', 'Link_photo'])
        for item in items:
            writer.writerow([item["title"], item["link_product"], item["name_bank"], item["card_img"]])


def parser():
    # PAGENATION = int(input("Вкажіть кількість сторінок пагінації:").strip())
    PAGENATION = 1  # на даному сайті немає пагінації тому встановимо 1

    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION + 1):
            print(f'Parsing page number : {page}')
            html = get_html(URL)  # html = get_html(URL, params={'page': page}) якщо треба пагінація
            cards.extend(get_content(html))  # в список додаємо дані які ми зпарсили з однієї стторінки, цикл проходиться по сторінках пагінації
            save_doc(cards, file_name)  # за допомогою написаної нами функції save doc ми записуємо построчно файл csv
        print(f"We have {len(cards)} records in our file")

    else:
        print('Error')


if __name__ == "__main__":
    parser()
