from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import CustomAuthForm
from .models import Profile, Cars, Order
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import CustomAuthForm, RegisterForm, UpdateUserForm, UserImageForm, CarImageForm, UpdatePasswordForm
from .decorators import anonymous_required
from .token import token_generator


def check_order(status):
    print(status)


def login(request):
    if request.method == 'POST':
        x = dict(request.POST)
        # form = CustomAuthForm(request.POST)
        # if form.is_valid():
        #     data = form.cleaned_data
        #     user = authenticate(
        #         email=data['username'],
        #         password=data['password']
        #     )
        #     print(user == True)
        #     if user:
        #         auth_login(request, user)

        try:
            user = User.objects.get(email=x['email'][0])
            if user.is_active:
                if user.check_password(x['password'][0]):
                    auth_login(request, user)
                    messages.success(request, f'Ласкаво просимо, {user}')
                    return redirect('home')
                else:
                    messages.error(request, 'Невірно вказаний пароль, спробуйте ще раз')
                    return redirect('login')
            else:
                messages.error(request,
                               'Авторизуйте свій аккаунт у повідомленні відправленому на вашу пошту та спробуйте ще раз')
                return redirect('login')
        except User.DoesNotExist:
            print('flag')
            messages.error(request, 'Невірно вказано email, спробуйте ще раз')
            return redirect('login')

    form = CustomAuthForm()
    context = {'form': form}

    return render(request, 'users/user.html', context)


@anonymous_required(redirect_url='home')
def reset_password(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            try:
                user = User.objects.get(email=data)
                current_site = get_current_site(request)
                subject = 'Reset your password'
                message = render_to_string(
                    'users/reset_password_mail.html',
                    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': token_generator.make_token(user),
                    }
                )

                # send_mail(subject, message, 'kobra1903@ukr.net', ['test-ykf0q4akt@srv1.mail-tester.com'], html_message=message, fail_silently=True)

                user.email_user(subject, message, html_message=message)
                return redirect('reset_password_done')
            except User.DoesNotExist:
                messages.error(request, 'Користувача с таким email не існує')
                return redirect('login')
    form = PasswordResetForm()
    return render(request=request, template_name="users/reset_password.html",
                  context={"form": form})


@anonymous_required(redirect_url='home')
def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        req_dict = dict(request.POST)
        if req_dict['username'][0].strip() == '-' or req_dict['username'][0].strip() == '.' or req_dict['username'][
            0].strip() == '_' or \
                req_dict['username'][0].strip() == '/' or req_dict['username'][0].strip() == '@':
            messages.error(request, f'Не корректний логін, спробуйте інший')
            return redirect('registration')
        elif form.is_valid():
            user = form.cleaned_data.get('username')
            form.save()
            p = User.objects.get(email=form.cleaned_data.get('email'))
            p.is_active = False
            p.save()
            form.send_activation_email(request, p)

            messages.success(request,
                             f'{user}, на вашу електронну адресу відправлено повідомлення для підтвердження реєстрації. Перейдіть в пошту та підтвердіть реєстрацію. Якщо повідомлення не прийшло, перевірьте будь-ласка "СПАМ" або правильність вказаного email - {p.email}')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required()
def profile(request):
    if request.method == "POST":
        # блок если мы довляем машину в бд
        if 'marka' in request.POST:
            req_dict = dict(request.POST)
            req_img = dict(request.FILES)
            try:
                b = Cars(user_id=request.user.id, marka=req_dict['marka'][0], model=req_dict['model'][0],
                         img_of_avto=req_img['img_of_avto'][0])
                b.save()
            except KeyError:
                b = Cars(user_id=request.user.id, marka=req_dict['marka'][0], model=req_dict['model'][0])
                b.save()

            all_users_auto_objects = Cars.objects.all()
            for i in all_users_auto_objects:
                i.is_main_car = False
                i.save()

            user_image_avto = CarImageForm(request.POST, request.FILES, instance=request.user)
            if user_image_avto.is_valid():
                user_image_avto.save()
                return redirect('profile:profile')
        # блок если мы удаляем уже созданную модель машины из бд
        elif 'delete_car_button' in request.POST:
            req_dict = dict(request.POST)
            delete_car_object = Cars.objects.get(id=int(req_dict['delete_car_button'][0]))
            delete_car_object.delete()
            return redirect('profile:profile')
        # блок с обновлением данных клиента
        else:
            req_dict = dict(request.POST)
            full_name = Profile.objects.get(user_id=request.user.id)
            full_name.first_name = req_dict['first_name'][0]
            full_name.last_name = req_dict['last_name'][0]
            full_name.save()
            user_image_form = UserImageForm(request.POST, request.FILES, instance=request.user.profile)
            update_user_form = UpdateUserForm(request.POST, instance=request.user)

            if user_image_form.is_valid() and update_user_form.is_valid():
                user_image_form.save()
                update_user_form.save()
                messages.success(request, f'Ваші данні були успішно оновлені')
                return redirect('profile:profile')
            # обрабатываем все возможные ошибки введенных данных
            else:
                x = update_user_form.cleaned_data
                if 'email' not in x:
                    messages.error(request,
                                   f'Не коректно введений email або користувач з таким email вже зареєстрований на цьому сайті, будь-ласка спробуйте ще раз')
                    return redirect('profile:profile')
                request_dict = dict(request.POST)
                name_list = request_dict['username']
                messages.error(request,
                               f'Користувач з логіном {name_list[0]} вже зареєстрований на цьому сайті, спробуйте будь-ласка інший логін')
                return redirect('profile:profile')

    user_image_form = UserImageForm()
    update_user_form = UpdateUserForm(instance=request.user)
    # форма для загрузки фото машины
    user_avto_form = CarImageForm()

    list_for_flag = []
    # общий список машин юзера
    t = Cars.objects.filter(user_id=request.user.id).order_by('-is_main_car', '-date_field')

    orders_users = Order.objects.filter(user_id=request.user.id, is_completed_repair=False)
    for i in orders_users:
        if i.status == 'Готово':
            list_for_flag.append(True)
        else:
            list_for_flag.append(False)
            break
    flag = False if False in list_for_flag else True
    # если приходит гет запрос с галочкой
    if len(request.GET) > 0:
        req_dict = dict(request.GET)
        # если добавляем галочку
        if 'horns' in req_dict:
            car_id = int(req_dict['horns'][0])
            all_cars_objects = Cars.objects.filter(user_id=request.user.id)
            for i in all_cars_objects:
                i.is_main_car = False
                i.save()
            car_object_req = Cars.objects.get(id=car_id)
            car_object_req.is_main_car = True
            car_object_req.save()
        # убираем
        elif 'scales' in req_dict:
            car_id = int(req_dict['scales'][0])
            car_object_req = Cars.objects.get(id=car_id)
            car_object_req.is_main_car = False
            car_object_req.save()

    all_active_orders_of_user = Order.objects.filter(user_id=request.user.id, is_completed_repair=False).order_by(
        '-date_field')

    if len(t) == 1:
        for i in t:
            i.is_main_car = True
            i.save()

    # история заказов
    all_disactive_orders = Order.objects.filter(user_id=request.user.id, is_completed_repair=True).order_by(
        '-date_field')

    print(all_disactive_orders)
    print(len(all_disactive_orders))

    data = {
        'UserImageForm': user_image_form,
        'UpdateUserForm': update_user_form,
        'CarImageForm': user_avto_form,
        'OrderUserInfo': orders_users,
        'CarUserInfo': t,
        'Flag': flag,
        'UsersRepairs': all_active_orders_of_user,
        'AllDisactiveOrders': all_disactive_orders
    }

    return render(request, 'users/profile.html', data)


class ActivateView(RedirectView):
    url = reverse_lazy('login')

    # Custom get method
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            print(user.is_authenticated)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, f'{user}, ваш аккаунт зареєстрований, виконайте будь-ласка вхід')
            return super().get(request, uidb64, token)
        else:

            messages.success(request, f'Користувач з email - {user.email} вже активований')

            return render(request, 'users/activate_account_invalid.html')


class CheckEmailView(TemplateView):
    template_name = 'users/check_email.html'


class SuccessView(TemplateView):
    template_name = 'users/success.html'
