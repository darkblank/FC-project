from rest_framework import serializers

from accounts.models import User, Profile
from accounts.validators import phone_number


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
        )


class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[phone_number],
    )
    profile_image = serializers.ImageField(allow_empty_file=True)

    class Meta:
        model = Profile
        fields = (
            'name',
            'nickname',
            'phone_number',
            'profile_image',
            'preferences',
        )


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'password1',
            'password2',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password does not match')
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password1'],
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'user': ret,
            'token': instance.token,
        }
        return data
