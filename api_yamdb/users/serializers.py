from rest_framework import serializers
from .models import User
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        # print(value.lower())
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'User cannot have username \'me\'.')
        pattern = re.compile(r'^[\w.@+-]+\Z') # r'^[\w.@+-]+\Z'
        if not pattern.match(value):
            raise serializers.ValidationError(
                'Username. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
        return value


class UserMeSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False, max_length=254)
    
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'User cannot have username \'me\'.')
        pattern = re.compile(r'^[\w.@+-]+\Z') # r'^[\w.@+-]+\Z'
        if not pattern.match(value):
            raise serializers.ValidationError(
                'Username. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
        return value
    def validate(self, data):
        if self.initial_data.get('role'):
            raise serializers.ValidationError(
                'Users \'me\' patch change role not allowed.')
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)

