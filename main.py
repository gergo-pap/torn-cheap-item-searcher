import json
import requests
import time
import webbrowser
from plyer import notification
import pyperclip
import database

api_key = 'AZUBtdoak55AXIfq'
api_url = 'https://api.torn.com/user/?selections=personalstats&key=%s' % api_key
url_base = 'https://www.torn.com/imarket.php#/p=shop&step=shop&type=&searchname='

best_items_list = []
obj = json.loads(requests.get(api_url).text)['personalstats']
itemsURL = 'https://api.torn.com/torn/?selections=items&key=%s' % api_key

TornItems = json.loads(requests.get(itemsURL).text)['items']


item_best_buy_list = [
    "Book of Carols", "Business Class Ticket", "Donator Pack", "Drug Pack",
    "Erotic DVD", "Feathery Hotel Coupon", "Gift Card", "Lawyer Business Card",
    "Lottery Voucher", "Six Pack of Alcohol", "Xanax", "Six Pack of Energy Drink", "Lawyer Business",
    #"Empty Blood Bag", "Blood Bag : A+", "Blood Bag : A-", "Blood Bag : B+", "Blood Bag : B-",
    #"Blood Bag : AB+", "Blood Bag : AB-", "Blood Bag : O+", "Blood Bag : O-", "Blood Bag : Irradiated",
    "Can of Munster", "Can of Red Cow", "Can of Taurine Elite", "Can of Santa Shooters", "Can of Rockstar Rudolph",
    "Can of X-MASS", "Can of Goose Juice", "Can of Damp Valley", "Can of Crocozade"
]

class Item:
    def __init__(self, item_id, item_name, item_type, item_value):
        self.item_id = item_id
        self.item_name = str(item_name)
        self.item_type = item_type
        self.item_path = url_base + str(item_name).replace(' ', '+')
        self.item_value = item_value


class ActiveItem:
    def __init__(self, item_id, item_name, cheapest_value, cheapest_quantity, second_value):
        self.item_id = int(item_id)
        self.item_name = str(item_name)
        self.cheapest_value = int(cheapest_value)
        self.cheapest_quantity = int(cheapest_quantity)
        self.second_value = int(second_value)
        self.profit = int((second_value - cheapest_value) * cheapest_quantity)
        self.sum = int(self.cheapest_quantity * self.cheapest_value)
        self.profit_percent = str("{0:.00%}".format(self.profit / self.sum))
        self.item_path = url_base + str(item_name).replace(' ', '+')


def get_best_items():
    for x in TornItems:
        new_item = Item(x, TornItems[x]['name'], TornItems[x]['type'], TornItems[x]['market_value'])
        if TornItems[x]['name'] in item_best_buy_list:
            print(x, " - ", new_item.item_name, "type:", new_item.item_type, 'value:', new_item.item_value)
            best_items_list.append(new_item)

    print('Number of items: ', len(best_items_list))


def loop(item_list):
    # getTornItems
    while True:
        # Search for item
        start_search = time.time()
        print()
        for item in item_list:
            search(item)
        end = time.time()
        print(round(end - start_search, 2), " sec")


def search(Item):
    start_search = time.time()

    # getBazaarPrices
    bazaar_url = 'http://api.torn.com/market/%s?selections=bazaar&key=%s' % (Item.item_id, api_key)
    bazaar_prices = json.loads(requests.get(bazaar_url).text)['bazaar']


    #a --> instance of the active item
    a = ActiveItem(Item.item_id, Item.item_name, bazaar_prices[0]['cost'],
                    bazaar_prices[0]['quantity'], bazaar_prices[1]['cost'])

    if int(a.profit_percent.replace('%', '')) > 3 or a.profit > 200000 and a.sum < 200000000:
    #if not database.check_row(a):
        #add data to database
        database.add_record(a)
        match(a)
    end = time.time()
    #if the check was too fast, slow it down
    if end - start_search < 0.8:
        time.sleep(0.4)
    #print a dot to console after each item check
    print("-", end='')


def match(ActiveItem):
        #copy sum to clipboard, to get money faster from vault
        pyperclip.copy(str(ActiveItem.sum))

        #windows notification
        notify_me(ActiveItem.item_name, str(ActiveItem.profit))

        #open link in browser
        webbrowser.open_new_tab(ActiveItem.item_path)

        print(f'\tID:{ActiveItem.item_id} - {ActiveItem.item_name} - profit in percent:{"{0:.0%}".format(ActiveItem.profit)}')

        #sleep, in order to have time to buy the cheap item
        time.sleep(9)


def notify_me(item_name, profit):
    notification.notify(
        title="Cheap " + item_name,
        message="Profit: " + profit,
        timeout=5
    )


if __name__ == "__main__":
    database.create_table()
    get_best_items()
    loop(best_items_list)

