from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Products
from django.core import serializers
from .cart import Cart
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # really_dict_request = dict()
    # for k, v in dict(request.POST).items():
    #     really_dict_request[k] = v[-1]
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    if cart.__len__() == 0:
        html = render_to_string('cart/ajax/cart_after_ajax.html')
        return JsonResponse({'data': html})
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart/detail.html', {'cart': cart})
