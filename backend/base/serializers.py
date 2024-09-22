from rest_framework import serializers
from base.models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'brand',
                  'category', 'description', 'price', 'stocks', 'rating']

    def get_rating(self, obj):
        return {
            'rate': obj.rate,
            'count': obj.count
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fileds = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fileds = "__all__"
