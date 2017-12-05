from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    # nickname = serializers.CharField(max_length=10)
    # phone_number = serializers.CharField(
    #     validators=[phone_number],
    # )
    # profile_image = serializers.ImageField(allow_empty_file=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'name',
            'email',
            # 'nickname',
            # 'phone_number',
            # 'profile_image',
        )

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile', {})
    #     name = profile_data.get('name')
    #
    #     instance = super(UserSerializer, self).update(instance, validated_data)
    #
    #     # get and update user profile
    #     profile = instance.profile
    #     if profile_data and name:
    #         profile.name = name
    #         profile.save()
    #     return instance


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'name',
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
            name=validated_data['name'],
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
