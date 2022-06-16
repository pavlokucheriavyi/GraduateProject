from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Products
from users.models import PartsOrder, UndefinedParts, Profile
from django.core import serializers
import json
from .test import get_vidd
from .cart import Cart
from .test import export_json
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import CartAddProductForm
from .forms import CaptchaTestForm
from django.core.mail import send_mail, BadHeaderError


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    print(request.POST)
    # really_dict_request = dict()
    # for k, v in dict(request.POST).items():
    #     really_dict_request[k] = v[-1]
    product = get_object_or_404(Products, id=product_id)
    req_dict = dict(request.POST)
    if product.count == 0 and 'update' not in req_dict:
        error = f'Наразі нажаль товару "{product.title}" немає в наявності$Нема товару'

        return HttpResponse(error)
    elif product.count < int(req_dict['quantity'][0]) and product.count != 0 and 'update' not in req_dict:
        error = f'Такої кількості товару "{product.title}" немає в наявності, ' \
                f'ви можете придбати максимум {product.count} штук$Нема товару'
        return HttpResponse(error)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']

        )

    y = dict(request.POST)
    try:
        send_mail('Message from Victor', 'Its last message for sendgrid', 'kobra1903@ukr.net', ['kuchriavy10@gmail.com'], fail_silently=True)
        print('All good with message')
    except BadHeaderError:
        print('Invalid message ')
    count = y['quantity'][0]
    x = Products.objects.get(id=product_id)
    product_sum = "%.2f" % float(float(x.price) * int(count))
    cart_sum = cart.get_total_price()
    if request.user.is_authenticated:
        id_of_current_user = request.user.id
        get_object_user = Profile.objects.get(user_id=id_of_current_user)

        new_or_not = get_object_user.is_new_user
        if new_or_not:
            cart_sum = "%.2f" % (float(cart_sum) * 0.8)
    export_string = count + '-' + str(product_sum) + '-' + str(cart_sum)
    html = render_to_string('cart/ajax/cart_after_update_product.html', {'data': export_string})
    return JsonResponse({'data': html})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    if cart.__len__() == 0:
        html = render_to_string('cart/ajax/cart_after_ajax.html')
        return JsonResponse({'data': html})

    cart_sum = cart.get_total_price()
    if request.user.is_authenticated:
        id_of_current_user = request.user.id
        get_object_user = Profile.objects.get(user_id=id_of_current_user)

        new_or_not = get_object_user.is_new_user
        if new_or_not:
            cart_sum = "%.2f" % (float(cart_sum) * 0.8)
    html = render_to_string('cart/ajax/sum_after_remove.html', {'data': cart_sum})

    return JsonResponse({'data': html})


def take_order(request):
    if request.POST:
        print(request.POST)
        form = CaptchaTestForm(request.POST)
        req_dict = dict(request.POST)
        if 'MyValue' in req_dict:
            city = req_dict['MyValue'][0]
            final_city = city.split(' ')
            export_list = get_vidd(final_city[1])
            # all_address_json = json.dumps(export_list, ensure_ascii=False)
            return HttpResponse(export_list)
        else:
            if form.is_valid() and int(req_dict['delivery_method_id'][0]) == 1:
                html = "HUMAN-"
                order_str = ''
                cart = Cart(request)
                total_sum = "%.2f" % (float(cart.get_total_price()) * 0.8 if req_dict['is_authenticated'][
                                                                                 0] != 'None' else cart.get_total_price())
                num = 0
                for i in cart:
                    num += 1
                    # get object from Products model and edit count field
                    get_object = Products.objects.get(id=i['product'].id)
                    if get_object.count < i['quantity'] and get_object.count != 0:
                        error = f'Такої кількості товару "{get_object.title}" немає в наявності, ' \
                                f'ви можете придбати максимум {get_object.count} штук$Нема товару'
                        return HttpResponse(error)
                    elif get_object.count == 0:
                        error = f'Наразі товару "{get_object.title}" немає в наявності, видаліть будь-ласка "{get_object.title}"' \
                                f'  з корзини$Нема товару'
                        return HttpResponse(error)
                    get_object.count = get_object.count - i['quantity']
                    get_object.save()
                    order_str = order_str + f'{num}) ' + 'Продукт: ' + i[
                        'product'].title + ';\n     ' + 'Кількість: ' + str(
                        i['quantity']) + ';\n     ' + 'Ціна за 1 штуку: ' + str(
                        i['price']) + ' грн;\n     ' + 'Загальна ціна: ' + i[
                                    'total_price'] + ' грн;\n     ' + '-----------------------------------------------------------' + '\n'

                # check is user authenticated
                get_user_id = req_dict['is_authenticated'][0]
                if get_user_id == 'None':
                    export_info_about_id = '0'
                else:
                    export_info_about_id = get_user_id

                export_comment = req_dict['comment_to_order'][0]
                # edit comment if comment == empty string
                if req_dict['comment_to_order'][0] == '':
                    export_comment = '---------------------------'

                b = PartsOrder(name=req_dict['full_name'][0], email=req_dict['email'][0],
                               phone_number=req_dict['phone_number'][0],
                               comment=export_comment,
                               is_authenticated_user=export_info_about_id,
                               composition_order=order_str, summa=total_sum)
                b.save()
                # save data to UndefinedParts db
                for item in cart:
                    part_object = UndefinedParts(id_order=b.id, name=req_dict['full_name'][0],
                                                 product=item['product'].title,
                                                 id_of_product=item['product'].id,
                                                 count_product=item['quantity'])
                    part_object.save()

                html += str(b.id)
                return HttpResponse(html)
            elif form.is_valid() and int(req_dict['delivery_method_id'][0]) == 9:
                html = "HUMAN-"
                order_str = ''
                cart = Cart(request)
                total_sum = "%.2f" % (float(cart.get_total_price()) * 0.8 if req_dict['is_authenticated'][
                                                                                 0] != 'None' else cart.get_total_price())
                num = 0
                for i in cart:
                    # get object from Products model and edit count field
                    get_object = Products.objects.get(id=i['product'].id)
                    if get_object.count < i['quantity'] and get_object.count != 0:
                        error = f'Такої кількості товару "{get_object.title}" немає в наявності, ' \
                                f'ви можете придбати максимум {get_object.count} штук$Нема товару'
                        return HttpResponse(error)
                    elif get_object.count == 0:
                        error = f'Товару "{get_object.title}" немає в наявності$Нема товару'
                        return HttpResponse(error)
                    get_object.count = get_object.count - i['quantity']
                    get_object.save()
                    num += 1
                    order_str = order_str + f'{num}) ' + 'Продукт: ' + i[
                        'product'].title + ';\n     ' + 'Кількість: ' + str(
                        i['quantity']) + ';\n     ' + 'Ціна за 1 штуку: ' + str(
                        i['price']) + ' грн;\n     ' + 'Загальна ціна: ' + i[
                                    'total_price'] + ' грн;\n     ' + '-----------------------------------------------------------' + '\n'

                # check is user authenticated
                get_user_id = req_dict['is_authenticated'][0]
                if get_user_id == 'None':
                    export_info_about_id = '0'
                else:
                    export_info_about_id = get_user_id

                export_comment = req_dict['comment_to_order'][0]
                # edit comment if comment == empty string
                if req_dict['comment_to_order'][0] == '':
                    export_comment = '---------------------------'

                b = PartsOrder(name=req_dict['full_name'][0], email=req_dict['email'][0],
                               phone_number=req_dict['phone_number'][0],
                               address_city=req_dict['address_order_city'][0],
                               address_vidd=req_dict['address_order_vidd'][0],
                               comment=export_comment,
                               is_authenticated_user=export_info_about_id,
                               composition_order=order_str, summa=total_sum)
                b.save()

                # save data to UndefinedParts db
                for item in cart:
                    part_object = UndefinedParts(id_order=b.id, name=req_dict['full_name'][0],
                                                 product=item['product'].title,
                                                 id_of_product=item['product'].id,
                                                 count_product=item['quantity'])
                    part_object.save()

                html += str(b.id)
                return HttpResponse(html)
            else:
                html = "Введено не вірні літери, спробуйте ще раз"
                return HttpResponse(html)
    else:

        cart = Cart(request)
        empty_list = []
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
            empty_list.append(item)
            # print(item)

        # print(empty_list[0]['product'].title)

        return render(request, 'cart/take_order.html', {'cart': cart})


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        # product = Products.objects.get(id=item['product'].id)
        # item['price'] = float(product.price)
        # print(item)
    total_products_price = cart.get_total_price()
    # print(total_products_price)
    captcha_form = CaptchaTestForm()

    flag = None
    id_of_current_user = 'None'
    export_email = ''

    if request.user.is_authenticated:
        id_of_current_user = request.user.id
        get_object_user = Profile.objects.get(user_id=id_of_current_user)
        export_email = request.user.email

        new_or_not = get_object_user.is_new_user
        if new_or_not:
            total_products_price = "%.2f" % (float(total_products_price) * 0.8)
            flag = True

    return render(request, 'cart/detail.html', {'cart': cart, 'total_products_price': total_products_price,
                                                'captcha': captcha_form, 'export_json': export_json,
                                                'flag': flag, 'email': export_email, 'user_id': id_of_current_user})


def cart_delete_all(request):
    cart = Cart(request)
    cart.delete()

    return render(request, 'cart/detail.html')
