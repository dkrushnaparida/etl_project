from django.db import models

# Model to store uploaded region files
class SalesUpload(models.Model):
    region_a_file = models.FileField(upload_to='uploads/')
    region_b_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload on {self.uploaded_at}"


class SalesData(models.Model):
    OrderId = models.CharField(max_length=50, unique=True)
    OrderItemId = models.CharField(max_length=50)
    QuantityOrdered = models.IntegerField()
    ItemPrice = models.FloatField()
    PromotionDiscount = models.FloatField()
    total_sales = models.FloatField()
    net_sale = models.FloatField()
    region = models.CharField(max_length=1)

    def __str__(self):
        return f"Order {self.OrderId} - Region {self.region}"
