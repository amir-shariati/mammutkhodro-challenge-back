import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db import IntegrityError, transaction
from decimal import Decimal
from utils.yahooFinance import Ticker
from .choices import StockNameChoices, StockSymbolChoices


# class Portfolio(models.Model):
#     user = models.modelsForeignKey('User',...)
#     # <other portfolio specific information>
#
#
# class Stock(models.Model):
#     ticker = models.CharField(...)
#     portfolio = models.ForeignKey('Portfolio', ...)
#
#
# class Transaction(models.Model):
#     stock = models.ForeignKey('Stock')
#     # <other transaction specific data>


class Stock(models.Model):
    # title = models.CharField(max_length=64, db_index=True, verbose_name=_('Stock title'))
    title = models.CharField(
        max_length=10,
        db_index=True,
        unique=True,
        choices=StockNameChoices.choices,
        default=StockNameChoices.GOLD,
        verbose_name=_('Stock title')
    )
    # slug = models.SlugField(unique=True, db_index=True, allow_unicode=True)
    slug = models.SlugField(unique=True, db_index=True, allow_unicode=True, editable=False)
    # symbol = models.CharField(max_length=10, editable=False, verbose_name=_('Stock symbol'))
    # symbol = models.CharField(max_length=10, verbose_name=_('Stock symbol'))
    symbol = models.CharField(
        max_length=10,
        unique=True,
        choices=StockSymbolChoices.choices,
        # default=StockSymbolChoices.GOLD,
        editable=False,
        verbose_name=_('Stock symbol')
    )
    # ticker = models.CharField(max_length=10, editable=False, verbose_name=_('Stock ticker'))

    # portfolio = models.ForeignKey('Portfolio', on_delete=models.SET_NULL, related_name='stocks')

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        self.slug = slugify(self.title, allow_unicode=True)
        self.symbol = StockSymbolChoices[self.get_title_display()]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')


class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_histories', verbose_name=_('Stock history'))
    open = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history open'))
    high = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history high'))
    low = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history low'))
    close = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history close'))
    volume = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history volume'))
    dividends = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history dividends'))
    stock_splits = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Stock history splits'))

    date_time = models.DateTimeField(null=True, blank=True, editable=False, verbose_name=_('Stock history dateTime'))

    def __str__(self):
        return f'{self.stock} , {self.date_time}'

    class Meta:
        verbose_name = _('Stock History')
        verbose_name_plural = _('Stocks Histories')


class PortfolioStockItem(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='Portfolio_Stock_Items')
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name='Portfolio_Items')

    # value_float = models.FloatField(null=True, blank=True, verbose_name=_('Value float'))
    # price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # change = models.DecimalField(max_digits=10, decimal_places=2)
    # stocks_owned = models.IntegerField()

    # buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    # # bought_on = models.DateTimeField(null=True, blank=True, editable=False, verbose_name=_('Bought on'))
    # bought_on = models.DateTimeField(null=True, blank=True, verbose_name=_('Bought on'))

    # amount = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Amount'))
    # amount_stock_item = models.FloatField(null=True, blank=True, verbose_name=_('Amount'))
    amount_stock_item = models.FloatField(default=0, verbose_name=_('Amount'))
    investment_stock_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Investment'))

    @property
    def title(self):
        return f'stock item for {self.portfolio} , {self.stock}'

    def set_amount_stock_item(self, amount):
        self.amount_stock_item = amount

    # def buy_stock(self, investment_amount):
    #     portfolio_investment = self.portfolio.investment
    #     portfolio_balance = self.portfolio.balance
    #     if portfolio_balance > investment_amount:
    #         with transaction.atomic():
    #             self.portfolio.balance = portfolio_balance - investment_amount
    #             self.portfolio.investment = portfolio_investment + investment_amount
    #             self.portfolio.save()
    #
    #         print('========================================')
    #         print(f'stock investment is {self.investment_stock_item + investment_amount}')
    #         print(f'total investment is {portfolio_investment}')
    #         print('========================================')

    def buy_stock_admin(self, obj, price, transaction_date):
    # def buy_stock(self, price, transaction_date):
        portfolio_investment = self.portfolio.investment
        portfolio_balance = self.portfolio.balance
        # price = Decimal.from_float(price)
        if portfolio_balance > price:
            with transaction.atomic():
                # Yahoo Finance info
                print('=========================================================')
                # print(f'stock {self.stock.symbol} info')
                # print(f'stock {obj.stock.symbol} info')
                # ticker = Ticker(self.stock.symbol)
                ticker = Ticker(obj.stock.symbol)
                ticker_row_df = ticker.get_stock_history_date(start=transaction_date)

                ticker_values_dict = Ticker.get_row_values(ticker_row_df)
                print(f'stock {self.stock.symbol} info : {ticker_values_dict}')

                ticker_close_value = Ticker.get_row_close_value(ticker_row_df)
                print(f'stock {self.stock.symbol} close value : {ticker_close_value}')

                # stock_amount = float(price)/ticker_close_value
                stock_amount = price/ticker_close_value
                print(f'stock {self.stock.symbol} amount : {stock_amount}')

                # Stock item instance
                print(f' type of amount_stock_item is : {type(self.amount_stock_item)}')
                print(f' type of stock_amount is : {type(stock_amount)}')
                # self.amount_stock_item = self.amount_stock_item + 1
                self.amount_stock_item = stock_amount if self.amount_stock_item is None else self.amount_stock_item + stock_amount
                # self.investment_stock_item = self.investment_stock_item + price
                self.investment_stock_item = self.investment_stock_item + Decimal.from_float(price)
                obj.save()

                # Portfolio instance
                # self.portfolio.balance = portfolio_balance - price
                self.portfolio.balance = portfolio_balance - Decimal.from_float(price)
                # self.portfolio.investment = portfolio_investment + price
                self.portfolio.investment = portfolio_investment + Decimal.from_float(price)
                self.portfolio.save()

                # Transactions instance
                # self.transactions.create(buying_price=price, deposit_amount=1, transaction_date=transaction_date)
                self.transactions.create(buying_price=price, deposit_amount=stock_amount, transaction_date=transaction_date)

    # def admin_buy_stock(self, investment_amount, ):
    #     ...

    def sell_stock_admin(self, obj, amount, transaction_date):
        portfolio_investment = self.portfolio.investment
        portfolio_balance = self.portfolio.balance
        if self.amount_stock_item >= amount:
            with transaction.atomic():
                # Yahoo Finance info
                print('=========================================================')
                ticker = Ticker(obj.stock.symbol)
                ticker_row_df = ticker.get_stock_history_date(start=transaction_date)

                ticker_values_dict = Ticker.get_row_values(ticker_row_df)
                print(f'stock {self.stock.symbol} info : {ticker_values_dict}')

                ticker_close_value = Ticker.get_row_close_value(ticker_row_df)
                print(f'stock {self.stock.symbol} close value : {ticker_close_value}')

                price = ticker_close_value * amount
                print(f'stock {self.stock.symbol} sell price : {price}')

                # Portfolio instance
                self.portfolio.balance = portfolio_balance + Decimal.from_float(price)
                # self.portfolio.investment = portfolio_investment + Decimal.from_float(price)
                self.portfolio.save()

                # Transactions instance
                self.transactions.create(
                    # buying_price=price,
                    selling_price=price,
                    withdraw_amount=amount,
                    transaction_date=transaction_date
                )

                # Stock item instance
                self.amount_stock_item = self.amount_stock_item - amount
                # self.amount_stock_item = stock_amount if self.amount_stock_item is None else self.amount_stock_item + stock_amount
                self.investment_stock_item = self.investment_stock_item + Decimal.from_float(price)
                obj.save()


    def __str__(self):
        return f'{self.portfolio} , {self.stock}'

    class Meta:
        verbose_name = _('Portfolio Stock Item')
        verbose_name_plural = _('Portfolio Stock Items')
        unique_together = ('stock', 'portfolio')


class Portfolio(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name=_('Portfolio title'))
    stocks = models.ManyToManyField(Stock, through=PortfolioStockItem)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100000)
    investment = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def invest(self, amount):
        if self.balance > amount:
            self.balance = self.balance - amount

    def __str__(self):
        return f'{self.title} , {self.investment}, {self.balance}'

    class Meta:
        verbose_name = _('Portfolio')
        verbose_name_plural = _('Portfolios')


class Transaction(models.Model):
    portfolio_stock_item = models.ForeignKey(PortfolioStockItem, on_delete=models.CASCADE, related_name='transactions')

    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Buying price'))
    # deposit_amount = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Deposit amount'))
    deposit_amount = models.FloatField(null=True, blank=True, verbose_name=_('Deposit amount'))
    # # bought_on = models.DateTimeField(null=True, blank=True, editable=False, verbose_name=_('Bought on'))
    # bought_on = models.DateTimeField(null=True, blank=True, verbose_name=_('Bought on'))

    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Selling price'))
    # withdraw_amount = models.FloatField(null=True, blank=True, editable=False, verbose_name=_('Withdraw amount'))
    withdraw_amount = models.FloatField(null=True, blank=True, verbose_name=_('Withdraw amount'))
    # sold_on = models.DateTimeField(null=True, blank=True, verbose_name=_('Sold on'))

    transaction_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Transaction date'))

    def admin_buy_transaction(self, stock_item, investment_amount):
        pass

    # def save(self, *args, **kwargs):
    #     with transaction.atomic():
    #         print(f' stock item amount : {self.portfolio_stock_item.amount_stock_item}')
    #
    #         self.portfolio_stock_item.buy_stock(random.randint(1,10))
    #
    #         super(Transaction, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # self.portfolio_stock_item.amount_stock_item = 5555
    #     # super(Transaction, self).save(*args, **kwargs)
    #     print(f' stock item amount : {self.portfolio_stock_item.amount_stock_item}')
    #     self.update_portfolio_stock_item(*args, **kwargs)
    #     super(Transaction, self).save(*args, **kwargs)
    #
    #     # self.portfolio_stock_item.save()
    #     # self.save_portfolio_stock_item_related()
    #
    # # # Creating a custom method
    # # def save_portfolio_stock_item_related(self):
    # #     self.portfolio_stock_item.save()
    # #     self.save()
    #
    # # def update_portfolio_stock_item(*args, **kwargs):
    # def update_portfolio_stock_item(self, *args, **kwargs):
    #     print('---------------------------------------')
    #     print('call update_portfolio_stock_item')
    #     with transaction.atomic():
    #         self.portfolio_stock_item.set_amount_stock_item(55555)
    #         self.portfolio_stock_item.save()
    #         # super(Transaction, self).save(*args, **kwargs)
    #         # transaction_obj = Transaction(*args, **kwargs)
    #         # transaction_obj.portfolio_stock_item.set_amount_stock_item(66666)
    #         # transaction_obj.portfolio_stock_item.save()
    #         # transaction_obj.save()

    # # PLAN_CHOICES = (
    # #     ("Basic - Daily 2% for 180 Days", "Basic - Daily 2% for 180 Days"),
    # #     ("Premium - Daily 4% for 360 Days", "Premium - Daily 4% for 360 Days"),
    # # )
    # # plan = models.CharField(max_length=100, choices=PLAN_CHOICES, null=True)
    # deposit_amount = models.IntegerField(default=0, null=True)
    # # basic_interest = models.IntegerField(default=0, null=True)
    # # premium_interest = models.IntegerField(default=0, null=True)
    # investment_return = models.IntegerField(default=0, null=True)
    # withdraw_amount = models.IntegerField(default=0, null=True, blank=True)
    # balance = models.IntegerField(default=0, null=True, blank=True)
    # total_available_balance = models.IntegerField(default=0, null=True, blank=True)
    # locked_balance = models.IntegerField(default=0, null=True, blank=True)
    # investment_id = models.CharField(max_length=10, null=True, blank=True)
    # is_active = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now=True, null=True)
    # due_date = models.DateTimeField(null=True)


    # def save(self, *args, **kwargs):
    #     if self.plan == "Basic - Daily 2% for 180 Days":
    #         self.basic_interest =  self.deposit_amount * 365 * 0.02/2
    #         self.investment_return = self.deposit_amount + self.basic_interest
    #         self.due_date = datetime.now() + timedelta(seconds=5)
    #     else:
    #         self.premium_interest = self.deposit_amount*365*0.04
    #         self.investment_return = self.deposit_amount +self.premium_interest
    #         self.due_date = datetime.now() + timedelta(seconds=5)
    #     super(Investment, self).save(*args, **kwargs)

    def __str__(self):
        return f'Transaction for {self.portfolio_stock_item} on {self.transaction_date}'

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


# class Transaction(models.Model):
#     # stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
#
#     ######################################################################################
#     # date = models.DateTimeField("Transaction's date", auto_now=True)
#     # order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     #
#     # total_profit = models.IntegerField("Transaction's Profit", default=0)
#     # total_cost = models.IntegerField("Transaction's Income", default=0)
#     # total_income = models.IntegerField("Transaction's Income", default=0)
#     #
#     # def __str__(self):
#     #     return f"Transaction #{self.pk}"
#     #
#     # # Here is the issue, I do not know how to save this calculations
#     #
#     # def calc_cost(self): pass
#     #     # for product in self.order.product.objects.all():
#     #     #     self.total_cost += product.price_cost()
#     #
#     # def calc_income(self): pass
#     #     # for product in self.order.product.objects.all():
#     #     #     self.total_income += product.price_sell()
#     #
#     # def calc_profit(self): pass
#     #     # self.total_profit = self.total_income - self.total_cost
#
#     ######################################################################################
#     # """This represents the individual transaction that a person has had."""
#     #
#     # user = models.ForeignKey(User, blank=False, null=False,
#     #                          help_text="The user this transaction relates to.")
#     # business = models.ForeignKey(Business, blank=False, null=False,
#     #                              help_text="The business that generated this expense.")
#     # amount = models.FloatField(blank=False, null=False,
#     #                            help_text="The amount charged.")
#     # date = models.DateField("Date charged", blank=False, null=False,
#     #                         help_text="The date the transaction occured.")
#     # tag = models.ManyToManyField(ExpenseType, blank=True, null=True,
#     #                              help_text="The expense type.")
#     # credit = models.BooleanField(blank=False, null=False,
#     #                              help_text="Is this a credit transation?")
#     #
#     # def __unicode__(self):
#     #     return u"[%s] - %s $%s" % (self.date, self.business, self.amount)
#     #
#     # class Meta:
#     #     ordering = ['date', 'business', 'amount']
#
#     ######################################################################################
#     # account = models.ForeignKey(Account)
#     # action = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
#     # date = models.DateField('transaction date')
#     # security = models.ForeignKey(Security)
#     # shares = models.DecimalField(decimal_places=4, max_digits=10, null=True)
#     # currency = models.ForeignKey(Currency)
#     # exchange_rate = models.DecimalField(decimal_places=4, max_digits=10,
#     # null=False, blank=False, default=Decimal('1.0'))
#     # price = models.DecimalField(decimal_places=4, max_digits=10, null=True)
#     # commission = models.DecimalField(decimal_places=2, max_digits=10,
#     #                                  null=True)
#     # cash_amount = models.DecimalField(decimal_places=2, max_digits=10,
#     #                                   null=True)
#     # sec_fee = models.DecimalField(decimal_places=2, max_digits=10, null=True)
#     # split_ratio = models.DecimalField(decimal_places=2, max_digits=5,
#     #                                   null=True)
#     #
#     # class Meta:
#     #     ordering = ['date']
#     #
#     # def __str__(self):
#     #     return self.action + ' ' + str(self.shares) + ' ' + self.security.name