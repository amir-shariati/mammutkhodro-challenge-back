from django.db import models
from django.utils.translation import gettext_lazy as _


class StockNameChoices(models.TextChoices):
    # GOLD = "gold", _("Gold")
    # FOREX = "forex", _("handleFOREX USD")
    # BITCOIN = "bitcoin", _("Bitcoin USD")
    # ETHEREUM = "ethereum", _("Ethereum USD")
    GOLD = "gold", _("GOLD")
    FOREX = "forex", _("FOREX")
    BITCOIN = "bitcoin", _("BITCOIN")
    ETHEREUM = "ethereum", _("ETHEREUM")


class StockSymbolChoices(models.TextChoices):
    GOLD = "GC=F", _("GC=F")
    FOREX = "FOREX-USD", _("FOREX-USD")
    BITCOIN = "BTC-USD", _("BTC-USD")
    ETHEREUM = "ETH-USD", _("ETH-USD")


class StockBuySellChoices(models.TextChoices):
    NONE = "NONE", _("None")
    BUY = "BUY", _("Buy")
    SELL = "SELL", _("Sell")
