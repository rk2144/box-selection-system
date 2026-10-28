from rest_framework import serializers
from .models import Product, Box


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        for field in ["length", "width", "height", "weight"]:
            if data.get(field, getattr(self.instance, field, 0)) <= 0:
                raise serializers.ValidationError(
                    {field: "Value must be greater than zero."}
                )
        return data


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"

    def validate(self, data):
        fields = [
            "inner_length",
            "inner_width",
            "inner_height",
            "max_weight",
            "cost",
        ]

        for field in fields:
            value = data.get(field, getattr(self.instance, field, 0))
            if value <= 0:
                raise serializers.ValidationError(
                    {field: "Value must be greater than zero."}
                )

        return data