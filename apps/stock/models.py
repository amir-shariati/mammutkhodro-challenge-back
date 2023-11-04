import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db import IntegrityError, transaction
from decimal import Decimal
from utils.yahooFinance import Ticker
from .choices import StockNameChoices, StockSymbolChoices


class Stock(models.Model):
    title = models.CharField(
        max_length=10,
        db_index=True,
        unique=True,
        choices=StockNameChoices.choices,
        default=StockNameChoices.GOLD,
        verbose_name=_('Stock title')
    )
    slug = models.SlugField(unique=True, db_index=True, allow_unicode=True, editable=False)
    symbol = models.CharField(
        max_length=10,
        unique=True,
        choices=StockSymbolChoices.choices,
        editable=False,
        verbose_name=_('Stock symbol')
    )

    def save(self, *args, **kwargs):
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
    amount_stock_item = models.FloatField(default=0, verbose_name=_('Amount'))
    investment_stock_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Investment'))

    @property
    def title(self):
        return f'stock item for {self.portfolio} , {self.stock}'

    def set_amount_stock_item(self, amount):
        self.amount_stock_item = amount

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
    deposit_amount = models.FloatField(null=True, blank=True, verbose_name=_('Deposit amount'))

    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Selling price'))
    withdraw_amount = models.FloatField(null=True, blank=True, verbose_name=_('Withdraw amount'))

    transaction_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Transaction date'))

    def __str__(self):
        return f'Transaction for {self.portfolio_stock_item} on {self.transaction_date}'

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
