from django.contrib import admin
from crowdmadeapp.models import Product,Address,Order,Item

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display=['name','email','total']

    search_fields=['name','email','address__street1']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('address',)
        return self.readonly_fields

    
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order,OrderAdmin)
admin.site.register(Item)

