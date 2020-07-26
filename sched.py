import schedule  
import time
from datetime import datetime
import smtp
import scrapy
import openpyxl
import csv

def date_now():
    print('date: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def search_price():
    with open('search.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        next(rows)
        prods = {}
        # 以迴圈輸出每一列
        for row in rows:
            if row[1]:
                if scrapy.search_prods(row[0], row[1]):
                    prods[row[0]] = scrapy.search_prods(row[0], row[1])

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet['A1'] = '型號'
        sheet['B1'] = '牌價'
        sheet['C1'] = '最低價'
        sheet['D1'] = 'URL'
        sheet['E1'] = '搜尋日期'

        count = 1
        for prod in prods:
            count += 1
            sheet['A' + str(count)] = prod
            sheet['B' + str(count)] = prods[prod][price]
            sheet['C' + str(count)] = prods[prod][lowestPrice]
            sheet['D' + str(count)
                ] = 'https://ecshweb.pchome.com.tw/search/v3.3/?q={}'.format(prod)
            sheet['E' + str(count)] = prods[prod][date]

        workbook.save('result.xlsx')
        smtp.send_email()

schedule.every().day.at("10:30").do(search_price)
schedule.every().day.at("16:30").do(search_price)
schedule.every(1).minutes.do(date_now)

while True:
    schedule.run_pending()
    time.sleep(1)
