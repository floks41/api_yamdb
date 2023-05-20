import re

from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User


USERNAME_PATTERN = r'^[\w.@+-]+\Z'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserUsernameValidationSerializer(UserSerializer):
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'User cannot have username \'me\'.')

        if not re.compile(USERNAME_PATTERN).match(value):
            raise serializers.ValidationError(
                'Username. 150 characters or fewer. '
                'Letters, digits and @/./+/-/_ only.')

        return value


class UserMePatchSerializer(UserUsernameValidationSerializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False, max_length=254)

    class Meta(UserUsernameValidationSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(UserUsernameValidationSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)
    is_object_existance_checked = False
    is_object_exists = False

    def check_object(self):
        """Подбирает объект из модели, если такой есть.
        Сохраняет в self.instance. Запоминает факт проверки и результат
        в self.is_object_existance_checked и self.is_object_exists.
        При отсутвии объекта исключений не выдает.
        """
        if self.is_object_existance_checked:
            return self.is_object_exists

        username = self.initial_data.get('username')

        if (username and self.Meta.model.objects.filter(
                username=username).exists()):
            self.instance = self.Meta.model.objects.get(username=username)
            self.is_object_exists = True
            self.is_object_existance_checked = True

        return self.is_object_exists

    def validate_email(self, value):
        if self.check_object():
            if value != self.instance.email:
                raise serializers.ValidationError('Wrong email.')
        else:
            if self.Meta.model.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    'User with that email exists already.')
        return value

    class Meta(UserUsernameValidationSerializer.Meta):
        fields = ('username', 'email')


class AuthGetTokenSerializer(SignUpSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return str(AccessToken.for_user(obj).token)

    def validate_confirmation_code(self, value):
        if self.check_object() and value != self.instance.confirmation_code:
            raise serializers.ValidationError('Wrong confirmation code.')
        return value

    def validate_username(self, value):
        if not self.check_object():
            raise serializers.ValidationError('Wrong username.')
        return super().validate_username(value)

    class Meta(SignUpSerializer.Meta):
        write_only_fields = ('username', 'confirmation_code')
        fields = ('username', 'confirmation_code', 'token')
