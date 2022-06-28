from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Products
from users.models import PartsOrder, UndefinedParts, Profile, Cars
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
    # try:
    #     send_mail('Last message', 'Its text of message', 'kobra1903@ukr.net', ['test-ykf0q4akt@srv1.mail-tester.com'], fail_silently=True)
    #     print('All good with message')
    # except BadHeaderError:
    #     print('Invalid message ')
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
                total_sum = float(cart.get_total_price()) * 0.8 if req_dict['is_authenticated'][
                                                                       0] != 'None' else cart.get_total_price()
                export_total_sum = "%.2f" % float(total_sum)

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

                # vars to send mail info
                test_view(request, kwargs=req_dict)
                b = PartsOrder(name=req_dict['full_name'][0], email=req_dict['email'][0],
                               phone_number=req_dict['phone_number'][0],
                               comment=export_comment,
                               is_authenticated_user=export_info_about_id,
                               composition_order=order_str, summa=export_total_sum)
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
                total_sum = float(cart.get_total_price()) * 0.8 if req_dict['is_authenticated'][
                                                                       0] != 'None' else cart.get_total_price()
                export_total_sum = "%.2f" % float(total_sum)

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

                # vars to send mail info
                test_view(request, kwargs=req_dict)
                b = PartsOrder(name=req_dict['full_name'][0], email=req_dict['email'][0],
                               phone_number=req_dict['phone_number'][0],
                               address_city=req_dict['address_order_city'][0],
                               address_vidd=req_dict['address_order_vidd'][0],
                               comment=export_comment,
                               is_authenticated_user=export_info_about_id,
                               composition_order=order_str, summa=export_total_sum)
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


def test_view(request, *args, **kwargs):
    cart = Cart(request)
    # send_cart_mail(request, req_dict)
    # final_list = []
    # for k, v in kwargs['kwargs'].items():
    #     final_list.append(v[0])
    x = kwargs['kwargs']
    total_products_price = cart.get_total_price()

    flag = None

    # export all data to html mail
    dict_user_info = is_user_buy_products(request, x['email'][0])
    users_cars = get_users_cars(request)
    orders_info = parse_dict(x)
    print(users_cars)
    # dict_user_info.update(users_cars)
    # dict_user_info.update(orders_info)

    if request.user.is_authenticated:
        id_of_current_user = request.user.id
        get_object_user = Profile.objects.get(user_id=id_of_current_user)

        new_or_not = get_object_user.is_new_user
        if new_or_not:
            total_products_price = "%.2f" % (float(total_products_price) * 0.8)
            flag = True
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    subject = 'У вас нове замовлення запчастин'
    message = render_to_string(
        'cart/test.html',
        {'cart': cart, 'total_products_price': total_products_price,
         'flag': flag, 'domain': current_site.domain, 'protocol': 'http',
         'dict_user_info': dict_user_info, 'users_cars': users_cars, 'orders_info': orders_info
         }

    )
    # message = 'Bot'
    send_mail(subject, message, from_email, ['kuchriavy10@gmail.com'], html_message=message,
              fail_silently=True)


def get_users_cars(request):
    final_list = []
    # get car/s of user if he is authorization
    b = Cars.objects.filter(user_id=request.user.id)
    if len(b) == 0:
        little_dict = dict()
        little_dict['Авто '] = "не вказано"
        final_list.append(little_dict)
    else:

        num = 1
        for i in b:
            little_dict = dict()
            status_of_car = ''
            if i.is_main_car:
                status_of_car = "   Головне авто"
            little_dict[f'{num}. Марка: '] = i.marka + '  ' + status_of_car
            little_dict['   Модель: '] = i.model
            final_list.append(little_dict)
            num += 1
    return final_list


def is_user_buy_products(request, my_email):
    flag = ''
    final_dict = dict()
    if request.user.is_authenticated:
        flag = True
    else:
        flag = False

    try:
        b = User.objects.get(email=my_email)
        flag = True
    except User.DoesNotExist:
        flag = False

    if not flag:
        final_dict['Статус користувача: '] = 'Не зареєстрований'
    else:
        final_dict['Статус користувача: '] = 'Зареєстрований'

    if flag:
        b = User.objects.get(email=my_email)
        final_dict['login: '] = b.username
        final_dict['email: '] = b.email
        final_dict['Ім`я: '] = b.first_name
        final_dict['Прізвище: '] = b.last_name

    return final_dict


def parse_dict(my_dict):
    final_dict = dict()
    for k, v in my_dict.items():
        if k == 'pay_method_id' or k == 'is_authenticated' or k == 'captcha_0' or k == 'captcha_0' or k == 'csrfmiddlewaretoken':
            continue
        elif k == 'delivery_method_id':
            if v[0] == '1':
                method_order = 'САМОВИВІЗ'
                final_dict['Метод замовлення: '] = method_order
            else:
                method_order = "Доставка Нова Пошта"
                final_dict['Метод замовлення: '] = method_order
        elif k == 'full_name':
            final_dict['ПІБ: '] = v[0]
        elif k == 'email':
            final_dict['email: '] = v[0]
        elif k == 'phone_number':
            final_dict['Номер телефону: '] = v[0]
        elif k == 'address_order_city':
            final_dict['Адреса доставки (Місто): '] = v[0]
        elif k == 'address_order_vidd':
            final_dict['Адреса доставки (Відділення): '] = v[0]
        elif k == 'comment_to_order':
            final_dict['Коментар до замовлення: '] = v[0]

    return final_dict



