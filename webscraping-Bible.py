import random
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

while True:
    # Generate a random number for the chapter
    num = random.randint(1, 21)
    if num <= 9:
        x = f"https://ebible.org/asv/JHN0{num}.htm"
    else:
        x = f"https://ebible.org/asv/JHN{num}.htm"

    webpage = str(x)
    print(webpage)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(x, headers=headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.title.text)

    page_verses = soup.findAll('div', class_='p')

    verses_list = []
    for section_verses in page_verses:
        verses_list.extend(section_verses.text.split("."))

    verses_list = [i.strip() for i in verses_list if i.strip()]

    my_choice = random.choice(verses_list)

    print(f"Chapter: {num} Verse: {my_choice}")

    # Ask the user if they want another verse
    cont = input("Press Enter for another verse, or type 'exit' to quit: ")
    if cont.lower() == 'exit':
        break
