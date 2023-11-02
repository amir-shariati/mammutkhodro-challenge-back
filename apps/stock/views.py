from rest_framework import generics, views, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F, Max, Min
from .choices import (
    StockSymbolChoices,
    StockNameChoices,
    StockBuySellChoices,
)
from .models import (
    Stock, Portfolio, PortfolioStockItem, Transaction
)
from .serializers import (
    StockSerializer, PortfolioSerializer, PortfolioStockItemSerializer, TransactionSerializer
)


@api_view(['GET'])
def get_stock_symbol_choices_view(request):
    choices = StockSymbolChoices.choices
    labels = StockSymbolChoices.labels
    values = StockSymbolChoices.values
    return Response(
        data={
            # 'choices': choices,
            'labels': labels,
            'values': values,
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_stock_name_choices_view(request):
    choices = StockNameChoices.choices
    labels = StockNameChoices.labels
    values = StockNameChoices.values
    return Response(
        data={
            # 'choices': choices,
            'labels': labels,
            'values': values,
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_stock_action_choices_view(request):
    choices = StockBuySellChoices.choices
    labels = StockBuySellChoices.labels
    values = StockBuySellChoices.values
    return Response(
        data={
            # 'choices': choices,
            'labels': labels,
            'values': values,
        },
        status=status.HTTP_200_OK
    )


class StockListView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockRetrieveView(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class PortfolioListView(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class PortfolioRetrieveView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class PortfolioStockItemListView(generics.ListAPIView):
    queryset = PortfolioStockItem.objects.all()
    serializer_class = PortfolioStockItemSerializer


class PortfolioStockItemRetrieveView(generics.RetrieveAPIView):
    queryset = PortfolioStockItem.objects.all()
    serializer_class = PortfolioStockItemSerializer


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionRetrieveView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
