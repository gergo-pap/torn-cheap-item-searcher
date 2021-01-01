import sqlite3
import datetime

# connect to db
conn = sqlite3.connect('torn.db')

# create cursor
cursor = conn.cursor()


def create_table():
    conn = sqlite3.connect('torn.db')
    cursor = conn.cursor()

    # create table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER NOT NULL PRIMARY KEY,
                item_id INTEGER,
                item_name TEXT,
                cheapest_value INTEGER,
                cheapest_quantity INTEGER,
                second_value INTEGER,
                profit INTEGER,
                profit_percent TEXT,
                sum_to_buy INTEGER,
                time TEXT
            )
        """)
    conn.commit()
    conn.close()


def check_row(active_item):
    conn = sqlite3.connect('torn.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM data WHERE item_id = {active_item.item_id} "
                   f"AND cheapest_value = {active_item.cheapest_value} "
                   f"AND profit = {active_item.profit} "
                   f"AND sum_to_buy = {active_item.sum}")

    if cursor.fetchone() is None:
        return False
    else:
        print('This item is in the database')
        print(f'{active_item.item_name} {active_item.cheapest_value}')
        return True
    conn.close()


def show_all(print):
    cursor.execute("SELECT * FROM data")
    items = cursor.fetchall()
    # cursor.fetchmany(2)
    # cursor.fetchone()
    if print:
        for item in items:
            print(item)
    return items


def add_record(active_item):
    # connect to db
    conn = sqlite3.connect('torn.db')

    # create cursor
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO data"
                   f"(item_id, item_name, cheapest_value, cheapest_quantity, second_value, profit, profit_percent, sum_to_buy, time)"
                   f"VALUES ('{int(active_item.item_id)}','{str(active_item.item_name)}',"
                   f"'{int(active_item.cheapest_value)}','{int(active_item.cheapest_quantity)}',"
                   f"'{int(active_item.second_value)}','{int(active_item.profit)}',"
                   f"'{str(active_item.profit_percent)}', {int(active_item.sum)},"
                   f"'{str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}')"
                   )
    # commit our comman
    conn.commit()
    conn.close()
    print("Added succesfully")


# close our connection
conn.close()
