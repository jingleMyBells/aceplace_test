import logging

from datetime import datetime as dt

from flask_mail import Message

from .constants import KeyEnum
from .exceptions import InvalidAPIUsage, MailingError
from . import app, db, mail


logger = logging.getLogger(__name__)


class Notification:

    def __init__(self, obj):
        self.user_id = obj.get('user_id')
        self.key = obj.get('key')
        self.target_id = obj.get('target_id')
        self.data = obj.get('data')
        self.email = obj.get('email')

    def perform_selected_action_with_data(self):
        choose_key_action(self.key)(self)


def registration(obj: Notification):
    logger.info('registration key was provided')
    email = obj.email
    if email:
        logger.info('email param was provided, trying to send email')
        send_email(obj.key, email)


def new_message(obj: Notification):
    logger.info('new_message key was provided')
    create_notification_record(obj)


def new_post(obj: Notification):
    logger.info('new_post key was provided')
    create_notification_record(obj)


def new_login(obj: Notification):
    logger.info('new_login key was provided')
    create_notification_record(obj)
    email = obj.email
    if email:
        send_email(obj.key, email)


def change_user_notif_status(user_id: str, notif_id: str):
    user_notifications = []

    user = db.users.find_one({'user_id': user_id})
    if user:
        user_notifications = user.get('notifications', [])

    if len(user_notifications) > 0:
        notification = None
        notif_index = None
        for i in range(len(user_notifications)):
            notif = user_notifications[i]
            if notif.get('id') == notif_id:
                notification = notif
                notif_index = i
                break

        if notif_index is not None and notification is not None:
            logger.info('OK. trying to update user doc in db')
            user_notifications.pop(notif_index)
            notification['is_new'] = False
            user_notifications.append(notification)

            db.users.update_one(
                {'_id': user.get('_id')},
                {'$set': {'notifications': user_notifications}},
            )
            return True
    logger.error('no user found')
    return False


def create_notification_record(obj: Notification):
    user_notifications = []

    user = db.users.find_one({'user_id': obj.user_id})
    if user:
        user_notifications = user.get('notifications', [])

    if len(user_notifications) > 0:
        user_notifications.sort(
            key=lambda x: x.get('timestamp'), reverse=True,
        )

        if len(user_notifications) >= app.config.get(
                'NOTIFICATIONS_MAX_COUNT',
        ):
            user_notifications.pop()

    timestamp = int(dt.timestamp(dt.now().replace(microsecond=0)))
    new_notification = {
        'id': obj.user_id + str(timestamp),
        'timestamp': timestamp,
        'is_new': True,
        'user_id': obj.user_id,
        'key': obj.key,
        'target_id': obj.target_id,
        'data': obj.data,
    }

    user_notifications.append(new_notification)

    if user:
        logger.info('user was found, updating doc in db')
        db.users.update_one(
            {'_id': user.get('_id')},
            {'$set': {'notifications': user_notifications}},
        )
    else:
        logger.info('user was not found, creating new doc in db')
        email = obj.email
        if email is None:
            email = app.config.get('EMAIL')
        db.users.insert_one(
            {
                'user_id': obj.user_id,
                'notifications': user_notifications,
                'email': email,
            },
        )


def choose_key_action(key):
    match key:
        case KeyEnum.registration.value:
            return registration
        case KeyEnum.new_message.value:
            return new_message
        case KeyEnum.new_post.value:
            return new_post
        case KeyEnum.new_login.value:
            return new_login
        case _:
            raise InvalidAPIUsage('Invalid "key" value')


def get_user_notifications(user_id, skip=None, limit=None):
    user = db.users.find_one(
        {'user_id': user_id},
    )
    if user:
        notifications = user.get('notifications', [])
        notifications.sort(key=lambda x: x.get('timestamp'), reverse=True)
        if skip:
            skip = int(skip)
            if skip >= len(notifications):
                notifications = []
            else:
                notifications = notifications[skip:]
        if limit:
            limit = int(limit)
            if limit <= len(notifications) and limit != 0:
                notifications = notifications[:limit]
        new_count = 0
        for notif in notifications:
            if notif.get('is_new') is True:
                new_count += 1
        meta_data = {
            'elements': len(notifications),
            'new': new_count,
        }
        logger.info('OK. returning notification and metadata')
        return True, notifications, meta_data
    logger.error('no user found')
    return False, None, None


def send_email(message: str, email: str):
    msg = Message(
        message,
        recipients=[email],
        sender=(
            app.config.get('SMTP_NAME', 'AcePlace'),
            app.config.get('MAIL_DEFAULT_SENDER'),
        ),
    )
    try:
        mail.send(msg)
    except Exception as e:
        raise MailingError(e.args)
