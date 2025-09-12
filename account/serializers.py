from rest_framework import serializers
from .models import User

class UserSerialization(serializers.ModelSerializer):
    confirmpassword = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password', 'confirmpassword']

    def validate(self, attrs):
        password = attrs.get('password')
        confirmpassword = attrs.get('confirmpassword')
        if password:
            if not confirmpassword:
                raise serializers.ValidationError({'confirmpassword': ['This field is required when setting a new password.']})
            if password != confirmpassword:
                    raise serializers.ValidationError("Passwords do not match!")
        return attrs

    def create(self, validated_data):
        # exclude saving confirmpassword field in db
        validated_data.pop('confirmpassword')
        # Extract the password field from validated_data, if present
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('confirmpassword', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
