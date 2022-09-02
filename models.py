import config
import sqlite3


class UserData:
    def __init__(self, name):
        self.name = name

    def db_insert(self, message):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        username = message.from_user.username
        val = (username, message.chat.id)
        sql_query = f'SELECT username FROM {config.DB_TABLE} WHERE user_id = ?'
        cursor.execute(sql_query, (message.chat.id,))

        if cursor.fetchall():
            return
        sql_query = f'INSERT INTO {config.DB_TABLE} ("username", user_id) VALUES (?, ?)'
        cursor.execute(sql_query, val)
        conn.commit()

    def db_select_user(self, message, callback=False):
        if callback:
            message = message.message
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        val = (message.chat.id, )
        sql_query = f'SELECT username FROM {config.DB_TABLE} WHERE user_id = ?'
        cursor.execute(sql_query, val)
        username = cursor.fetchall()[0][0]
        conn.commit()
        return username

    def db_select_user_id(self, username):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        val = (username,)
        sql_query = f'SELECT user_id FROM {config.DB_TABLE} WHERE username = ?'
        cursor.execute(sql_query, val)
        user_id = cursor.fetchall()[0][0]
        conn.commit()
        return user_id

    def db_select_all_users(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        sql_query = f'SELECT username FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        usernames = cursor.fetchall()
        conn.commit()
        return usernames

    def db_select_all_users_id(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        sql_query = f'SELECT "user_id" FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        users_id = cursor.fetchall()
        conn.commit()
        return users_id


db_object = UserData(config.DB_URI)
