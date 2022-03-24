from bs4 import BeautifulSoup
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

startingUrl = "https://fontawesome.com/search?m=free"


def getCategoryUrl(category):
    template = 'https://fontawesome.com/search?m=free&c={}'
    category = category.replace('_', '-').replace('0', '-')
    return template.format(category)


def getCategoryNameFromLiTag(liTag):
    rawCategoryName = liTag.label.find('span', {
        'class': 'text-capitalize'
    }).text
    return rawCategoryName.lower().replace(' ', '_').replace('_+_', '0')


def getIconId(icon):
    iconIdSpan = icon.button.span
    return iconIdSpan.text


# Opens the browser and gets all available categories.
driver.get(startingUrl)
categoriesSoup = BeautifulSoup(driver.page_source, 'html.parser')
categoriesLi = categoriesSoup.find('ul', {
    'class': 'icons-facets-group-categories'
}).find_all('li')

categoryList = []
categoryRecords = {}
iconsCounter = 0

print('Getting all available categories:')
for li in categoriesLi:
    categoryName = getCategoryNameFromLiTag(li)
    if (categoryName == "genders"):
        categoryName = "gender"
    if (categoryName == "disaster0crisis"):
        categoryName = "disaster"
    categoryList.append(categoryName)
    print('➥ ' + categoryName)

for category in categoryList:
    print('Redirecting to ' + category + ' icons page...')
    driver.get(getCategoryUrl(category))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('article', {'class': 'wrap-icon'})
    categoryRecords[category] = {
        'icons': [],
        'label': category.title().replace('_', ' ').replace('0', ' + ')
    }
    print('Adding icons to category:')
    for icon in results:
        iconsCounter += 1
        iconId = getIconId(icon)
        categoryRecords[category]['icons'].append(iconId)
        print('➥ ' + iconId)
    print('Done ✓')

print('Finished scraping for categories and icons')
print(f'Parsed {iconsCounter} icons from {len(categoryList)} categories')
print('Creating category file')

with open("categories.json", "w") as outfile:
    json.dump(categoryRecords, outfile)

print('Finished ✓')
driver.close()
