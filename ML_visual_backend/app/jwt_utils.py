import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY  # 获取 Django 的 SECRET_KEY

def create_access_token(identity):
    payload = {
        'identity': identity,
        'exp': datetime.utcnow() + timedelta(days=1)  # 设置过期时间为1天
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return access_token

def decode_access_token(access_token):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('identity')
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def validate_token(request):
    token = request.headers.get('Authorization')
    if not token:
        return None

    try:
        token_type, access_token = token.split()
        if token_type.lower() != 'bearer':
            return None

        username = decode_access_token(access_token)
        return username
    except Exception as e:
        return None