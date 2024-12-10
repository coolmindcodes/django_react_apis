from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.now() + timedelta(minutes=60),
        "iat": datetime.now()
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256")

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')
        token_id = payload['user_id']
        user = get_user_model().objects.get(id=token_id)

        if user is None:
            raise  AuthenticationFailed('User not found')
        return user, None