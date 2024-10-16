import requests                # to access source code of html and store in string
import selectorlib             # extract only particular information from source code
from send_email import send_email
import time
import sqlite3 as sql

URL = 'http://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sql.connect('sqldb.db')


def scrape(url):
    '''Scrape the Page Source from the url'''
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value


# def send_email():
#     print("email is sent")


def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("insert into events values(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city , date = row
    cursor = connection.cursor()
    cursor.execute("select * from events where band=? and city=? and date=?", (band,city,date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        
        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="new event found")
        time.sleep(2)