import sqlite3

word_path = 'words/TOEFL_word.txt'
word_source = 'toefl_words'

with open(word_path, encoding='utf-8') as file:
    words = file.read().split(' ')

# Connect to the database
conn = sqlite3.connect('data/data.db')
c = conn.cursor()



c.execute(f'''CREATE TABLE {word_source} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT
    );''')
# Insert each word into the table
for word in words:
    c.execute(f"INSERT INTO {word_source} (word) VALUES (?)", (word,))

# Commit the changes and close the connection
conn.commit()
c.close()
conn.close()