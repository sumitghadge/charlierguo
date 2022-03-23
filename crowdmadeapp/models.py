from datetime import date, timedelta
from django.db import models
from django.db.models import Sum, Count, Avg, F


class Product(models.Model):
    """Product is model which represents product
    Attributes:
        title: Title of the product
        description : Description of the product
        status : Status of product DRAFT/ACTIVE
        price : Price of the product
        vendor : Vendor of the product
        image : Image of the product
    """

    class Status(models.TextChoices):
        """Choices of status"""

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
    """Address is model which represents address
    Attributes:
        street1: street1 for the order
        street2 : street2 for the order
        city : city for the order
        state : State for the order
        zipcode : Zipcode for the order
        country_name : Country_name for the order
        country_code : country_code for the order
    """

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
    """Order is model which represents order and have a reference of Address
    Attributes:
        name: Name for the order
        email : Email for the order
        address : Address for order DRAFT/ACTIVE
        subtotal : Subtotal for the order
        taxes : Taxes for the order
        shipping : shipping charges for the order
        total : total charges for the order
        created_at : Order created date
        shipped_at : Order shipping date
    """

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

    @classmethod
    def order_count(cls):
        last_30_days = date.today() - timedelta(days=30)
        order_count = cls.objects.filter(shipped_at__gt=last_30_days).aggregate(
            Count("id")
        )
        return order_count

    @classmethod
    def order_total(cls):
        last_30_days = date.today() - timedelta(days=30)
        order_total = cls.objects.filter(shipped_at__gt=last_30_days).aggregate(
            Sum("total")
        )
        return order_total

    @classmethod
    def average_shipping_time(cls):
        average_shipping_time = cls.objects.filter(shipped_at__isnull=False).aggregate(
            avg_score=Avg(F("shipped_at") - F("created_at"))
        )
        return average_shipping_time


class Item(models.Model):
    """Item is model which has a reference of oder and product
    Attributes:
        quantity : Quantity of an item
        total : Total cost of an item
    """

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.FloatField()

    @classmethod
    def product_quantities(cls):
        last_30_days = date.today() - timedelta(days=30)
        product_quantities = (
            cls.objects.filter(order__shipped_at__gt=last_30_days)
            .values("product__title")
            .annotate(sum_q=Sum("quantity"))
        )
        return list(product_quantities)


class Collection(models.Model):
    """Collection is model which has a reference to product
    Attributes:
        title : Title is choice field of New/On_Sale/Fall_Collection
        description : Description cost of collection
    """

    class Status(models.TextChoices):
        NEW = "new", "New"
        ON_SALE = "on sale", "On sale"
        FALL_COLLECTION = "fall collection", "Fall Collection"

    title = models.CharField(max_length=1024, choices=Status.choices)
    description = models.TextField()
    products = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
