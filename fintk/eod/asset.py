# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:38:56 2022

@author: ilep
"""

import typing
import datetime
import pandas
import requests
from io import StringIO
import matplotlib.pyplot as plt



EOD_HISTORICAL_DATA_API_URL = "https://eodhistoricaldata.com/api"


def _format_date(dt: typing.Union[None, datetime.datetime]) -> typing.Union[None, str]:
    """
        Returns formatted date
    """
    return None if dt is None else dt.strftime("%Y-%m-%d")




class Inflation:
    pass


# def mean_price(eodhd, year=2022):
#     if not hasattr(eodhd, "s_close"):
#         return None
#     else:
#         s_close = getattr(eodhd, "s_close")
#         mean_price_asset = s_close.loc[s_close.index.year ==  year].mean()
#         return mean_price_asset



# https://github.com/EodHistoricalData/python-eodhistoricaldata/blob/master/eod_historical_data/data.py
class EODHistoricalData:
    
    def __init__(self, symbol: str, exchange: str, start_date=None, end_date=None):
        
        self.symbol = symbol
        self.exchange = exchange
        self.start_date = start_date
        self.end_date = end_date
        

    def get_data(self, API_KEY, DATA, override=False):
        
        
        data_folder =  DATA / 'EOD Historical data' / 'SYMBOL_EXCHANGE' / ('%s.%s' % (self.symbol, self.exchange))
    
        if not data_folder.exists():
            data_folder.mkdir(parents=True)
                    
        df_path = data_folder / 'eod_historical_data.xlsx'
        
        if df_path.exists() and not override:
            print("loaded from existing excel")
            df = pandas.read_excel(df_path, index_col=0, engine='openpyxl')
        else:
            symbol_exchange: str = f"{self.symbol}.{self.exchange}"
            endpoint: str = f"/eod/{symbol_exchange}"
            
            url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
    
            params: dict = {
                "api_token": API_KEY,
                "from": _format_date(self.start_date),
                "to": _format_date(self.end_date)
            }    
            
            r: requests.Response = requests.get(url, params=params)
            
            if r.status_code == requests.codes.ok:
                # NOTE engine='c' which is default does not support skip footer
                df: typing.Union[pandas.DataFrame, None] = pandas.read_csv(StringIO(r.text), engine='python', skipfooter=1, parse_dates=[0], index_col=0)
                df.to_excel(df_path)
            else:
                df = None
            
        # df['date_dt'] = pandas.to_datetime(df['date'])
        self.df = df
        
        try:
            self.s_close = df.Close
            self.s_adjusted_close = df.Adjusted_close
        except:
            pass
            
        return df


    def mean_close_price(self, year=2022):
        if not hasattr(self, "s_close"):
            return None
        else:
            s_close = getattr(self, "s_close")
            mean_price_asset = s_close.loc[s_close.index.year ==  year].mean()
            return mean_price_asset
    


# def get_dividends(symbol: str, exchange: str, start: typing.Union[str, int] = None, end: typing.Union[str, int] = None,
#                   api_key: str = EOD_HISTORICAL_DATA_API_KEY_DEFAULT,
#                   session: typing.Union[None, requests.Session] = None) -> typing.Union[pd.DataFrame, None]:
#     """
#         Returns dividends
#     """
#     symbol_exchange: str = f"{symbol},{exchange}"
#     session: requests.Session = _init_session(session)
#     start, end = _sanitize_dates(start, end)
#     endpoint: str = f"/div/{symbol_exchange}"
#     url: str = EOD_HISTORICAL_DATA_API_URL + endpoint
#     params: dict = {
#         "api_token": api_key,
#         "from": _format_date(start),
#         "to": _format_date(end)
#     }
#     r: requests.Response = session.get(url, params=params)
#     print(f'status code : {r.status_code}')

#     if r.status_code == requests.codes.ok:
#         # NOTE engine='c' which is default does not support skip footer
#         df: typing.Union[None, pd.DataFrame] = pd.read_csv(StringIO(r.text), engine='python', skipfooter=1,
#                                                            parse_dates=[0], index_col=0)
#         assert len(df.columns) == 1
#         ts = df["Dividends"]
#         return ts
#     elif r.status_code == api_key_not_authorized:
#         inv_api_key()
#     else:
#         params["api_token"] = "YOUR_HIDDEN_API"
#         raise RemoteDataError(r.status_code, r.reason, _url(url, params))



class Asset:
    
    @staticmethod
    def build_S(ISIN):
        pass

    
    def __init__(self, ISIN):
        
        # pandas TimeSeries, S[t]
        self.S = None
        self.currency = None
        
        # PER par annee
        # div yield
        # payout ratio
        # mean TRI
        
    def get_historical_data(self):
        pass
        
    
    def plot_nominal(self, t_i, t_f):
        pass
    
    def plot_real(self, t_i, t_f):
        pass
    
    
    
class ETF(Asset):
    
    def __init__(self, d_eod_fundamentals):  
        
        self.d_eod_fundamentals = d_eod_fundamentals
        try:
            self.d_top_10_holdings = d_eod_fundamentals['ETF_Data']['Top_10_Holdings']
            self.df_top_10_holdings = pandas.DataFrame(d_eod_fundamentals['ETF_Data']['Top_10_Holdings']).T
        except: 
            self.d_top_10_holdings = None
            self.df_top_10_holdings = None
                    
        self.S_top_10 = self._build_S_top_10()
        
        
    def pie_chart_top_10(self, figsize=(10,10)):
        
        # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        labels = ['%s (%s.%s)' % (v.get("Name"), v.get("Code"), v.get("Exchange")) for k,v in self.d_top_10_holdings.items()]
        
        
        # sizes = [15, 30, 45, 10]
        sizes =  [v['Assets_%'] for v in self.d_top_10_holdings.values()]
        
        labels = labels + ['Autre']
        sizes = sizes + [100-sum(sizes)]
        
        
        # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        explode = [0.1] * len(sizes)
        
        fig1, ax1 = plt.subplots(figsize=figsize)
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90, counterclock=False)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        plt.show()
        
    def plot_VS_top_10_compo(self):
        '''
        Plot comparatif de l ETF VS un basket des 10 premiers stocks/assets qui le composent
        '''
        pass

    def _get_corr_vs_top_10_compo(self):
        pass

    def _build_S_top_10(self):
        return None
    
    
    

class Stock(Asset):
    
    def __init__(self, d_eod_fundamentals):  
        
        self.d_eod_fundamentals = d_eod_fundamentals
        
        # dividend history + payment frequency
        # dividend growth and/or stability
        # div stability
        
        # inflation_resistant_score
        
        # df_yearly_recap
        # div
        # CA, + CA perc increase vs y-1
        # operating income
        # debt/asset | leverage ratio
        # payout_ratio
        # stock price
        # PER
        # net_income / total asset 
        # ==> ROIC
        
    
    
    def plot(self, t_i, t_f):
        pass
        



class Portfolio:
    pass



















        
        
        
        
        
