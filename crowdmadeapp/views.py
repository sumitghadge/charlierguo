from crowdmadeapp.forms import CreateProductForm
from django.views.generic.edit import FormView

# Create your views here.
class ProductCreateView(FormView):
    form_class = CreateProductForm
    template_name = "crowdmadeapp/product_form.html"
    success_url ="/products/create/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
