from django.http import JsonResponse
from crowdmadeapp.forms import CreateProductForm
from crowdmadeapp.models import Order,Item
from datetime import date, timedelta
from django.db.models import Sum,Count
from django.views.generic.edit import FormView

# Create your views here.
class ProductCreateView(FormView):
    form_class = CreateProductForm
    template_name = "crowdmadeapp/product_form.html"
    success_url ="/add_product/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def order_count(request):
    last_30_days = date.today() - timedelta(days=30)
    order_count = Order.objects.filter(shipped_at__gt = last_30_days).aggregate(Count('id'))
    return JsonResponse({'data': order_count})

def order_total(request):
    last_30_days = date.today() - timedelta(days=30)
    order_total = Order.objects.filter(shipped_at__gt = last_30_days).aggregate(Sum('total'))
    return JsonResponse({'data': order_total})

def product_quantities(request):
    last_30_days = date.today() - timedelta(days=30)
    product_quantities = Item.objects.filter(order__shipped_at__gt = last_30_days).values('product__title').annotate(sum_q=Sum('quantity'))
    return JsonResponse({'data': list(product_quantities)})