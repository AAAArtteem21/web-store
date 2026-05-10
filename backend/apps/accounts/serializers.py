from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True,validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email','password','password_confirm',
                  'first_name','last_name','phone')
        extra_kwargs = {
            'first_name':{'required':False},
            'last_name':{'required':False},
            'phone':{'required':False},
        }
        
    def validate(self,attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password':'Password fields didn`t match.'}
            )
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password_confirm')
        user=User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # ← было email, стало username
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Неверный логин или пароль')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Введите username и пароль')
    
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    

    class Meta:
        model = User
        fields = (
            'id','username','email','first_name','last_name'
            ,'full_name','phone','created_at'        )
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required = True,
        validators =[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is correct')
        return value
    
    def validate(self,attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new password': 'Password fields didn`t match'
            })
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

