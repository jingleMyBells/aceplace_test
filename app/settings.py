import os


class Config:
    MONGO_INITDB_DATABASE = os.getenv('DB_URI', 'mongodb://db:27017/user_db')
    EMAIL = os.getenv('EMAIL')
    NOTIFICATIONS_MAX_COUNT = os.getenv('NOTIFICATIONS_MAX_COUNT', 10)
    MAIL_SERVER = os.getenv('SMTP_HOST')
    MAIL_PORT = os.getenv('SMTP_PORT')
    MAIL_USERNAME = os.getenv('SMTP_LOGIN')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('SMTP_EMAIL')
    SMTP_NAME = os.getenv('SMTP_NAME')
