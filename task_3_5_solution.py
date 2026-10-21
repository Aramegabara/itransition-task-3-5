import json, re, sqlite3

EUR_TO_USD = 1.2

with open('task1_d.json', 'r', encoding='utf-8') as f:
    data = f.read()

fixed_data = re.sub(r':(\w+)=>', r'"\1":', data)
records = json.loads(fixed_data)


def convert_to_usd(price):
    if price.startswith("€"):
        return round(float(price[1:]) * EUR_TO_USD, 2)
    else:
        return float(price[1:])


for record in records:
    price = record['price']
    converted_price = convert_to_usd(price)
    record['price_usd'] = converted_price

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

rows = [(str(record['id']), record['title'], record['author'], record['genre'], record['publisher'], record['year'], record['price'], record['price_usd']) for record in records]

cursor.executemany(INSERT_SQL, rows)
connection.commit()

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
connection.close()