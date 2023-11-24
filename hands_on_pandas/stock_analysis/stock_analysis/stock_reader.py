"""Gather select stock data."""

import datetime as dt
import re

import pandas as pd
import pandas_datareader.data as web

from .utils import label_sanitizer


class StockReader:
    """Class for reading financial data from websites."""
    
    _index_tickers = {'S&P 500': '^GSPC', 'Dow Jones': '^DJI', 'NASDAQ': '^IXIC'}
    
    def __init__(self, start, end=None):
        """
        Create a `StockReader` object for reading across a given date range.
        
        Parameters:
            - start: The first date to include, as a datetime object or a string in the
              format 'YYYYMMDD'.
            - end: The last date to include, as a datetime object or string in the
              format 'YYYYMMDD'.  Defaults to today if not provided.
        """
        self.start, self.end = map(
            lambda x: x.strftime('%Y%m%d') if isinstance(x, dt.date) else re.sub(r'\D', '', x), [start, end or dt.date.today()]
        )
        if self.start >= self.end:
            raise ValueError('`start` must be before `end`')
            
    @property
    def available_tickers(self):
        """Indices whose tickers are supported."""
        return list(self._index_tickers.keys())
    
    @classmethod
    def get_index_ticker(cls, index):
        """
        Get the ticker of the specified index, if known.
        
        Parameters:
            - index: The name of the index; check
              `available_tickers` for full list which includes:
                  - 'S&P 500' for S&P 500,
                  - 'Dow Jones' for Dow Jones Industrial Average,
                  - 'NASDAQ' for NASDAQ Composite Index
        
        Returns:
            The ticker as a string if known, otherwise `None`.
        """
        try:
            index = index.upper()
        except AttributeError:
            raise ValueError('`index` must be a string')
        return cls._index_tickers.get(index, None)