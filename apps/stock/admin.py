from django.contrib import admin

from .choices import StockBuySellChoices
from .forms import PortfolioStockItemForm
from .models import Stock, Portfolio, PortfolioStockItem, Transaction


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'symbol',)
    search_fields = ('title',)
    # autocomplete_fields = ('parent',)
    # prepopulated_fields = {"slug": ("title",)}
    list_per_page = 5


class PortfolioStockItemTabularInline(admin.TabularInline):
    # model = PortfolioStockItem
    model = Portfolio.stocks.through
    # form = PortfolioStockItemForm
    # fields = ('stock', 'amount',)
    # readonly_fields = ('stock', 'amount_stock_item', 'investment_stock_item',)
    readonly_fields = ('amount_stock_item', 'investment_stock_item',)
    extra = 0
    max_num = 4
    autocomplete_fields = ('stock',)


@admin.register(PortfolioStockItem)
class PortfolioStockItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount_stock_item',)
    # search_fields = ('title',)
    # autocomplete_fields = ('parent',)
    # prepopulated_fields = {"slug": ("title",)}
    form = PortfolioStockItemForm
    # fields = ('portfolio', 'stock',)
    readonly_fields = ('amount_stock_item', 'investment_stock_item')
    autocomplete_fields = ('stock', 'portfolio')
    list_per_page = 5

    def save_model(self, request, obj: PortfolioStockItem, form: PortfolioStockItemForm, change):
        portfolio = form.cleaned_data.get('portfolio')
        stock = form.cleaned_data.get('stock')
        # amount_stock_item = form.cleaned_data.get('amount_stock_item')
        # investment_stock_item = form.cleaned_data.get('investment_stock_item')
        # print('-------------------------------------------------------------')
        # print(f'portfolio type is : {type(portfolio)}')
        # print(f'portfolio is : {portfolio}')
        # print(f'stock type is : {type(stock)}')
        # print(f'stock is : {stock}')
        # print(f'amount_stock_item is : {amount_stock_item}')
        # print(f'investment_stock_item is : {investment_stock_item}')

        price_amount = form.cleaned_data.get('price_amount')
        stock_choice = form.cleaned_data.get('stock_choice')
        # print(f'price is : {price}')
        # print(f'stock_choice is : {stock_choice}')

        transaction_date = form.cleaned_data.get('transaction_date')
        # print(f'transaction_date is : {transaction_date}')
        # print(f'transaction_date type is : {type(transaction_date)}')

        # form_data = form.cleaned_data
        # print(f'form_data is : {form_data}')
        # print('-------------------------------------------------------------')
        #
        # print(f'obj type is : {type(obj)}')
        # print(f'obj portfolio is : {type(obj.portfolio)}')
        # print(f'obj portfolio is : {obj.portfolio}')
        # print(f'obj portfolio is : {obj.portfolio.pk}')
        # print(f'obj stock is : {type(obj.stock)}')
        # print(f'obj stock is : {obj.stock}')
        # print(f'obj stock is : {obj.stock.pk}')
        # print(f'obj amount_stock_item is : {obj.amount_stock_item}')
        # print(f'obj investment_stock_item is : {obj.investment_stock_item}')

        # Buy stock
        if stock_choice == StockBuySellChoices.BUY:
            # obj.buy_stock(price, transaction_date)
            obj.buy_stock_admin(obj=obj, price=price_amount, transaction_date=transaction_date)
        # Sell stock
        elif stock_choice == StockBuySellChoices.SELL:
            obj.sell_stock_admin(obj=obj, amount=price_amount, transaction_date=transaction_date)
        else:
            super().save_model(request, obj, form, change)

        # # super(PortfolioStockItemAdmin, self).save_model(request, obj, form, change)
        # super().save_model(request, obj, form, change)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'balance', 'investment',
        # 'get_product_image'
    )
    readonly_fields = ('investment',)

    # autocomplete_fields = ('category', 'product_class')
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title',)

    inlines = (
        PortfolioStockItemTabularInline,
    )
    list_per_page = 5

    # def get_queryset(self, obj):
    #     qs = super(ProductAdmin, self).get_queryset(obj)
    #     return qs.prefetch_related('product_images')
    #
    # @admin.display(description=_('image preview'))
    # def get_product_image(self, obj):
    #     product_image_obj = obj.product_images.first()
    #     if product_image_obj is not None:
    #         return product_image_obj.img_preview()
    #     else:
    #         return None


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'portfolio_stock_item',
        'buying_price', 'deposit_amount',
        'selling_price', 'withdraw_amount',
        'transaction_date',
    )
    search_fields = ('transaction_date',)
    # prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20
