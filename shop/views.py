import json
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse
from .models import Products
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from cart.forms import CartAddProductForm
from .models import AvailableMarks
from .cars_dict import cars

from .forms import SearchForm, RepairForm


def home(request):
    start = 'Hello Kolischa'

    return render(request, 'shop/home.html')


class ProductsView(ListView):
    model = Products
    template_name = 'shop/shop.html'
    context_object_name = 'products_list'
    paginate_by = 8
    ordering = ['-date']

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
            html = render_to_string('shop/ajax/shop.html', {'data': tags})
            return JsonResponse({'data': html})

        # if 'click' in request.POST:
        # # list with final product objects
        #     stuff = request.POST.get('cat')
        #     tags = Products.objects.filter(category__category=stuff)
        #     html = render_to_string('shop/shop.html', {'product_list': tags})
        #     return HttpResponse(html)


def filter_data(request):
    stuff = request.POST.get('cat')
    tags = Products.objects.all().filter(category__category=stuff)
    # for k, v in cars['list'].items():
    #     b2 = AvailableMarks(name=f'{k}', is_available=True)
    #     b2.save()
    #     print('good')

    html = render_to_string('shop/ajax/shop.html', {'data': tags})
    return JsonResponse({'data': html})


class UpdateProductView(UserPassesTestMixin, UpdateView):
    model = Products
    template_name = 'shop/update_product.html'

    fields = ['title', 'price', 'description', 'count', 'category', 'image']

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        messages.error(self.request, 'Сторінка не знайдена')
        return redirect('home')


class DeleteProductView(UserPassesTestMixin, DeleteView, SuccessMessageMixin):
    model = Products
    success_url = '/shop'  # после удаления будет переходить на главную страницу
    template_name = 'shop/delete_product.html'
    success_message = 'All good'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteProductView, self).delete(request, *args, **kwargs)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect('home')


def product_detail(request, pk):
    all_objects_list = Products.objects.all()
    result_list = []

    for i in all_objects_list:
        if i.id == pk:
            result_list.append(i)

    cart_product_form = CartAddProductForm()

    data = {
        'result_list': result_list,
        'form': cart_product_form
    }

    return render(request, 'shop/product_detail.html', data)


# class ProductDetailView(DetailView):
#     model = Products
#     template_name = 'shop/product_detail.html'
#     context_object_name = 'item'
#
#     def post(self, request, pk):
#         print(pk)
#         return redirect('cart:cart_add', pk)
#
#     def get_context_data(self, **kwargs):
#         form = CartAddProductForm()
#         ctx = super(ProductDetailView, self).get_context_data(**kwargs)
#
#         ctx['form'] = form
#         return ctx


def repair(request, type_name):
    types_of_repair_list = ['Шиномонтаж', 'Кузовний ремонт', 'Ремонт ходової', 'Покраска', 'Ремонт тормозної системи',
                            'Диагностика та ТО']

    if request.method == 'POST':
        mark_var = request.POST
        print(mark_var)
        return redirect('home')

    else:
        is_available_list = AvailableMarks.objects.all()
        f = open('shop/is_available.json')
        data = json.load(f)
        empty_dict = dict()

        for i in is_available_list:
            empty_dict[i.name] = i.is_available

        if empty_dict != data:
            with open('shop/is_available.json', 'w', encoding='utf8') as json_file:
                json.dump(empty_dict, json_file, indent=4)

        json_dict = json.dumps(empty_dict)

        x = RepairForm()
        return render(request, 'shop/repair.html',
                      {'form': x, 'type_of_repair': type_name, 'types_of_repair_list': types_of_repair_list,
                       'My_json': json_dict})
