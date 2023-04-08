import sqlite3
import random

class DBOperator():
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()

    def __del__(self):
        self.c.close()
        self.conn.close()

    def get_wordsource_list(self):
        self.c.execute('select id, name from wordsource')
        id_name = self.c.fetchall()
        return id_name

    def get_wordsource_data(self, id_, name):
        if id_:
            self.c.execute(f'select table_name from wordsource where id={id_}')
        elif name:
            self.c.execute(f'select table_name from wordsource where name={name}')
        data = self.c.fetchall()
        if len(data) > 0:
            table_name = data[0][0]
        else:
            raise Exception(f'Wrong id:{id_} or name:{name}')
        
        self.c.execute(f'select word from {table_name}')
        words = [x[0] for x in self.c.fetchall()]
        return words

    def get_new_words(self, source_id, source_name, number):
        word_list = self.get_wordsource_data(source_id, source_name)
        new_words = random.sample(word_list, number) 
        return new_words


if __name__ == '__main__':
    db = DBOperator('data/data.db')
    lst = db.get_wordsource_list()
    new_words = db.get_new_words(2, 'TOEFL', 10)
    print(lst)
    print(new_words)
