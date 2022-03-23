from django.db import models

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"

    title = models.CharField(max_length=1024)
    description = models.TextField()
    status = models.CharField(max_length=1024, choices=Status.choices)
    price = models.FloatField()
    vendor = models.CharField(max_length=1024)

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
    address = models.ForeignKey(Address, related_name="orders", on_delete=models.CASCADE)

    subtotal = models.FloatField()
    taxes = models.FloatField()
    shipping = models.FloatField()
    total = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    shipped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
    

class Item(models.Model):
    order = models.ForeignKey(Order, related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.FloatField()