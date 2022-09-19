import requests
from bs4 import BeautifulSoup
import lxml
import time
import json
import time

start_time = time.time()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
lst = []
lst_of_currencies = []
url = 'https://cryptorank.io/ru/all-coins-list'
lst_of_arb = []
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'lxml')
data = soup.find_all("tr", class_="styled__StyledTableRow-sc-1oam7fn-5 ftyTMR")
for i in data:
    link = "https://cryptorank.io" + i.find("a", class_="table-coin-link__StyledLink-sc-pprt06-6 bLZygE").get("href")
    lst_of_currencies.append(link)

for j in lst_of_currencies:
    response = requests.get(j, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find("div", class_="menu-header__MenuHeaderWrapper-sc-177ymon-0 dfssCF")
    s = str(data.find("a", class_="item active").get("href"))
    arb_name = "https://cryptorank.io" + s
    lst_of_arb.append(arb_name)


for k in lst_of_arb:
    res = requests.get(k, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    name = soup.find("div", class_="app-header__AppHeader-sc-13ssse4-0 hMhNCk coin-info__name").text
    if soup.find("span", class_="styled__PercentContainer-sc-1qtnlbe-0 iuFICN percent") == None:
        percents_for_week = soup.find("span", class_="styled__PercentContainer-sc-1qtnlbe-0 eeuaGk percent").text
    if soup.find("span", class_="styled__PercentContainer-sc-1qtnlbe-0 eeuaGk percent") == None:
        percents_for_week = soup.find("span", class_="styled__PercentContainer-sc-1qtnlbe-0 iuFICN percent").text
    price = soup.find("div", class_="app-header__AppHeader-sc-13ssse4-0 styled__CoinPriceHeaderComponent-sc-dtzux9-0 gTgLPZ edyRnj").text
    capitalisation = soup.find("div", class_="styled__DataColumn-sc-4javab-3 eDCINN").text
    lst.append(
        {
            "Имя криптовалюты": name,
            "Цена": price.strip(percents_for_week),
            "Изменение за неделю в процентах": percents_for_week.strip("\xa0"),
            "Капитализация": capitalisation
        }
    )

with open("currencies.json", "w", encoding='utf-8') as file:
    json.dump(lst, file, indent=4, ensure_ascii=False)

print("Время поиска данных:" + "\n" + "-" * 30 + "\n" + f"{time.time()-start_time}")