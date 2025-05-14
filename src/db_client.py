import pymysql
from pymysql.cursors import DictCursor
from config import DB_CONFIG


class MySQLClient:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)

    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS quotes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT,
            author VARCHAR(100),
            tags VARCHAR(255),
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
        '''
        with self.conn.cursor() as cur:
            cur.execute(sql)
        self.conn.commit()

    def insert_quotes(self, quotes):
        sql = "INSERT INTO quotes (text, author, tags) VALUES (%s, %s, %s)"
        with self.conn.cursor() as cur:
            data = [(q['text'], q['author'], ','.join(q['tags'])) for q in quotes]
            cur.executemany(sql, data)
        self.conn.commit()

    def close(self):
        self.conn.close()