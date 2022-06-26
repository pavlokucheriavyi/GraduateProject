import json
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse
from .models import Products, AvailableMarks, Category
from users.models import Order, TypeOfRepair, Cars
from django.utils import timezone
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from cart.forms import CartAddProductForm
from .models import AvailableMarks, PidMarks
from users.models import TypeOfRepair
from .cars_dict import cars

from .forms import SearchForm, RepairForm


def home(request):
    start = 'Hello Kolischa'
    all_types_of_repair = TypeOfRepair.objects.all()
    data = {
        'AllTypesOfRepair': all_types_of_repair
    }

    return render(request, 'shop/home.html', data)


class ProductsView(ListView):
    model = Products
    template_name = 'shop/shop.html'
    context_object_name = 'products_list'
    paginate_by = 6
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        form = SearchForm(self.request.POST or None)
        ctx = super(ProductsView, self).get_context_data(**kwargs)
        category_list = Category.objects.all()
        pid_list = PidMarks.objects.all()
        same_button = 'pid_butt'

        ctx['same_button'] = same_button
        ctx['pid_marks'] = pid_list
        ctx['category_list'] = category_list
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
    print(request.POST)
    if 'pid_butt' in request.POST:
        if 'category' in request.POST:
            category = request.POST.get('category')
            if category == 'Підшипники маточини (втулки)':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Підшипники маточини (втулки)')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
            elif category == 'Комплекти зчеплення':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Комплекти зчеплення')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                flag = 'pid'
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list, 'marka': marka})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
            elif category == 'Тормозні диски ПЕРЕДНІ':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Тормозні диски ПЕРЕДНІ')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
            elif category == 'Тормозні диски ЗАДНІ':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Тормозні диски ЗАДНІ')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
            elif category == 'Склоочисники':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Склоочисники')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                flag = 'pid'
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list, 'marka': marka})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
            elif category == 'Гальмові колодки':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Гальмові колодки')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                flag = 'pid'
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list, 'marka': marka})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
            elif category == 'Важелі підвіски':
                marka = request.POST.get('pid_butt')
                b = Products.objects.filter(category__category='Важелі підвіски')
                empty_list = []
                for item in b:
                    if marka in item.description:
                        empty_list.append(item)

                if len(empty_list) == 0:
                    return HttpResponse('Немає в наявності' + '*' + marka)
                flag = 'pid'
                html = render_to_string('shop/ajax/shop.html', {'data': empty_list, 'marka': marka})
                return JsonResponse({'data': html + '*' + marka + '*' + 'with_category'})
        else:
            marka = request.POST.get('pid_butt')
            b = Products.objects.all()
            empty_list = []
            for item in b:
                if marka in item.description:
                    empty_list.append(item)

            if len(empty_list) == 0:
                return HttpResponse('Немає в наявності')
            flag = 'pid'
            html = render_to_string('shop/ajax/shop.html', {'data': empty_list, 'flag': flag})
            return JsonResponse({'data': html + '*' + marka})
    else:
        stuff = request.POST.get('cat')
        tags = Products.objects.all().filter(category__category=stuff).order_by('-date')
        # код для сохранения данных из json в бд
        # for k, v in cars['list'].items():
        #     b2 = AvailableMarks(name=f'{k}', is_available=True)
        #     b2.save()
        #     print('good')

        html = render_to_string('shop/ajax/shop.html', {'data': tags})
        return JsonResponse({'data': html + '*' + stuff})


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
    types_of_repair_list = []
    # открываем json с доступными марками
    f = open('shop/is_available.json')
    data = json.load(f)

    all_types_of_repair = TypeOfRepair.objects.all()
    for i in all_types_of_repair:
        types_of_repair_list.append(i.type)

    if request.method == 'POST':
        current_user_id = request.user.id
        req_dict = dict(request.POST)
        # собираем данные с пост запроса про юзера и форматируем
        # их в нужном формате
        current_type_of_repair = req_dict['type_of_repair'][0]
        type_object = TypeOfRepair.objects.get(type=current_type_of_repair)
        first_name = req_dict['Name_of_user'][0]
        last_name = '----'
        is_available_mark = req_dict['marka'][0]

        if request.user.is_authenticated and req_dict['marka'][0] != '' and req_dict['marka'][0] in data:
            user_object = User.objects.get(id=current_user_id)
            user_surname = user_object.last_name
            user_name = user_object.first_name
            user_email = user_object.email

            is_available_object = AvailableMarks.objects.get(name=is_available_mark)
            if is_available_object.is_available:
                dict_for_whatsapp_bot = {'Статус користувача: ': 'Авторизований',
                                         'Логін: ': user_object.username,
                                         'email: ': user_email,
                                         'Імʼя: ': user_name,
                                         'Прізвище: ': user_surname,
                                         'Телефон: ': req_dict['phone_number'][0],
                                         'Тип: ': type_object.type,
                                         'Марка: ': req_dict['marka'][0],
                                         'Модель: ': req_dict['model'][0],
                                         'Рік авто: ': req_dict['year'][0]
                                         }

                message(request, dict_for_whatsapp_bot)

                b = Order(user=user_object, first_name=user_name, last_name=user_surname,
                          phone_number=req_dict['phone_number'][0], type=type_object,
                          marka=req_dict['marka'][0], model=req_dict['model'][0], year_of_car=req_dict['year'][0])
                b.save()

        elif request.user.is_authenticated and (req_dict['marka'][0] == '' or req_dict['marka'][0] not in data):
            user_object = User.objects.get(id=current_user_id)
            user_surname = user_object.last_name
            user_name = user_object.first_name
            user_email = user_object.email

            dict_for_whatsapp_bot = {'Статус користувача: ': 'Авторизований',
                                     'Логін: ': user_object.username,
                                     'email: ': user_email,
                                     'Імʼя: ': user_name,
                                     'Прізвище: ': last_name,
                                     'Телефон: ': req_dict['phone_number'][0],
                                     'Тип: ': type_object.type,
                                     'Марка: ': req_dict['marka'][0],
                                     'Модель: ': req_dict['model'][0],
                                     'Рік авто: ': req_dict['year'][0]
                                     }

            message(request, dict_for_whatsapp_bot)

            b = Order(user=user_object, first_name=user_name, last_name=user_surname,
                      phone_number=req_dict['phone_number'][0], type=type_object,
                      marka=req_dict['marka'][0], model=req_dict['model'][0], year_of_car=req_dict['year'][0])
            b.save()

        elif not request.user.is_authenticated and req_dict['marka'][0] != '' and req_dict['marka'][0] in data:
            is_available_object = AvailableMarks.objects.get(name=is_available_mark)
            if is_available_object.is_available:
                dict_for_whatsapp_bot = {'Статус користувача: ': 'Не авторизований',
                                         'Імʼя: ': first_name,
                                         'Прізвище: ': last_name,
                                         'Телефон: ': req_dict['phone_number'][0],
                                         'Тип: ': type_object.type,
                                         'Марка: ': req_dict['marka'][0],
                                         'Модель: ': req_dict['model'][0],
                                         'Рік авто: ': req_dict['year'][0]
                                         }

                message(request, dict_for_whatsapp_bot)

                b = Order(first_name=first_name, last_name=last_name, phone_number=req_dict['phone_number'][0],
                          type=type_object, marka=req_dict['marka'][0], model=req_dict['model'][0],
                          year_of_car=req_dict['year'][0])
                b.save()

        elif not request.user.is_authenticated and (req_dict['marka'][0] == '' or req_dict['marka'][0] not in data):
            dict_for_whatsapp_bot = {'Статус користувача: ': 'Не авторизований',
                                     'Імʼя: ': first_name,
                                     'Прізвище: ': last_name,
                                     'Телефон: ': req_dict['phone_number'][0],
                                     'Тип: ': type_object.type,
                                     'Марка: ': req_dict['marka'][0],
                                     'Модель: ': req_dict['model'][0],
                                     'Рік авто: ': req_dict['year'][0]
                                     }

            message(request, dict_for_whatsapp_bot)

            b = Order(first_name=first_name, last_name=last_name, phone_number=req_dict['phone_number'][0],
                      type=type_object, marka=req_dict['marka'][0], model=req_dict['model'][0],
                      year_of_car=req_dict['year'][0])
            b.save()

        return redirect('home')

    else:
        users_name = ''
        users_surname = ''
        main_marka = ''
        main_model = ''
        if request.user.is_authenticated:
            t = Cars.objects.filter(user_id=request.user.id)
            name_of_user = User.objects.get(id=request.user.id)
            for i in t:
                if i.is_main_car:
                    main_marka = i.marka
                    main_model = i.model

            users_name = name_of_user.first_name
            users_surname = name_of_user.last_name

        is_available_list = AvailableMarks.objects.all()
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
                       'My_json': json_dict, 'main_marka': main_marka, 'main_model': main_model,
                       'users_name': users_name, 'users_surname': users_surname})


account_sid = 'ACba3baf85b063f2614c78765409b68bb8'
auth_token = 'd0832b32d4e0c2e684f025ae503078b9'
client = Client(account_sid, auth_token)


@csrf_exempt
def message(request, something):
    print(something)
    user = request.POST.get('From')
    message = request.POST.get('Body')
    export_string = 'У вас нове замовлення ремонту!\n ---------------------------------\n'

    for k, v in something.items():
        export_string = export_string + k + v + '\n'

    client.messages.create(
        from_='whatsapp:+14155238886',
        body=export_string,
        to='whatsapp:+380662196787'
    )
    return HttpResponse("halo")
