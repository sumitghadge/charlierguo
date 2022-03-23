from datetime import date, timedelta
from django.db import models
from django.db.models import Sum, Count, Avg, F


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"

    title = models.CharField(max_length=1024)
    description = models.TextField()
    status = models.CharField(max_length=1024, choices=Status.choices)
    price = models.FloatField()
    vendor = models.CharField(max_length=1024)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.title)


class Address(models.Model):
    street1 = models.CharField(max_length=1024)
    street2 = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=1024)
    zipcode = models.CharField(max_length=1024)
    country_name = models.CharField(max_length=1024)
    country_code = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.street1)


class Order(models.Model):
    name = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    address = models.ForeignKey(
        Address, related_name="orders", on_delete=models.CASCADE
    )
    subtotal = models.FloatField()
    taxes = models.FloatField()
    shipping = models.FloatField()
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    @property
    def order_count(self):
        last_30_days = date.today() - timedelta(days=30)
        order_count = Order.objects.filter(shipped_at__gt=last_30_days).aggregate(
            Count("id")
        )
        return order_count

    @property
    def order_total(self):
        last_30_days = date.today() - timedelta(days=30)
        order_total = Order.objects.filter(shipped_at__gt=last_30_days).aggregate(
            Sum("total")
        )
        return order_total

    @property
    def average_shipping_time(self):
        average_shipping_time = Order.objects.filter(
            shipped_at__isnull=False
        ).aggregate(avg_score=Avg(F("shipped_at") - F("created_at")))
        return average_shipping_time


class Item(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.FloatField()

    @property
    def product_quantities(self):
        last_30_days = date.today() - timedelta(days=30)
        product_quantities = (
            Item.objects.filter(order__shipped_at__gt=last_30_days)
            .values("product__title")
            .annotate(sum_q=Sum("quantity"))
        )
        return list(product_quantities)


class Collections(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        ON_SALE = "on sale", "On sale"
        Fall_Collection = "fall collection", "Fall Collection"

    title = models.CharField(max_length=1024, choices=Status.choices)
    description = models.TextField()
    products = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
