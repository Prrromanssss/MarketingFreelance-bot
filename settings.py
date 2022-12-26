import os

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN', 'summy-dummy-token')

YOO_TOKEN = os.environ.get('YOO_TOKEN', 'summy-dummy-token')

APP_URL = os.environ.get('APP_URL', 'summy-dummy-url')

DB_URI = 'dbsqlite3.db'

ADMINS = {
          'qzark': os.environ.get(
            'ADMIN_QZARK_CHAT_ID',
            'summy-dummy-chat-id'
            ),
          'decotto': os.environ.get(
            'ADMIN_DECOTTO_CHAT_ID',
            'summy-dummy-chat-id'
            ),
          'sourr_cream': os.environ.get(
            'ADMIN_SOURR_CREAM_CHAT_ID',
            'summy-dummy-chat-id'
            ),
          'zakazy': os.environ.get(
            'ADMIN_GROP_ZAKAZY_CHAT_ID',
            'summy-dummy-chat-id'
            ),
         }

CHAT_ID_BOT = os.environ.get('CHAT_ID_BOT', 'summy-dummy-chat-id')

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'summy-dummy-password')

CONTENT_TYPES = [
    'text', 'audio', 'photo',
    'sticker', 'video', 'video_note', 'voice',
    'location', 'contact', 'venue'
    ]

SITE_HASH_FILE_ID = os.environ.get('SITE_HASH_FILE_ID', 'summy-dummy-file-id')

DESIGN_HASH_FILE_ID = os.environ.get('ADMIN_PASSWORD', 'summy-dummy-file-id')
