# �������� �������.

�������� ����������� ����������� �������������. 

����������� ������ ������������ �� ���� RestAPI ������, ������� ��������� ��������� ������ ����������� � ��������� ������������ � MongoDB, ���������� email, � ��� �� ������������� ������� ����������� �� ��������� ������������.

����������� ������������� ������ ��������� � ���� � ��������� ������������ � �� ������������ ���-�� ������ ���� ���������� (����� ����� ���������� ������������)

��� ������������ �������� Email ���������� key �� ������������ �����������.

#### ������ ����������� � ��������� ������������

```json
{
    "id": "some_notification_id",
    "timestamp": 1698138241,
    "is_new": false,
    "user_id": "638f394d4b7243fc0399ea67",
    "key": "new_message",
    "target_id": "0399ea67638f394d4b7243fc",
    "data": {
        "some_field": "some_value"
    }
}
```

��� ����� � ������ ���������� ������������ ������� ������� ����� ������� � email, ������� ����� ����� ���������.

## ���������� ���������, ����� ������� ��������������� ������

- PORT - ���� �� ������� ����� �������� ����������
- EMAIL - �������� email
- DB_URI - ������ ��� ����������� � mongoDB
- SMTP_HOST - ���� smtp �������
- SMTP_PORT - ���� smtp �������
- SMTP_LOGIN - ����� ������������
- SMTP_PASSWORD - ������ ������������
- SMTP_EMAIL - email � �������� ����� ���������� ���������
- SMTP_NAME - ��� ������������ � ���������� ������

## API Handlers: 

### [POST] /create ������� ����� �����������.

#### ���� �������:

- user_id - ������ �� 24 ������� (�������� ObjectID ��������� ������������ �������� ������������ �����������)
- target_id - ������ �� 24 ������� (�������� ObjectID ��������� ��������, � ������� ��������� �����������) (����� �������������)
- key - ���� ����������� enum
    - registration (������ �������� ������������ Email)
    - new_message (������ ������� ������ � ��������� ������������)
    - new_post (������ ������� ������ � ��������� ������������)
    - new_login (������� ������ � ��������� ������������ � �������� email)
- data - ������������ ������ �� ��� ����/�������� (����� �������������)

#### ������ ���� �������:

```json
{
    "user_id": "638f394d4b7243fc0399ea67",
    "key": "registration"
}
```

#### ������ ������

HTTP 201 Created

```json
{
    "success": true
}
```

### [GET] /list ���������� ������� ����������� ������������.

#### query params
- user_id [string] - ������������� ������������
- skip [int] - ���-�� �����������, ������� ������� ����������
- limit [int] - ���-�� ����������� ������� ������� �������

#### ������ ������

HTTP 200 Ok

```json
{
    "success": true,
    "data": {
        "elements": 23, // ����� �����������
        "new": 12, // ���-�� ������������� �����������
        "request": {
            "user_id": "638f394d4b7243fc0399ea67",
            "skip": 0,
            "limit": 10,
        }
        "list": [
            {
                "id": "some_notification_id",
                "timestamp": 1698138241,
                "is_new": false,
                "user_id": "638f394d4b7243fc0399ea67",
                "key": "new_message",
                "target_id": "0399ea67638f394d4b7243fc",
                "data": {
                    "some_field": "some_value"
                },
            },
            ...
        ]
    }
}
```

#### [POST] /read ������� ������� � ��������� �����������.

#### query params
- user_id [string] - ������������� ������������
- notification_id [string] - ������������� �����������

#### ������ ������

HTTP 200 Ok

```json
{
    "success": true
}
```

## �� ���� ����������

��� ��������� ������ ��������� ���� ������ ��� ��������, ������� �� ������� �������� ����������. ������ ������� ���� ������ � ������� ����� � Readme ����� � �����������.

## ��������� ���������� �������

������ ������� ����� ��������� ����������� ��� ������� ���������� ���� � Dockerfile'a � ����������� �� github.com.
