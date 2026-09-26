from rest_framework import serializers
from .models import Product, PriceRecord, CollectionLog


class PriceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRecord
        fields = ["id", "price", "availability", "collected_at"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "url", "store", "target_price", "is_active", "created_at"]