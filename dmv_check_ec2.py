#!/usr/bin/python3

import bs4 as bs
import requests
import lxml
import datetime as dt
import boto3

def pull_data():
    resp = requests.get('https://www.dmv.ca.gov/portal/make-an-appointment/')
    soup = bs.BeautifulSoup(resp.text, features="lxml")
    qotd = [ soup.find_all('p')[0].get_text() ]
    return qotd

def sns_away():
    sns = boto3.client('sns', region_name='us-east-1')
    numbers = [ '+15555555' ]
    [ sns.publish(PhoneNumber = number, Message='CA DMV might accept APPOINTMENTS!' ) for number in numbers ]

def main():
    ''' One more covid-19 inconvenience solved with science. '''
    out = '/root/dmv_scrape.o'
    search_str = 'New appointments are not currently available'
    pulled = pull_data()
    if search_str in pulled[0]:
        rn = str(dt.datetime.now())
        with open(out, 'a') as f:
            f.write('{} - DMV appointments still constipated\n'.format(rn))
    else:
        sns_away()

if __name__ == '__main__':
    main()
