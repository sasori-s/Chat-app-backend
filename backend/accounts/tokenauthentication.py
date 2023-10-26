import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = self.extract_token(request=request)
        if token is None:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            self.verify_token(payload=payload)
            user_id = payload['id']
            userID = User.objects.get(id= user_id)
            return userID
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token ')
        

    def verify_token(self, payload):
        if "exp" not in payload:
            raise InvalidTokenError("Token has no expiration")
        
        exp_timestamp = payload['exp']
        current_timestamp = datetime.utcnow().timestamp()

        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has Expired")
    
    def extract_token(self, request):
        header = request.headers.get('Authorization')
        if header and header.startswith('Bearer '):
            return header.split(' ')[1]
        return None
    
    @staticmethod
    def generateToken(payload):
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload['exp'] = expiration
        token = jwt.encode(payload=payload, key= settings.SECRET_KEY, algorithm= 'HS256')
        return token