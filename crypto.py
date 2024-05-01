from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import openpyxl as xl
from openpyxl.styles import Font

webpage = 'https://www.webull.com/quote/crypto'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(webpage, headers=headers)

url = urlopen(req).read()
soup = BeautifulSoup(url, 'html.parser')
print(soup.title.text)

crypto_data = soup.findAll('div', class_='table-cell')
crypto_names = soup.findAll('p', class_='tit bold')

for i in range(5):
    name = crypto_names[i].text.strip()
    last_price = float(crypto_data[i*5+2].text.replace(',', ''))
    percent_change_str = crypto_data[i*5+3].text.replace('%','')
    percent_change = float(percent_change_str) if percent_change_str != '-' else 0
    corresponding_price = last_price * (1 + percent_change / 100)

    print(f"Name: {name}")
    print(f"Current Price: {last_price:,.3f}")
    print(f"Percent Change: {percent_change}")
    print(f"Corresponding Price: {corresponding_price:.2f}")
    print()
    print()