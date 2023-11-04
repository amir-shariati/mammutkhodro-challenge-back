from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from .choices import StockSymbolChoices
from .models import (
    Stock, Portfolio, PortfolioStockItem, Transaction
)


class StockChoiceSerializer(serializers.Serializer):
    labels = serializers.ListSerializer(child=serializers.CharField(), read_only=True)
    values = serializers.ListSerializer(child=serializers.CharField(), read_only=True)


class StockHistorySerializer(serializers.Serializer):
    Open = serializers.FloatField(read_only=True)
    High = serializers.FloatField(read_only=True)
    Low = serializers.FloatField(read_only=True)
    Close = serializers.FloatField(read_only=True)
    Volume = serializers.FloatField(read_only=True)
    Dividends = serializers.FloatField(read_only=True)
    Stock_Splits = serializers.FloatField(read_only=True, label='Stock Splits')


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
