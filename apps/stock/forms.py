from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .choices import StockBuySellChoices
from .models import PortfolioStockItem


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class PortfolioStockItemForm(forms.ModelForm):
    # price = forms.DecimalField(max_digits=10, decimal_places=2, initial=0, label='Buy pricing | sell amount')
    price_amount = forms.FloatField(initial=0, label='Buy pricing | sell amount')
    transaction_date = forms.DateTimeField(label='transaction date (Buy | Sell)', required=False, widget=DateInput())
    stock_choice = forms.ChoiceField(
        choices=StockBuySellChoices.choices,
        initial=StockBuySellChoices.NONE,
        label='Stock (Buy | Sell)'
    )
    # transaction_date = forms.DateTimeField(label='transaction date', widget=AdminSplitDateTime())
    # transaction_date = forms.DateTimeField(label='transaction date', widget=forms.DateTimeInput())
    # transaction_date = forms.DateTimeField(label='transaction date', widget=DateTimeInput())

    # def clean_price_amount(self):
    #     print('................................................................')
    #
    #     price_amount = self.cleaned_data.get('price_amount')
    #     print(f'validation for price_amount : {price_amount}')
    #     if price_amount < 0 or price_amount is None:
    #         print(f'ValidationError for price_amount: {price_amount}')
    #         raise ValidationError(
    #             _("price|amount must be grater than 0, Invalid value: %(value)s"),
    #             params={"value": price_amount},
    #         )
    #     print('................................................................')

    def clean(self):
        # super(PortfolioStockItemForm, self).clean()
        cleaned_data = super().clean()

        choice = cleaned_data.get('stock_choice')
        price_amount = cleaned_data.get('price_amount')
        # print(f'cleaned_data is {self.cleaned_data} ')
        # print(f'price_amount is {price_amount} ')
        # print(f'stock_choice is {choice} ')

        if choice == StockBuySellChoices.SELL or choice == StockBuySellChoices.BUY:
            if cleaned_data.get('transaction_date') is None:
                raise ValidationError(_("Transaction date, Invalid value: %(value)s"), params={"value": "None"},)
        # if choice == StockBuySellChoices.BUY and self.cleaned_data.get('price') <= 0:
        if choice == StockBuySellChoices.BUY and price_amount <= 0:
            # raise ValidationError(
            # _("Buy pricing, Invalid value: %(value)s"),
            # params={"value": self.cleaned_data.get('price')},
            # )
            raise ValidationError(_("Buy pricing, Invalid value: %(value)s"), params={"value": price_amount}, )
        # if choice == StockBuySellChoices.SELL and self.cleaned_data.get('price') <= 0:
        if choice == StockBuySellChoices.SELL and (price_amount is None or price_amount <= 0):
            # raise ValidationError(
            # _("sell amount, Invalid value: %(value)s"),
            # params={"value": self.cleaned_data.get('price')},
            # )
            raise ValidationError(_("sell amount, Invalid value: %(value)s"), params={"value": price_amount}, )

    # def save(self, commit=True):
    #     return super().save(commit)

    class Meta:
        model = PortfolioStockItem
        # fields = '__all__'
        fields = ('portfolio', 'stock', 'amount_stock_item', 'investment_stock_item')
        # widgets = {
        #     # 'transaction_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        #     # 'transaction_date': DateInput(),
        # }
