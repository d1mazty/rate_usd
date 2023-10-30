import requests

from flask import Flask
import gspread

app = Flask(__name__)


@app.route('/')
def main():
    gc = gspread.service_account(filename='/home/d1mazty/rate_usd/creds.json')
    sh = gc.open_by_key('1Pm5FXgA0oFdp_sn45r4JMKA4aR4V0iQb5CV0WD_a3xw')

    worksheet_1 = sh.get_worksheet_by_id(1028033322)
    date_from_to = worksheet_1.get('B1:B2')
    date_from = ''.join(date_from_to[0][0].split('.')[::-1])
    date_to = ''.join(date_from_to[1][0].split('.')[::-1])

    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={date_from}&end={date_to}&valcode=usd&sort=exchangedate&order=asc&json'
    response = requests.get(url)

    rates = []
    if response.status_code == 200:
        data = response.json()
        rates = [[row['exchangedate'], row['rate']/100] for row in data]

    worksheet_2 = sh.get_worksheet_by_id(70376639)
    worksheet_2.batch_clear(['A3:B'])
    worksheet_2.update(values=rates, range_name='A3:B')

    return 'Курс оновлено'