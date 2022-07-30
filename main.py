# Imports
import argparse
import csv
from datetime import timedelta, datetime, date
import calendar
from rich.console import Console
from rich.table import Table
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table as Table2, TableStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"
# Your code below this line.


def get_date():
    file_contents = open("date_now.txt", "r").read()
    return file_contents


def advance_time(days_to_increase):
    """ advances todays date
    arguments:
    current_date: todays date
    args: command line args
    """
    try:
        days_to_increase = int(days_to_increase)
        current_date = get_date()
        dt = datetime.strptime(current_date, '%Y-%m-%d')
        if days_to_increase == 0:
            current_date = date.today().strftime('%Y-%m-%d')
            print(current_date)
        else:
            yesterday = dt + timedelta(days=days_to_increase)
            current_date = yesterday.strftime('%Y-%m-%d')
        file = open("date_now.txt", "w")
        file.write(current_date)
        file.close()
        console = Console()
        text = str("Date is set to: " + current_date)
        console.print(text, style="bold magenta", highlight=False)
    except ValueError:
        print("Please insert integer as argument")

# Get products in stock
def get_stock(sold):
    with open('bought.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        all_rows = []
        for row in csv_reader:
            all_rows.append(row)
        return all_rows

# Get products sold
def get_sold():
    with open('sold.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        all_rows = []
        for row in csv_reader:
            all_rows.append(row)
        return all_rows


# Get revenue report
def report_revenue(current_date, args):
    """ reports revenue
    arguments:
    current_date: todays date
    args: command line args
    """
    revenue = 0
    month = 0
    date_name = 0
    if args.today:
        report_date = current_date
        date_name = 'today'
    elif args.yesterday:
        report_date = (datetime.strptime(current_date, '%Y-%m-%d') +
                       timedelta(days=-1)).strftime('%Y-%m-%d')
        date_name = 'yesterday'
    elif args.date:
        report_date = args.date
        if len(args.date) == 7:
            month = 1
            date_name = (calendar.month_name[int(args.date[5:])])
    with open('sold.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if month == 1:
                date_string = row[2][:-3]
            else:
                date_string = row[2]
            if date_string == report_date:
                revenue += float(row[-1])
    console = Console()
    if date_name == 'today':
        text = "Today's revenue so far: " + str(revenue)
    elif date_name == 'yesterday':
        text = str("Yesterday's revenue: " + str(revenue))
    elif month == 1:
        text = "Revenue in " + date_name + ": " + str(revenue)
    else:
        text = str("Revenue on " + report_date + ": " + str(revenue))
    console.print(text, style="bold magenta", highlight=False)

# Get inventory report
def report_inventory(current_date, stock, args, sold):
    """ reports inventory
    arguments:
    current_date: todays date
    stock: current stock
    args: command line args
    sold: sold items
    """
    table = []
    if args.today:
        report_date = current_date
    elif args.yesterday:
        report_date = (datetime.strptime(current_date, '%Y-%m-%d') +
                       timedelta(days=-1)).strftime('%Y-%m-%d')
    elif args.date:
        report_date = args.date
    console = Console()
    if args.pdf:
        styles = getSampleStyleSheet()
        flowables = []
        doc = SimpleDocTemplate(
            "Inventory " + report_date + ".pdf", pagesize=A4)
        title = "Inventory " + report_date
        para = Paragraph(title, style=styles["Normal"])
        spacer = Spacer(1, 2*cm)
        flowables.append(para)
        flowables.append(spacer)
        tblstyle = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.magenta)
        ])
        data = [["ID", "Product Name", "Buy Date",
                "Buy Price", "Expiration Date"]]
        for item in (stock):
            if item[2] <= report_date and item[4] >= report_date and item[0] != 'id':
                data.append(item)
        tbl = Table2(data)
        tbl.setStyle(tblstyle)
        flowables.append(tbl)
        doc.build(flowables)
        text = str("Report saved as PDF")
        console.print(text, style="bold magenta", highlight=False)
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=4)
        table.add_column("Product Name")
        table.add_column("Buy Date")
        table.add_column("Buy Price")
        table.add_column("Expiration Date")
        for item in (stock):
            if sold != []:
                sold_list = [row[1] for row in sold]
                #print(sold_list)
                if item[0] not in sold_list:
                    if item[2] <= report_date and item[4] >= report_date and item[0] != 'id':
                        table.add_row(*item)
            else:
                if item[2] <= report_date and item[4] >= report_date and item[0] != 'id':
                            table.add_row(*item)
        console.print(table)

# Get profit report
def report_profit(current_date, args):
    """ combines revenue and price bougt for the calculate profit
    arguments:
    current_date: todays date
    args: command line args
    """
    bought_sum = 0
    revenue = 0
    profit = 0
    month = 0
    date_name = 0
    if args.today:
        report_date = current_date
        date_name = 'today'
    elif args.yesterday:
        report_date = (datetime.strptime(current_date, '%Y-%m-%d') +
                       timedelta(days=-1)).strftime('%Y-%m-%d')
        date_name = 'yesterday'
    elif args.date:
        report_date = args.date
        if len(args.date) == 7:
            month = 1
            date_name = (calendar.month_name[int(args.date[5:])])
    with open('sold.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if month == 1:
                date_string = row[2][:-3]
            else:
                date_string = row[2]
            if date_string == report_date:
                revenue += float(row[-1])
    with open('bought.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if month == 1:
                date_string = row[2][:-3]
            else:
                date_string = row[2]
            if date_string == report_date:
                bought_sum += float(row[3])
    profit = revenue - bought_sum
    console = Console()
    if date_name == 'today':
        text = "Today's profit so far: " + str(profit)
    elif date_name == 'yesterday':
        text = str("Yesterday's profit: " + str(profit))
    elif month == 1:
        text = "Profit in " + date_name + ": " + str(profit)
    else:
        text = str("Profit on " + report_date + ": " + str(profit))
    console.print(text, style="bold magenta", highlight=False)

# buy item
def buy_item(id, product_name, buy_date, price, expiry):
    """ buys products
    arguments:
    id: product id
    product_name: name of product
    buy_date: date on which bought
    price: price of product bought for
    expiry: date on which the product expires
    """
    with open('bought.csv', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([id, product_name, buy_date,
                        price, expiry])
    console = Console()
    text = str("New item bought: " + product_name)
    console.print(text, style="bold magenta", highlight=False)

# sell item
def sell_item(id, product_name, product_price, current_date, stock, sold):
    """ checks if product is in stock and when it is the product is added to the sold list
    arguments:
    id: product id
    product_name: name of product
    product_price: price of product 
    current_date: date set as current
    stock: product stocklist
    sold: product soldlist 
    """
    console = Console()
    bought_list = []
    sold_list = []
    for item in stock:
        if item[1] == product_name:
            bought_list.append(item[0])
    if bought_list != []:
        for item in bought_list:
            for item_sold in sold:
                if int(item_sold[1]) == int(item):
                    sold_list.append(item)
    available_to_sell = set(bought_list) ^ set(sold_list)
    if len(available_to_sell) != 0:
        for item in stock:
            if item[0] in available_to_sell:
                product = item
                with open('sold.csv', mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([id, product[0], current_date, product_price])
                    text = str("New item sold: " + product_name)
                    console.print(text, style="bold magenta", highlight=False)
                break
    else:
        text = str("ERROR: Product not in stock: " + product_name)
        console.print(text, style="bold red", highlight=False)

 


def parser():
    """ builds the parsers
    returns: args parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    parser.add_argument('--advance-time', 
                        help='advance time by inserted amount of days')
    # Build Buy Parser:
    buy_parser = subparsers.add_parser(
        'buy', help='register purchased product')
    buy_parser.add_argument('--product-name', help='insert product name')
    buy_parser.add_argument('--price', type=float, help='insert buy price')
    buy_parser.add_argument(
        '--expiration-date', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help='insert date as: YYYY-MM-DD')

    # Build Sell Parser:
    sell_parser = subparsers.add_parser('sell', help='register sold product')
    sell_parser.add_argument('--product-name', help='insert product name')
    sell_parser.add_argument('--price', type=float, help='insert sell price')

    # Build Report Parser:
    report = subparsers.add_parser('report', help='report transactions')
    report_subparsers = report.add_subparsers(dest='parser_report')
    inventory = report_subparsers.add_parser('inventory', help='inventory')
    revenue = report_subparsers.add_parser('revenue', help='revenue')
    profit = report_subparsers.add_parser('profit', help='profit')
    inventory.add_argument('--today', action='store_true',
                           help='show current report')
    inventory.add_argument('--yesterday', action='store_true',
                           help='show yesterday\'s report')
    inventory.add_argument('--pdf', action='store_true',
                           help='output report in PDF file')
    inventory.add_argument(
        '--date', help='show report from given date: insert date as: YYYY-MM-DD')
    revenue.add_argument('--yesterday', action='store_true',
                         help='show yesterday\'s report')
    revenue.add_argument('--today', action='store_true',
                         help='show today\'s report')
    revenue.add_argument(
        '--date', help='show report from given date: insert date as: YYYY-MM or YYYY-MM-DD')
    profit.add_argument('--today', action='store_true',
                        help='show today\'s report')
    profit.add_argument('--yesterday', action='store_true',
                        help='show today\'s report')
    profit.add_argument(
        '--date', help='show report from given date: insert date as: YYYY-MM or YYYY-MM-DD')
    return parser.parse_args()

def main():
    # Current date, stock en sold items:
    current_date = get_date()
    sold = get_sold()
    stock = get_stock(sold)
    
    # Get ID's:
    try:
        last_item_id = int(stock[-1][0])
    except ValueError:
        last_item_id = 1
    try:
        last_item_id_sold = int(sold[-1][0])
    except IndexError:
        last_item_id_sold = 0

    args = parser()
    if args.advance_time:
        advance_time(args.advance_time)
    if args.action == 'buy':
        buy_item(last_item_id + 1, args.product_name,
                 get_date(), args.price, args.expiration_date.date())
    if args.action == 'sell':
        sell_item(last_item_id_sold + 1, args.product_name,
                  args.price, get_date(), stock, sold)
    if args.action == 'report':
        if args.parser_report == 'revenue':
            report_revenue(current_date, args)
        elif args.parser_report == 'inventory':
            report_inventory(current_date, stock, args, sold)
        elif args.parser_report == 'profit':
            report_profit(current_date, args)


if __name__ == "__main__":
    main()
