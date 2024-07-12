from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'fav_discounts', 'mobile_phone']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

class MobilePhoneChangeSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(required=True, max_length=11)

    def validate_mobile_phone(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("Mobile phone number must be 11 digits.")
        return value

class UsernameChangeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=60)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'mobile_phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_phone=validated_data['mobile_phone'],
        )
        return user
