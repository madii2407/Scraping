import requests
from bs4 import BeautifulSoup
import os
import sys

def imagedown(url, folder, logo_no):
  print("URL: ", url)
  path = os.path.join(os.getcwd(), folder)
  isExist = os.path.exists(path)
  if not isExist:
    os.mkdir(path)
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  images = soup.find_all('img',{'alt': 'Company image'})
  for image in images:
    name = image['alt']
    link = image['src']
    with open(path + "/" + name.replace(' ', '-').replace('/', '') + '_' + str(logo_no) + '.jpg', 'wb') as f:
      im = requests.get('https://www.medicines.org.uk/'+link)
      # f.write(im.content)
      print('Writing: ', name)


page = requests.get("https://www.medicines.org.uk/emc/browse-companies")
soup = BeautifulSoup(page.content, 'lxml')
next_url = ''
def getnextpage(soup):
    logo_no = 0
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'browse'})
    lis = pages.find('li')
    m = pages.find('li')
    n = m.find('a')
    categories = pages.find_all("li")
    for a in pages.find_all('a', href=True):
        x =a['href']
        url = 'https://www.medicines.org.uk/' + str(x)
        page1 = requests.get(url)
        soup1 = BeautifulSoup(page1.content, 'lxml')
        companies_count = len(soup.find_all("a", class_="key"))
        eligible_companies = [0]
        if companies_count > 3:
          eligible_companies.append(2)
        eligible_companies.append(companies_count - 1)
        count = 0
        for p in soup.find_all("a", class_="key"):
          if count in eligible_companies:
            print(str(count) + " is printing")
            next_link = p['href']
            next_url = 'https://www.medicines.org.uk' + str(next_link)
            names=p.getText(strip=True)
            print(names)
            imagedown(next_url,'Logos', logo_no)
            logo_no += 1
          count += 1
          #print(img_url)
          #page = requests.get(img_url)
          #soup = BeautifulSoup(page.content, 'lxml') 
          #print(soup)
          



getnextpage(soup)

