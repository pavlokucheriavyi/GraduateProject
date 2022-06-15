from django import forms
from captcha.fields import CaptchaField

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label='Кількість'
    )

    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()