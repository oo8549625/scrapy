import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_apscheduler import APScheduler
from datetime import datetime
import time
import smtp
import scrapy
import openpyxl
import csv
import logging

UPLOAD_FOLDER = os.path.dirname(__file__)
ALLOWED_EXTENSIONS = set(['csv'])
# os.environ.get('LOG_DIR')
# os.path.dirname(__file__)
app = Flask(__name__)
logging.basicConfig(filename=os.path.join(
    os.environ.get('LOG_DIR'), 'flask.log'), level=logging.INFO)


def search_price():
    with open('search.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        next(rows)
        prods = {}
        # 以迴圈輸出每一列
        app.logger.info(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + ' searching prod price')
        for row in rows:
            if row[1]:
                if scrapy.search_prods(row[0], row[1]):
                    prods[row[0]] = scrapy.search_prods(row[0], row[1])
                    prod = prods[row[0]]
                    app.logger.info(datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' prod: ' + row[0] + ',\tprice: ' + str(prod['price']) + ',\tlowestPrice: ' + str(prod['lowestPrice']))

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet['A1'] = '型號'
        sheet['B1'] = '牌價'
        sheet['C1'] = '最低價'
        sheet['D1'] = 'URL'
        sheet['E1'] = '搜尋日期'

        count = 1
        app.logger.info(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + ' writing to xlsm file')
        for prod in prods:
            count += 1
            sheet['A' + str(count)] = prod
            sheet['B' + str(count)] = prods[prod]['price']
            sheet['C' + str(count)] = prods[prod]['lowestPrice']
            sheet['D' + str(count)
                  ] = 'https://ecshweb.pchome.com.tw/search/v3.3/?q={}'.format(prod)
            sheet['E' + str(count)] = prods[prod]['date']
            if prods[prod]['is_welfare']:
                sheet['F' + str(count)] = '福利品'

        workbook.save('result.xlsx')
        app.logger.info(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + ' sending email')
        smtp.send_email()


def allowed_file(filename):
    return 'search' in filename and '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@ app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                            ' search.csv save in path: ' + os.path.join(UPLOAD_FOLDER, filename))
            file.save(os.path.join(UPLOAD_FOLDER,
                                   filename))
            return "OK"
    # GET return
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': search_price,
            'args': '',
            'trigger': 'cron',
            'hour': '10',
            'minute': '50',
        },
        {
            'id': 'job2',
            'func': search_price,
            'args': '',
            'trigger': 'cron',
            'hour': '16',
            'minute': '50',
        },
        {
            'id': 'job3',
            'func': search_price,
            'args': '',
            'trigger': 'cron',
            'hour': '23',
            'minute': '30',
        }
    ]

    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB

scheduler = APScheduler()
# it is also possible to enable the API directly
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.info')
    app.logger.handlers = gunicorn_logger.handlers
