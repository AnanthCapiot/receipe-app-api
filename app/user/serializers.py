from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    # -- use ugettext_lazy for i18N support
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate users"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = F'Unable to validate user (input user name is: {email})'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        # -- validate method MUST return attrs
        return attrs
