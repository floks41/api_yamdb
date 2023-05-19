from rest_framework import serializers, status
from users.models import User
import re
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    # def validate_username(self, value):
    #     if value.lower() == 'me':
    #         raise serializers.ValidationError(
    #             'User cannot have username \'me\'.')
    #     pattern = re.compile(r'^[\w.@+-]+\Z')
    #     if not pattern.match(value):
    #         raise serializers.ValidationError(
    #             'Username. 150 characters or fewer. '
    #             'Letters, digits and @/./+/-/_ only.')
    #     return value
    
    # def validate_email(self, value):
    #     if self.instance:
    #         if value != self.instance.email:
    #             raise serializers.ValidationError({'email':'Wrong email.'})
    #     else:
    #         if self.Meta.model.objects.filter(email=value).exists():
    #             raise serializers.ValidationError(
    #                 'User with that email exists already.')
    #     return value
    # def validate(self, data):
    #     if not self.instance:
    #         if self.Meta.model.objects.filter(username=data.get('username', None)).exists():
    #             self.instance = self.Meta.model.objects.filter(username=data.get('username', None))
    #             self.is_valid()
    #     return data
            


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False, max_length=254)

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

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(UserSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)
    is_exist_checked = False
    has_object = False
    
    def check_object(self, username=None, email=None):
        if self.is_exist_checked:
            return self.has_object
        username = self.initial_data.get('username')
        if username and self.Meta.model.objects.filter(username=username).exists():
            self.instance = self.Meta.model.objects.get(username=username)
            self.has_object = True
            self.is_exist_checked = True
        return self.has_object

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
    
    def validate_email(self, value):
        if self.check_object() or self.instance:
            if value != self.instance.email:
                raise serializers.ValidationError({'email':'Wrong email1.'})
        else:
            if self.Meta.model.objects.filter(email=self.initial_data.get('email')).exists():
                    raise serializers.ValidationError(
                        'User with that email exists already.')
        return value

    class Meta(UserSerializer.Meta):
        fields = ('username', 'email')

class AuthGetTokenSerializer(SignUpSerializer):
    token = serializers.SerializerMethodField()
    def get_token(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def validate_confirmation_code(self, value):
        if self.check_object(): # or self.instance
            if hasattr(self.instance, 'confirmation_code') and value != self.instance.confirmation_code:
                raise serializers.ValidationError('Wrong confirmation code.')
        return value
    def validate_username(self, value):
        if not self.check_object():
            raise serializers.ValidationError('Wrong username.')
        return super().validate_username(value)
    
    class Meta(SignUpSerializer.Meta):
        write_only_fields = ('username', 'confirmation_code')
        fields = ('username', 'confirmation_code', 'token')