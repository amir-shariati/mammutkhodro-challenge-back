import datetime
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, views, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, F, Max, Min
from utils.yahooFinance import Ticker
from .choices import (
    StockSymbolChoices,
    StockNameChoices,
    StockBuySellChoices,
)
from .models import (
    Stock, Portfolio, PortfolioStockItem, Transaction
)
from .serializers import (
    StockChoiceSerializer, StockHistorySerializer,
    StockSerializer, PortfolioSerializer, PortfolioStockItemSerializer, TransactionSerializer
)


@api_view(['GET'])
def get_stock_symbol_choices_view(request):
    serializer = StockChoiceSerializer(
        instance={
            "labels": StockSymbolChoices.labels,
            "values": StockSymbolChoices.values
        }
    )
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_stock_name_choices_view(request):
    serializer = StockChoiceSerializer(
        instance={
            "labels": StockNameChoices.labels,
            "values": StockNameChoices.values
        }
    )
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_stock_action_choices_view(request):
    serializer = StockChoiceSerializer(
        instance={
            "labels": StockBuySellChoices.labels,
            "values": StockBuySellChoices.values
        }
    )
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_stock_history_data_view(request):
    symbol = request.data.get('symbol')
    # start = request.data.get('start')
    start = datetime.datetime(2022, 10, 1)
    # end = request.data.get('end')
    end = datetime.datetime(2023, 10, 1)

    if symbol is None or symbol not in StockSymbolChoices.values:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'send correct symbol'})

    # if start is None or end is None:
    #     pass
    #
    # start = datetime.fromisoformat(start[:-1])
    # end = datetime.fromisoformat(end[:-1])

    ticker = Ticker(symbol)
    ticker_row_df = ticker.get_stock_history_date(start=start, end=end)
    ticker_values_dict = Ticker.df_to_dict(ticker_row_df)
    serializer = StockHistorySerializer(instance=ticker_values_dict, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def stock_item_add(request):
    stock_id = request.data.get('stock_id')
    portfolio_id = request.data.get('portfolio_id')

    try:
        stock = Stock.objects.get(pk=stock_id)
        portfolio = Portfolio.objects.get(pk=portfolio_id)
    except ObjectDoesNotExist:
        return Response(
            data={"error": 'ObjectDoesNotExist: stock_id, portfolio_id'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        queryset = PortfolioStockItem.objects.create(stock=stock, portfolio=portfolio)
        serializer = PortfolioStockItemSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response(
            data={"error": 'UNIQUE constraint failed: stock_id, portfolio_id'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def stock_item_buy(request):
    stock_item_id = request.data.get('stock_item_id')
    price = request.data.get('price')
    transaction_date = request.data.get('transaction_date')
    print('-------------------------------------')
    print(f'price: {price}')
    print(f'transaction_date: {transaction_date}')
    date = datetime.datetime.fromisoformat(transaction_date)
    print(f'date: {date}')

    if price is not None:
        price = float(price)

    try:
        stock_item = PortfolioStockItem.objects.get(pk=stock_item_id)
    except ObjectDoesNotExist:
        return Response(
            data={"error": 'ObjectDoesNotExist: PortfolioStockItem'},
            status=status.HTTP_400_BAD_REQUEST
        )
    transaction = stock_item.stock_buy(price=price, transaction_date=date)
    serializer = TransactionSerializer(transaction)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def stock_item_sell(request):
    stock_item_id = request.data.get('stock_item_id')
    amount = request.data.get('amount')
    transaction_date = request.data.get('transaction_date')
    print('-------------------------------------')
    print(f'amount: {amount}')
    print(f'transaction_date: {transaction_date}')
    date = datetime.datetime.fromisoformat(transaction_date)
    print(f'date: {date}')

    if amount is not None:
        amount = float(amount)

    try:
        stock_item = PortfolioStockItem.objects.get(pk=stock_item_id)
    except ObjectDoesNotExist:
        return Response(
            data={"error": 'ObjectDoesNotExist: PortfolioStockItem'},
            status=status.HTTP_400_BAD_REQUEST
        )
    transaction = stock_item.stock_sell(amount=amount, transaction_date=date)
    serializer = TransactionSerializer(transaction)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockRetrieveView(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class PortfolioListCreateView(generics.ListCreateAPIView):
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
