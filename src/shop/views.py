from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView

from shop.forms import ProductForm
from shop.models import Image, Product


class HomePageView(TemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = Product.objects.all()
        context['images'] = Image.objects.all().distinct('product')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/products/add.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
