from decimal import Decimal
from django.conf import settings
from shop.models import Products
from django.http import JsonResponse
from django.template.loader import render_to_string


class Cart(object):
    """
        Initialization constructor of cart
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        num = []
        for k in self.cart.keys():
            try:
                x = Products.objects.get(id=int(k))
            except Products.DoesNotExist:
                num.append(int(k))

        for item in num:
            del self.cart[str(item)]

    def __iter__(self):
        """
            Recycle(перебираем) products in the cart and getting products from the data base.
        """
        product_ids = self.cart.keys()
        # get products and add in to the cart
        products = Products.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            product = Products.objects.get(id=item['product'].id)
            item['price'] = float(product.price)
            item['total_price'] = "%.2f" % float(item['price'] * item['quantity'])
            # print(item, 'GOOD')
            yield item

    def __len__(self):
        """
            Counting how many items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    # def get_info_product(self, product_id):
    #     products = Products.objects.filter(id=product_id)
    #
    #     # for item in self.cart.values():
    #     #     item['price'] = float(item['price'])
    #
    #     return list(products)[0].count

    def delete(self):
        self.cart.clear()
        self.save()

    def add(self, product, quantity=1, update_quantity=False):
        """
            Add products in to the cart, or update quantity
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            product = Products.objects.get(id=product.id)
            self.cart[product_id]['price'] = float(product.price)
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # save product
        self.session.modified = True

    # def get_cart(self):
    #     empty_list = []
    #     product_ids = self.cart.keys()
    #     # get products and add in to the cart
    #     products = Products.objects.filter(id__in=product_ids)
    #
    #     cart = self.cart.copy()
    #     for product in products:
    #         cart[str(product.id)]['product'] = product
    #
    #     for item in self.cart.values():
    #         item['price'] = float(item['price'])
    #         item['total_price'] = item['price'] * item['quantity']
    #         # print(item, 'GOOD')
    #         print(item)

    def get_total_price(self):
        # print(self.cart.values())
        # print(self.cart.keys())
        result_list = []
        # for i in self.cart.values():
        #     print(i)
        return "%.2f" % float(sum(float(item['price']) * item['quantity'] for item in self.cart.values()))

    def remove(self, product):
        """
            Remove product
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()
