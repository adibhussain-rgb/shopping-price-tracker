from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, PriceRecord
from .serializers import ProductSerializer, PriceRecordSerializer
from .services import get_current_price, get_lowest_price, get_highest_price, get_price_change, get_best_price_comparison


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
def product_history(request, pk):
    product = Product.objects.get(pk=pk)
    records = PriceRecord.objects.filter(product=product).order_by("collected_at")
    serializer = PriceRecordSerializer(records, many=True)

    return Response({
        "current_price": get_current_price(product),
        "lowest_price": get_lowest_price(product),
        "highest_price": get_highest_price(product),
        "price_change": get_price_change(product),
        "history": serializer.data,
    })


@api_view(["GET"])
def product_comparison(request, pk):
    product = Product.objects.get(pk=pk)
    comparison = get_best_price_comparison(product.name)
    return Response({"comparison": comparison})
