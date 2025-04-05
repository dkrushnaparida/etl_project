from django.contrib import admin
from .models import SalesData, SalesUpload

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('OrderId', 'region', 'QuantityOrdered', 'ItemPrice', 'total_sales', 'net_sale')

@admin.register(SalesUpload)
class SalesUploadAdmin(admin.ModelAdmin):
    list_display = ('region_a_file', 'region_b_file', 'uploaded_at')
