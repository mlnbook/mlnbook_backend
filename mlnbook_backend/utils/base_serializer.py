from rest_framework import serializers


class AuthModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # Get the authenticated user from the request
        user = self.context['request'].user

        # Add the authenticated user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Get the authenticated user from the request
        user = self.context['request'].user

        # Add the authenticated user
        validated_data['user'] = user
        return super().update(instance, validated_data)
