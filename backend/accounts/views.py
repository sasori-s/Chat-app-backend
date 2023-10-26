from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.tokenauthentication import JwtAuthentication
from .serializers import UserSerializer, LoginSerializer

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        token = JwtAuthentication.generateToken(payload=serializer.data)
        return Response({
            "message": "Login Successful",
            'token': token,
            'user': serializer.data
        }, status=201)
    return Response(serializer.errors, status=400)