my_dict = {'delivery_method_id': ['9'], 'pay_method_id': ['1'], 'full_name': ['asvasd'], 'email': ['kuchriavy10@maslo.com'], 'phone_number': ['1234'], 'is_authenticated': ['43'], 'address_order_city': [''], 'address_order_vidd': [''], 'comment_to_order': [''], 'captcha_0': ['48b7165376a32b05cabbcc4877f7c087be61c6a6'], 'captcha_1': ['CHGU'], 'csrfmiddlewaretoken': ['sc179AjAyybcZVfnDQpUWvg0hL7gkDXOwpKpjDsKYLEeyEAfVXU6tWr35wF500YY']}

def parse_dict(my_dict):
    final_dict = dict()
    for k, v in my_dict.items():
        if k == 'pay_method_id' or k == 'is_authenticated' or k == 'captcha_0' or k == 'captcha_0' or k == 'csrfmiddlewaretoken':
            continue
        elif k == 'delivery_method_id':
            if v[0] == '1':
                method_order = 'САМОВИВОЗ'
                final_dict['Метод замовлення'] = method_order
            else:
                method_order = "Доставка Нова Пошта"
                final_dict['Метод замовлення'] = method_order
        elif k == 'full_name':
            final_dict['ПІБ'] = v[0]
        elif k == 'email':
            final_dict['email'] = v[0]
        elif k == 'phone_number':
            final_dict['Номер телефону: '] = v[0]
        elif k == 'address_order_city':
            final_dict['Адреса доставки (Місто): '] = v[0]
        elif k == 'address_order_vidd':
            final_dict['Адреса доставки (Відділення): '] = v[0]
        elif k == 'comment_to_order':
            final_dict['Коментар до замовлення: '] = v[0]

    return final_dict


print(parse_dict(my_dict))