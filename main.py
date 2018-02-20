import requests
from bs4 import BeautifulSoup
import xlsxwriter


'''
Для тестов
z = "https://itunes.apple.com/us/app/abc-puzzle-preschool-kindergarten-early-learning-games/id1110123626?mt=8"

x = requests.get(z)
obj = BeautifulSoup(x.text, "html.parser")

print(obj.find("h1", {"class": "product-header__title"}))

'''

workbook = xlsxwriter.Workbook("List.xlsx")
worksheet = workbook.add_worksheet()

worksheet.write("A1", "Game")
worksheet.write("B1", "Company")
worksheet.write("C1", "Contact")

page = "https://itunes.apple.com/us/genre/ios-games/id6014?mt=8&letter=A&page=1#page"

text = requests.get(page)
bsObj = BeautifulSoup(text.text, "html.parser")

#listLink = bsObj.find("div", {"id": "selectedcontent"}).findAll("a")
allPage = bsObj.find("ul", {"class": "list paginate"}).findAll("a")

applications = {}

count = 2
game_count = 1
page = 1

for suchka in allPage:
    print("PAGE: ", page)
    main_page = BeautifulSoup((requests.get(suchka['href'])).text, "html.parser")
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


workbook.close()