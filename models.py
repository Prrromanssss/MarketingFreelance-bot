import psycopg2
import config


class UserData:
    def __init__(self, name):
        self.name = name

    def db_insert(self, message):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        username = message.from_user.username
        val = (username,)
        sql_query = f'SELECT username FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        if cursor.fetchall():
            return
        sql_query = f'INSERT INTO {config.DB_TABLE} ("username") VALUES (%s)'
        cursor.execute(sql_query, val)
        conn.commit()

    def db_select(self, message):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        sql_query = f'SELECT username FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        usernames = cursor.fetchall()
        conn.commit()
        return usernames


db_object = UserData(config.DB_URI)
