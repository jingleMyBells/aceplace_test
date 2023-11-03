import logging

from flask import jsonify, request

from .exceptions import InvalidAPIUsage, MailingError
from .service import (
    change_user_notif_status,
    get_user_notifications,
    Notification,
)
from .validation import (
    validate_create_body,
    validate_list_params,
    validate_read_params,
)
from . import app


logger = logging.getLogger(__name__)


@app.route('/create', methods=['POST'])
def create_notification():
    body_obj = request.get_json()
    if validate_create_body(body_obj) is False:
        return {
            'success': 'false',
            'errors': ['invalid input data']
        }, 400
    if request.args.get('email'):
        body_obj['email'] = request.args.get('email')
    notification = Notification(body_obj)
    notification.perform_selected_action_with_data()
    return {'success': 'true'}, 200


@app.route('/list', methods=['GET'])
def list_notifications():
    logger.critical('lol')
    params = request.args
    if validate_list_params(params) is False:
        return {
            'success': False,
            'errors': ['invalid input data']
        }, 400

    status, notifications, meta_data = get_user_notifications(
        params.get('user_id'),
        params.get('skip'),
        params.get('limit'),
    )

    if status:
        return {
            'success': 'true',
            'data': {
                'elements': meta_data.get('elements'),
                'new': meta_data.get('new'),
                'request': {
                    'user_id': params.get('user_id'),
                    'skip': params.get('skip', 0),
                    'limit': params.get('limit', 0),
                },
                'list': notifications,
            }
        }, 200
    else:
        return {'success': False}, 404


@app.route('/read', methods=['POST'])
def read_notification():
    params = request.args
    if validate_read_params(params) is False:
        return {
            'success': 'false',
            'errors': ['invalid input data']
        }, 400
    result = change_user_notif_status(
        params.get('user_id'),
        params.get('notification_id'),
    )
    if result:
        return {'success': 'true'}, 200
    return {'success': 'false'}, 404


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage_handler(error):
    logger.error(error.to_dict)
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(MailingError)
def mailing_error_handler(error):
    logger.error(f'mailing error: {error.to_dict}')
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(500)
def page_not_found(error):
    logger.error(f'internal error: {error}')
    return {'Internal server error'}, 500
