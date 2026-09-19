

# Register your models here.
from django.contrib import admin
from .models import Product, PriceRecord, CollectionLog

admin.site.register(Product)
admin.site.register(PriceRecord)
admin.site.register(CollectionLog)
