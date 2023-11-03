import logging

from .constants import KeyEnum


logger = logging.getLogger(__name__)


def validate_create_body(obj: dict):
    is_user_id_valid = entity_id_validation(obj.get('user_id'))
    is_target_id_valid = True
    if obj.get('target_id'):
        is_target_id_valid = entity_id_validation(obj.get('target_id'))
    is_key_valid = key_validation(obj.get('key'))

    return is_user_id_valid and is_target_id_valid and is_key_valid


def validate_list_params(params: dict):
    is_user_id_valid = entity_id_validation(params.get('user_id'))
    is_skip_and_limit_valid = True
    try:
        int(params.get('skip', '0'))
        int(params.get('limit', '0'))
    except (ValueError, TypeError) as e:
        logger.error(f'Query params validation error: {e}')
        is_skip_and_limit_valid = False
    return is_user_id_valid and is_skip_and_limit_valid


def validate_read_params(params: dict):
    is_user_id_valid = entity_id_validation(params.get('user_id'))
    is_notif_id_valid = notification_id_validation(params.get(
        'notification_id'),
    )
    return is_user_id_valid and is_notif_id_valid


def entity_id_validation(entity_id):
    if entity_id is None:
        logger.error('entity_id was not provided')
        return False
    if not isinstance(entity_id, str):
        logger.error('entity id is not a string')
        return False
    if len(entity_id) != 24:
        logger.error('entity id was not provided')
        return False
    return True


def key_validation(key):
    is_key_valid = key in [e.value for e in KeyEnum]
    if is_key_valid is False:
        logger.error('key provided is not correct')
    return is_key_valid


def notification_id_validation(notif_id):
    if notif_id is None:
        logger.error('notification id was not provided')
    if isinstance(notif_id, str) is False:
        logger.error('notification id is not correct')
    return notif_id is not None and isinstance(notif_id, str)
