# Imports
import argparse
import csv
import datetime
import pandas as pd
from pandas import read_csv
import os
import os.path
import numpy as np
# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'
# Your code below this line.
def main():
    pass
# Store current date, current time and yesterday's date in variables:
now = datetime.datetime.now()
today = datetime.datetime.today().strftime("%Y-%m-%d")
yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
# Parsers:
parser = argparse.ArgumentParser(
    description='Keep track of your inventory.',
    formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers(dest='command')
# advance time argument:
parser.add_argument('--advance-time', type=int, help='advance time by inserted amount of days')
# Buy Parser:
buy_parser = subparsers.add_parser('buy', help='register purchased product')
buy_parser.add_argument('--product-name', help='insert product name')
buy_parser.add_argument('--price', type=float, help='insert buy price')
buy_parser.add_argument('--expiration-date', type=datetime.date.fromisoformat, help='insert date as: YYYY-MM-DD')
# Sell Parser:
sell_parser = subparsers.add_parser('sell', help='register sold product')
sell_parser.add_argument('--product-name', help='insert product name')
sell_parser.add_argument('--price', type=float, help='insert sell price')
# Report Parser:
report = subparsers.add_parser('report', help='report transactions')
report_subparsers = report.add_subparsers(dest='parser_report')
inventory = report_subparsers.add_parser('inventory', help='inventory')
revenue = report_subparsers.add_parser('revenue', help='revenue')
profit = report_subparsers.add_parser('profit', help='profit')
inventory.add_argument('--now', help='show current report')
inventory.add_argument('--yesterday', help='show yesterday\'s report')
revenue.add_argument('--yesterday', action='store_true', help='show yesterday\'s report')
revenue.add_argument('--today', action='store_true', help='show today\'s report')
revenue.add_argument('--date', help='show report from given date: insert date as: YYYY-MM')
profit.add_argument('--today', help='show today\'s report')
args = parser.parse_args()
# Function to create csv files if they don't exist.
def create_csv_files():
    if not os.path.exists('data.csv'):
        with open('data.csv', 'w'):
            pass
    if not os.path.exists('bought.csv'):
        with open('bought.csv', 'a') as bought_file:
            headers = ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
            writer = csv.DictWriter(bought_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            pass
    if not os.path.exists('sold.csv'):
        with open('sold.csv', 'a') as sold_file:
            headers = ['id', 'bought_id', 'sell_date', 'sell_price']
            writer = csv.DictWriter(sold_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            pass
    if not os.path.exists('inventory.csv'):
        with open('inventory.csv', 'a') as inventory_file:
            headers = ['product_name', 'count', 'buy_price', 'expiration_date']
            writer = csv.DictWriter(inventory_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            writer.writeheader()
            pass
# Function to load data from csv to dictionary
def load_csv_data():
    with open('data.csv', 'r') as data:
        for line in csv.DictReader(data):
            return line
# Function to advance time.
def advance_time():
    if args.advance_time:
        n = args.advance_time
        new_day = (datetime.datetime.today() + datetime.timedelta(days=n)).strftime("%Y-%m-%d")
        global today
        today = new_day # overwrite today with new_day
        print('OK')
# Buy function to write to bought.csv:
def buy_to_csv():
    if args.command == 'buy':
        product_name = args.product_name
        buy_price = args.price
        expiration_date = args.expiration_date
        bought_id = 0
        with open('data.csv', 'a', newline='') as data:
            buy_dict = {'id': bought_id, 'product_name': product_name, 'buy_date': today, 'buy_price': buy_price, 'expiration_date': expiration_date}
            field_names = ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
            data_writer = csv.DictWriter(data, fieldnames=field_names)
            data_writer.writerow(buy_dict)
        with open('bought.csv', 'a', newline='') as bought_file:
            writer = csv.writer(bought_file)
            for bought_row in open('bought.csv'):
                bought_id += 1
            row = [bought_id, product_name, today, buy_price, expiration_date]
            writer.writerow(row)
        print('OK')  
def sell_to_csv():
    if args.command == 'sell':
        sold_id = 0
        bought_id = 0
        sell_price = args.price
        with open('data.csv', 'a', newline='') as data:
            sell_dict = {'id': sold_id, 'bought_id': bought_id, 'sell_date': today, 'sell_price': sell_price}
            field_names = ['id', 'bought_id', 'sell_date', 'sell_price']
            data_writer = csv.DictWriter(data, fieldnames=field_names)
            data_writer.writerow(sell_dict)
        with open('sold.csv', 'a', newline='') as sold_file:
            writer = csv.writer(sold_file)
            for sold_row in open('sold.csv'):
                sold_id += 1
            with open('bought.csv', 'r', ) as bought_file:
                reader = csv.reader(bought_file)
                for bought_row in reader:
                    if args.product_name in bought_row:
                        bought_id = bought_row[0]
                row = [sold_id, bought_id, today, sell_price]
                writer.writerow(row)
        print('OK')                
# Sell function to write to sold.csv:
       
def report():
    if args.command == 'report':
        sold_csv_path = os.getcwd() + '\\sold.csv'
        sold_csv = read_csv(os.getcwd() + '\\sold.csv')
        if args.parser_report == 'revenue':
            if args.today:
                revenue = sold_csv.loc[sold_csv['sell_date'] == today, 'sell_price'].sum() 
                print(f'Today\'s revenue so far: {revenue}')
            elif args.yesterday:
                revenue = sold_csv.loc[sold_csv['sell_date'] == yesterday, 'sell_price'].sum() 
                print(f'Yesterday\'s revenue: {revenue}')
            elif args.date:
                date = args.date
                set_date = datetime.datetime.strptime(date, "%Y-%m")
                sold_csv.sell_date = pd.to_datetime(sold_csv.sell_date).dt.to_period('m') # convert dates in sell_date column to YYYY-MM only
                year = datetime.datetime.strftime(set_date, "%Y")
                month_name = set_date.strftime('%B')
                revenue = sold_csv.loc[sold_csv['sell_date'] == date, 'sell_price'].sum() # sum prices in sell_price column of given month
                print(f'Revenue from {month_name} {year}: {revenue}')
create_csv_files()     
advance_time()
buy_to_csv()
sell_to_csv()
report()
load_csv_data()
if __name__ == '__main__':
    main()