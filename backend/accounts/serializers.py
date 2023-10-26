from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email= validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name', ""),
            last_name = validated_data.get('last_name', "")
        )
        return user
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only':True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.CharField(read_only = True)
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        email = attrs.get('email',None)
        password = attrs.get('password', None)

        if email is None:
            raise serializers.ValidationError('email required')
        if password is None:
            raise serializers.ValidationError('password is required')
        user = authenticate(username = email, password = password)

        if user is None:
            raise ValueError('Invalid email or password')
        
        return {
            'email' : user.email,
            'id' : user.id
        }