from rest_framework import serializers


class DirectionSerializer(serializers.Serializer):
    direction = serializers.CharField()
    available_prices = serializers.JSONField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

