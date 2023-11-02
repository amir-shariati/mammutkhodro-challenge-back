from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .choices import StockSymbolChoices
from .models import (
    Stock, Portfolio, PortfolioStockItem, Transaction
)


class StockSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class PortfolioSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class PortfolioStockItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PortfolioStockItem
        fields = '__all__'


class TransactionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
