import requests
from bs4 import BeautifulSoup
import xlsxwriter
from pyhunter import PyHunter
import json

'''
#Для тестов
z = "https://itunes.apple.com/us/genre/ios-games/id6014?mt=8&letter=A&page=1#page"

x = requests.get(z)
obj = BeautifulSoup(x.text, "html.parser")

new = BeautifulSoup((requests.get(obj.find("a", {"class": "paginate-more"})['href'])).text, "html.parser")
print(new.find("a", {"class": "paginate-more"})['href'])
'''

hunter = PyHunter("8db5e297f49a680ba4c44e7bde053ada37443550")
#print(hunter.domain_search("http://alphaforkids.com"))
#file = (requests.get("https://api.hunter.io/v2/domain-search?domain=http://alphaforkids.com&api_key=8db5e297f49a680ba4c44e7bde053ada37443550").json())
#json.load()

workbook = xlsxwriter.Workbook("Game_B.xlsx")
worksheet = workbook.add_worksheet()

worksheet.write("A1", "Game")
worksheet.write("B1", "Company")
worksheet.write("C1", "Contact")

before = "https://itunes.apple.com/us/genre/ios-games/id6014?mt=8&letter=B&page="
after = "#page"

applications = {}

count = 2
game_count = 1
page = 1

for suchka in range(158):
    try:
        print("PAGE: ", page)
        main_page = BeautifulSoup((requests.get(before + str(page) + after)).text, "html.parser")
        listLink = main_page.find("div", {"id": "selectedcontent"}).findAll("a")
        for i in listLink:
            print("GAME: ", game_count)
            link = BeautifulSoup((requests.get(i['href'])).text, "html.parser")
            price = link.findAll("li", {"class": "inline-list__item inline-list__item--bulleted"})
            if len(price) == 2 or (price[0]).text != "Free":
                name = link.find("h1", {"class": "product-header__title"})
                name.span.decompose()
                applications['Name'] = name.text
                company = link.find("a", {"class": "link"})
                applications['Company'] = company.text
                suite = link.find("a", {"class": "targeted-link link icon icon-after icon-external"})
                applications['Contact'] = suite['href']
                worksheet.write("A" + str(count), applications['Name'])
                worksheet.write("B" + str(count), applications['Company'])
                worksheet.write("C" + str(count), applications['Contact'])
                print(applications['Name'])
                print(applications['Company'])
                print(applications['Contact'])
                print()
                count += 1
            game_count += 1
        page += 1
    except Exception:
        print(Exception, " ERROR")
        continue


workbook.close()