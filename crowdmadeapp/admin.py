from django.contrib import admin
from django.db.models import Sum

from crowdmadeapp.models import Product, Address, Order, Item, Collection

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "total", "get_quantity"]

    search_fields = ["name", "email", "address__street1"]

    list_filter = [
        "address__country_name",
    ]

    @admin.display(ordering="item__quantity")
    def get_quantity(self, obj):
        quantity = obj.items.all().aggregate(Sum("quantity"))
        return quantity["quantity__sum"]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ("address",)
        return self.readonly_fields


class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "get_title", "get_price"]

    @admin.display(ordering="products__title", description="Product Title")
    def get_title(self, obj):
        data = [a.title for a in obj.products.all()]
        return data

    @admin.display(ordering="products__price", description="Price")
    def get_price(self, obj):
        price = obj.products.all().aggregate(Sum("price"))["price__sum"]
        return price


admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
admin.site.register(Collection, CollectionAdmin)
