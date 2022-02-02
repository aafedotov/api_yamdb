from rest_framework import serializers
from users.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class GetTokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']


