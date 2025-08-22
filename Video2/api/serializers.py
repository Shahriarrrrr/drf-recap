from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "stock",
            "price",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Value must be greater than zero"
            )
        return value
