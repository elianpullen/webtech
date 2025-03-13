import sqlite3

# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Example query to fetch data
cursor.execute("SELECT * FROM user")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
