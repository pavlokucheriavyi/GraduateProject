from django.shortcuts import render
from .models import Products
from django.views.generic import ListView, DetailView
from .forms import SearchForm


def home(request):
    start = 'Hello Kolischa'

    return render(request, 'shop/home.html')


class ProductsView(ListView):
    model = Products
    template_name = 'shop/shop.html'
    context_object_name = 'products_list'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        form = SearchForm(self.request.POST or None)
        ctx = super(ProductsView, self).get_context_data(**kwargs)

        ctx['form'] = form
        return ctx

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        if form.is_valid() and form.cleaned_data.get('search') != '':
            search_word = form.cleaned_data.get('search').capitalize()
            tags = Products.objects.filter(title__contains=search_word)
            print(search_word)
            return render(request, self.template_name, {'products_list': tags, 'form': form})

        stuff = request.POST.get('category')
        # list with final product objects
        tags = Products.objects.filter(category__category=stuff)

        return render(request, self.template_name, {'products_list': tags, 'form': form})


class ProductDetailView(DetailView):
    model = Products
    template_name = 'shop/product_detail.html'
    context_object_name = 'item'