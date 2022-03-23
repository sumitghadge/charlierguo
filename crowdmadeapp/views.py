from django.views.generic.edit import FormView
from crowdmadeapp.forms import CreateProductForm

# Create your views here.
class ProductCreateView(FormView):
    form_class = CreateProductForm
    template_name = "crowdmadeapp/product_form.html"
    success_url = "/products/create/"
