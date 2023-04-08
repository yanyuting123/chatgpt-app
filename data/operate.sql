-- Active: 1680848296124@@127.0.0.1@3306

CREATE TABLE
    highschool_words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT
    );

-- ALTER TABLE my_table ADD COLUMN new_column_name INTEGER;

.import Highschool.txt highschool_words 