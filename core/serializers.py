from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    # make sure to extend BaseUserCreateSerializer.Meta too
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name' ]


class UserSerializer(BaseUserSerializer):
    # make sure to extend BaseUserSerializer.Meta too
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username','email', 'first_name', 'last_name' ]
