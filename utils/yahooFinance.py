"""
import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info
msft.info

# get historical market data
hist = msft.history(period="1mo")

# show meta information about the history (requires history() to be called first)
msft.history_metadata

# show actions (dividends, splits, capital gains)
msft.actions
msft.dividends
msft.splits
msft.capital_gains  # only for mutual funds & etfs

# show share count
msft.get_shares_full(start="2022-01-01", end=None)

# show financials:
# - income statement
msft.income_stmt
msft.quarterly_income_stmt
# - balance sheet
msft.balance_sheet
msft.quarterly_balance_sheet
# - cash flow statement
msft.cashflow
msft.quarterly_cashflow
# see `Ticker.get_income_stmt()` for more options

# show holders
msft.major_holders
msft.institutional_holders
msft.mutualfund_holders

# Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
# Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
msft.earnings_dates

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
msft.isin

# show options expirations
msft.options

# show news
msft.news

# get option chain for specific expiration
opt = msft.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts
"""

import datetime
import pandas as pd
import yfinance as yf


class Ticker:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker.upper())

    # get all stock info
    def get_stock_info(self) -> dict:
        return self.ticker.info

    # get historical market data
    def get_stock_history_period(self, period="1mo") -> pd.DataFrame:
        """
        :Parameters:
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
        """
        return self.ticker.history(period=period)

    # get historical market data
    def get_stock_history_interval(self, interval="1d") -> pd.DataFrame:
        """
        :Parameters:
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
        """
        return self.ticker.history(interval=interval)

    # get historical market data
    def get_stock_history_date(self, start: datetime.datetime = None, end: datetime.datetime = None) -> pd.DataFrame:
        """
        :Parameters:
            start: str
                Download start date string (YYYY-MM-DD) or _datetime, inclusive.
                Default is 99 years ago
                E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
            end: str
                Download end date string (YYYY-MM-DD) or _datetime, exclusive.
                Default is now
                E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
        """
        return self.ticker.history(start=start, end=end if end is not None else start + datetime.timedelta(days=1))

    @staticmethod
    def df_to_dict(df=None) -> dict:
        if df is None:
            return None
        else:
            return df.to_dict(orient='records')

    @staticmethod
    def get_row_values(row=None) -> dict:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0] if len(temp) > 0 else None

    @staticmethod
    def get_row_index(row=None) -> datetime:
        if row is None:
            return None
        else:
            temp = row.index.to_pydatetime()
            return temp[0] if len(temp) > 0 else None

    @staticmethod
    def get_row_close_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['Close'] if len(temp) > 0 else None

    @staticmethod
    def get_row_open_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['Open'] if len(temp) > 0 else None

    @staticmethod
    def get_row_high_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['High'] if len(temp) > 0 else None

    @staticmethod
    def get_row_low_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['Low'] if len(temp) > 0 else None

    @staticmethod
    def get_row_volume_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['Volume'] if len(temp) > 0 else None

    @staticmethod
    def get_row_dividends_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['Dividends'] if len(temp) > 0 else None

    @staticmethod
    def get_row_stock_splits_value(row=None) -> float:
        if row is None:
            return None
        else:
            temp = row.to_dict(orient='records')
            return temp[0]['Stock Splits'] if len(temp) > 0 else None
