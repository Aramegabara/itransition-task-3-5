import json, re, sqlite3

# with open('task1_d.json', 'r') as f:
#     data = json.load(f)

# print(type(data))
EUR_TO_USD = 1.2

with open('task1_d.json', 'r', encoding='utf-8') as f:
    data = f.read()

list_of_keys = []

for key in re.findall(r':\w+=>', data):
    if key not in list_of_keys:
        list_of_keys.append(key)

# print(f"List of keys: {list_of_keys}")

for key in list_of_keys:
    count = data.count(key)
    # print(f"Count of '{key}': {count}")

fixed_data = re.sub(r':(\w+)=>', r'"\1":', data)
records = json.loads(fixed_data)
# print(len(records))


# print(records[0])

# print(data[:300])
# print(set(r['price'][0] for r in records))

# print(f"price: {records[234]['price']}")
# print(ascii(records[234]['price']))
# print(f"price: {records[234]['price'].encode('cp1252').decode('utf-8')}")
# print(f"price: {records[234]['price']}")
# print(records[0]['price'][0])
# print(float(records[0]['price'][1:]))

def convert_to_usd(price):
    if price.startswith("€"):
        # converted_price = round(float(price[1:]) * EUR_TO_USD, 2)
        # return "$" + str(converted_price)
        return round(float(price[1:]) * EUR_TO_USD, 2)
    else:   
        # return price
        return float(price[1:])

# a = records[274]['price']
# print  (a)
# print(convert_to_usd(a))


if key == ':price=>':
    for record in records:
        price = record['price']
        converted_price = convert_to_usd(price)
        # print(f"Original price: {price}, Converted price: {converted_price}")
        record['price_usd'] = converted_price
# print(records[234]['price'], records[234]['price_usd'])


# print(records[0])
# print(records[0].keys())

# CREATE TABLE IF NOT EXISTS books ( 
#     id TEXT PRIMARY KEY,
#     title TEXT,
#     author TEXT,
#     genre TEXT,
#     publisher TEXT,
#     year INTEGER,
#     price TEXT,
#     price_usd REAL
# );

connection = sqlite3.connect('books.db')
cursor = connection.cursor()
CREATE_BOOKS_SQL = """CREATE TABLE IF NOT EXISTS books ( 
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    publisher TEXT,
    year INTEGER,
    price TEXT,
    price_usd REAL
);"""
INSERT_SQL = "INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
cursor.execute(CREATE_BOOKS_SQL)

rows = [ (str(record['id']), record['title'], record['author'], record['genre'], record['publisher'], record['year'], record['price'], record['price_usd']) for record in records ]
print(f"{len(rows)} + {rows[0]}")

cursor.executemany(INSERT_SQL, rows)
connection.commit()

# cursor.execute("SELECT COUNT(*) FROM books")
# print(cursor.fethall())

COUNT_YEAR = "SELECT year, COUNT(*) FROM books GROUP BY year"
# cursor.execute(COUNT_YEAR)
# print(cursor.fetchall())

# MIDLE_PRICE = """
# SELECT year, COUNT(*) AS book_count, ROUND(AVG(price_usd), 2) AS averege_price
# FROM books
# GROUP BY year"""
# cursor.execute(MIDLE_PRICE)
# print(cursor.fetchall())

CREATE_BOOK_SUMMARY = """
CREATE TABLE book_summary AS
SELECT year, COUNT(*) AS book_count, ROUND(AVG(price_usd), 2) AS average_price
FROM books
GROUP BY year"""
cursor.execute("DROP TABLE IF EXISTS book_summary")
cursor.execute(CREATE_BOOK_SUMMARY)
connection.commit()

cursor.execute("SELECT COUNT(*) FROM book_summary")
print(cursor.fetchall())
cursor.execute("SELECT SUM(book_count) FROM book_summary")
print(cursor.fetchall())