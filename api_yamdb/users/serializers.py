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
    
    # def validate_email(self, value):
    #     if self.instance:
    #         if value != self.instance.email:
    #             raise serializers.ValidationError({'email':'Wrong email.'})
    #     else:
    #         if self.Meta.model.objects.filter(email=value).exists():
    #             raise serializers.ValidationError(
    #                 'User with that email exists already.')
    #     return value
    def validate(self, data):
        if not self.instance:
            if self.Meta.model.objects.filter(username=data.get('username', None)).exists():
                self.instance = self.Meta.model.objects.filter(username=data.get('username', None))
                self.is_valid()
        return data
            


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False, max_length=254)

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserAuthSignUpSerializer(UserMeSerializer):
    
    class Meta(UserMeSerializer.Meta):
        fields = ('username', 'email')


class SignUpSerializer(UserSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)
    corresponding_object: object
    is_exist_checked = False
    has_object = False
    
    def check_object(self, username=None, email=None):
        if self.is_exist_checked:
            return self.has_object
        username = self.initial_data.get('username')
        if username and self.Meta.model.objects.filter(username=username).exists():
            # self.corresponding_object = self.Meta.model.objects.get(username=username)
            # self.instance = self.corresponding_object
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
                        'User with that eamil exists already.')
        return value


        # if self.instance:
        #     if value != self.instance.email:
        #         raise serializers.ValidationError({'email':'Wrong email1.'})
        # else:
        #     if self.check_object():
        #         if self.corresponding_object.email != value:
        #             raise serializers.ValidationError(
        #                 'Wrong email2.')
        #     else:
        #         if self.Meta.model.objects.filter(email=self.initial_data.get('email')).exists():
        #             raise serializers.ValidationError(
        #                 'User with that eamil exists already.')
        # return value
    
    class Meta(UserSerializer.Meta):
        fields = ('username', 'email')
   