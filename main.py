import re
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time

URL = 'https://cnft.tools/yummiuniverse'
HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15', 'accept':'*/*'}
FILE = 'data/naru_tools.csv'
options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15')
options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path='/Users/egororlov/Desktop/naru_parser/chromedriver',
    options=options
)

def get_html(url):
    try:
        driver.get(url)
        time.sleep(2)
        req = driver.page_source
        return req
    except:
        return 'Error'
    # finally:
    #     driver.close()
    #     driver.quit()

def save(list, name):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['rank', 'id', 'price'])
        for i in list:
            writer.writerow([i['rank'], i['number'], i['price']])

def get_content(html):
    print('get content')
    items = []
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find_all('div', class_='zoom showbox')
    for i in data:
        try:
            price = i.find(text=re.compile('ADA')).text.strip()
        except:
            price = 'None'

        items.append({
            'rank': i.find('div').text.strip(),
            'number': i.find(text=re.compile('#')).get_text(strip=True),
            'price': price
        })
    return items

def get_page(count):
    try:
        print('Check page')
        driver.get(f'https://cnft.tools/yummiuniverse?background=x&body=x&face=x&headwear=x&sort=ASC&method=rarity&page={count}&')
        time.sleep(5)

        # driver.find_element_by_xpath('//*[@id="page"]').click()
        #
        # driver.find_element_by_css_selector(f'#page > option:nth-child({count})').click()
        # driver.find_element_by_xpath(f'//*[@id="page"]/option[{count}]').click()
        # time.sleep(2)
        req = driver.page_source
        print(req)
        return req

    except:
        return 'stop'

def parser():
    html = get_html(URL)
    all_items = []
    count = 2
    while count <= 5:
        try:
            all_items.extend(get_content(html))
            html = get_page(count)
            print(f'Parsing {count} page...')
            count += 1
        except Exception as ex:
            print(ex)
            break
        finally:
            save(all_items, FILE)
            driver.quit()
            driver.close()

if __name__ == '__main__':
    parser()
