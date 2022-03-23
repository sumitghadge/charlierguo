from django.contrib import admin
from crowdmadeapp.models import Product,Address,Order,Item,Collections
from django.db.models import Sum

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display=['name','email','total','get_quantity']

    @admin.display(ordering='item__quantity')
    def get_quantity(self,obj):
        quantity = obj.items.all().aggregate(Sum('quantity'))
        return quantity['quantity__sum']

    search_fields=['name','email','address__street1']

    list_filter =['address__country_name',]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('address',)
        return self.readonly_fields

class CollectionsAdmin(admin.ModelAdmin):
    list_display=['title','created_at','products','get_price']

    @admin.display(ordering='products__price',description='Price')
    def get_price(self,obj):
        return obj.products.price
  
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order,OrderAdmin)
admin.site.register(Item)
admin.site.register(Collections,CollectionsAdmin)

