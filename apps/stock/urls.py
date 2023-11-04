from django.contrib import admin
from django.urls import path, include

from .views import (
    get_stock_symbol_choices_view, get_stock_name_choices_view, get_stock_action_choices_view,
    get_stock_history_data_view, stock_item_add, stock_item_buy, stock_item_sell,
    StockListView, StockRetrieveView,
    PortfolioListView, PortfolioRetrieveDestroyView,
    PortfolioStockItemListView, PortfolioStockItemRetrieveDestroyView,
    TransactionListView, TransactionRetrieveView,
)

urlpatterns = [
    path('stock-symbol/', get_stock_symbol_choices_view, name='stock-symbol'),
    path('stock-name/', get_stock_name_choices_view, name='stock-name'),
    path('stock-action/', get_stock_action_choices_view, name='stock-action'),

    path('stock/history/', get_stock_history_data_view, name='stock-history'),

    path('stock/', StockListView.as_view(), name='stock-list'),
    path('stock/<int:pk>', StockRetrieveView.as_view(), name='stock-detail'),

    path('portfolio/', PortfolioListView.as_view(), name='portfolio-list'),
    path('portfolio/<int:pk>', PortfolioRetrieveDestroyView.as_view(), name='portfolio-detail'),

    path('stock-item/add/', stock_item_add, name='stock-item-add'),
    path('stock-item/buy/', stock_item_buy, name='stock-item-buy'),
    path('stock-item/sell/', stock_item_sell, name='stock-item-sell'),

    path('stock-item/', PortfolioStockItemListView.as_view(), name='stock-item-list'),
    path('stock-item/<int:pk>', PortfolioStockItemRetrieveDestroyView.as_view(), name='stock-item-detail'),

    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>', TransactionRetrieveView.as_view(), name='transaction-detail'),
]
