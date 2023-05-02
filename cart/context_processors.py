from .cart import Cart
from users.models import Profile


def cart(request):
    flag = ''
    if request.user.is_authenticated:
        id_of_current_user = request.user.id
        get_object_user = Profile.objects.get(user_id=id_of_current_user)

        new_or_not = get_object_user.is_new_user
        if new_or_not:
            flag = True

    sections = 'Old_user'
    if flag:
        sections = 'New_user'

    return {'cart': Cart(request), 'sections': sections}
