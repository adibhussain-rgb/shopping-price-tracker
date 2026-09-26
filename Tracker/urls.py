from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListCreateView.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/history/", views.product_history, name="product-history"),
    path("products/<int:pk>/comparison/", views.product_comparison, name="product-comparison"),
]