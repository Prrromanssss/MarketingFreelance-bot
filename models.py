import psycopg2
import config


class UserData:
    def __init__(self, name):
        self.name = name

    def db_insert(self, message):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        username = message.from_user.username
        val = (username, message.chat.id)
        sql_query = f'SELECT username FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        if cursor.fetchall():
            return
        sql_query = f'INSERT INTO {config.DB_TABLE} ("username", "user_id") VALUES (%s, %s)'
        cursor.execute(sql_query, val)
        conn.commit()

    def db_select_user(self, message, callback=False):
        if callback:
            message = message.message
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        val = (message.chat.id, )
        sql_query = f'SELECT username FROM {config.DB_TABLE} WHERE user_id = %s'
        cursor.execute(sql_query, val)
        username = cursor.fetchall()[0][0]
        conn.commit()
        return username

    def db_select_all_users(self):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        sql_query = f'SELECT username FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        usernames = cursor.fetchall()
        conn.commit()
        return usernames


db_object = UserData(config.DB_URI)
