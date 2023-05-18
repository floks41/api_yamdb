from rest_framework import serializers
from users.models import User
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'User cannot have username \'me\'.')
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if not pattern.match(value):
            raise serializers.ValidationError(
                'Username. 150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only.')
        return value


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False, max_length=254)

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserAuthSignUpSerializer(UserMeSerializer):
    class Meta(UserMeSerializer.Meta):
        fields = ('username', 'email')
