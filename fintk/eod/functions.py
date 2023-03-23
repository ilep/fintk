# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 17:58:52 2022

@author: ilepoutre
"""

import pandas
import requests
import json

def search(query_string, EOD_API_KEY):
    eod_url_search = f'https://eodhistoricaldata.com/api/search/{query_string}?api_token={EOD_API_KEY}'
    r = requests.get(eod_url_search)
    
    df_search = pandas.DataFrame(r.json())
    return df_search
    

def get_all_exchanges(API_KEY, DATA, override=False):
    
    xlsx_path = DATA / 'df_all_exchanges.xlsx'
    if xlsx_path.exists() and not override:
        print("from saved xlsx")
        df_all_exchanges = pandas.read_excel(xlsx_path, index_col=0, engine='openpyxl')
        
    else:
        print("from request")
        url_all_exchanges = r'https://eodhistoricaldata.com/api/exchanges-list/?api_token=%s&fmt=json' % API_KEY
        r = requests.get(url_all_exchanges)
    
        df_all_exchanges = pandas.DataFrame(r.json()) # same as https://eodhistoricaldata.com/financial-apis/list-supported-exchanges/
        df_all_exchanges.to_excel(xlsx_path)
        
        # df_all_exchanges.shape
        
    return df_all_exchanges



def get_exchange_symbol_list(exchange_code, API_KEY, DATA, override=False):
    
    exchange_folder =  DATA / 'Exchange_symbol_list' / ('%s' % exchange_code)
    
    if not exchange_folder.exists():
        exchange_folder.mkdir(parents=True)
    
    xlsx_path = exchange_folder / 'df_exchange_symbol_list.xlsx'
    
    if xlsx_path.exists() and not override:
        print("from saved xlsx")
        df_exchange_symbol_list= pandas.read_excel(xlsx_path, index_col=0, engine='openpyxl')
        
    else:
        url_exchange_symbol_list = r'https://eodhistoricaldata.com/api/exchange-symbol-list/%s?api_token=%s&fmt=json' % (exchange_code, API_KEY)
        r = requests.get(url_exchange_symbol_list)
        
        df_exchange_symbol_list = pandas.DataFrame(r.json())
        df_exchange_symbol_list.to_excel(xlsx_path)

    return df_exchange_symbol_list


def get_all_symbols(API_KEY, DATA, override=False):
    
    xlsx_path = DATA / 'df_all_symbols.xlsx'
    
    if xlsx_path.exists() and not override:
        print("from saved xlsx")
        df_all_symbols = pandas.read_excel(xlsx_path, index_col=0, engine='openpyxl')
        
    else:
        df_all_exchanges = get_all_exchanges(API_KEY, DATA)
        
        _l = []
        
        for exchange_code in df_all_exchanges.Code:
            print("=" * 50)
            print("exchange_code %s" % exchange_code)
            df_exchange_symbol_list = get_exchange_symbol_list(exchange_code, API_KEY, DATA, override)
            _l.append(df_exchange_symbol_list)
        
        # df_all_symbols = None
        df_all_symbols = pandas.concat(_l, axis=0)
        print("Saving to excel")
        df_all_symbols.to_excel(xlsx_path)
    
    
    return df_all_symbols




def from_isin_to_code(isin, API_KEY, currency=None):
    url_search = f'https://eodhistoricaldata.com/api/search/{isin}?api_token={API_KEY}'
    r = requests.get(url_search)
    df_search = pandas.DataFrame(r.json())
    
    # assert len(df_search) == 1
    if len(df_search) >= 1:
        if currency is not None and currency in df_search.Currency:
            df_search = df_search.loc[df_search.Currency==currency]
        else:
            if 'EUR' in df_search.Currency:
                df_search = df_search.loc[df_search.Currency=='EUR']
            elif 'USD' in df_search.Currency:
                df_search = df_search.loc[df_search.Currency=='USD']
            else:
                df_search = df_search.iloc[0]
            
    s_search = df_search.squeeze()
    exchange = s_search.get('Exchange')
    code = s_search.get('Code')
    
    return exchange, code


def from_code_to_isin():
    pass


def get_divs_from_SYMBOL_EXCHANGE(SYMBOL, EXCHANGE, API_KEY, DATA, override=False):

    divs_folder =  DATA / 'Divs' / 'SYMBOL_EXCHANGE' / ('%s.%s' % (SYMBOL,EXCHANGE))

    if not divs_folder.exists():
        divs_folder.mkdir(parents=True)
        
    json_path = divs_folder / 'divs.json'
    

    if json_path.exists() and not override:
        print("from saved json")
        with open(json_path, 'r') as f:
            r_json = json.load(f)

    else:
        try:
            url_divs = f'https://eodhistoricaldata.com/api/div/{SYMBOL}.{EXCHANGE}?fmt=json&api_token={API_KEY}'
            r = requests.get(url_divs)
            r_json = r.json()        
    
            with open(json_path, 'w') as f: 
                json.dump(r.json(), f)
        except:
            r_json = []
        
    return r_json



def get_divs_from_ISIN(ISIN, API_KEY, DATA, override=False):
    divs_folder =  DATA / 'Divs' / 'ISIN' / ('%s' % ISIN)

    if not divs_folder.exists():
        divs_folder.mkdir(parents=True)

    json_path = divs_folder / 'divs.json'
    
    if json_path.exists() and not override:
        print("from saved json")
        with open(json_path, 'r') as f:
            r_json = json.load(f)    

    else:    
        try:
            EXCHANGE, SYMBOL = from_isin_to_code(ISIN, API_KEY)
            url_divs = f'https://eodhistoricaldata.com/api/div/{SYMBOL}.{EXCHANGE}?fmt=json&api_token={API_KEY}'
            r = requests.get(url_divs)
            r_json = r.json()  
                    
            with open(json_path, 'w') as f: 
                json.dump(r.json(), f)
        except: 
            r_json = []
    
    return r_json


    


def get_fundamentals_from_SYMBOL_EXCHANGE(SYMBOL, EXCHANGE, API_KEY, DATA, override=False):
    fundamental_folder =  DATA / 'Fundamentals' / 'SYMBOL_EXCHANGE' / ('%s.%s' % (SYMBOL,EXCHANGE))
        
    json_path = fundamental_folder / 'fundamentals.json'

    if json_path.exists() and not override:
        print("from saved json")
        with open(json_path, 'r') as f:
            r_json = json.load(f)

    else:
        url_fundamentals = f'https://eodhistoricaldata.com/api/fundamentals/{SYMBOL}.{EXCHANGE}?api_token={API_KEY}'
        
        try:
            r = requests.get(url_fundamentals)
            r_json = r.json()
        except: 
            print("Problem: %s" % str(r.content))
            r_json = None
        else:
            if not fundamental_folder.exists():
                fundamental_folder.mkdir(parents=True)
                
            with open(json_path, 'w') as f: 
                json.dump(r.json(), f)
            
    return r_json




def get_fundamentals_from_ISIN(ISIN, API_KEY, DATA, override=False):

    fundamental_folder =  DATA / 'Fundamentals' / 'ISIN' / ('%s' % ISIN)

    if not fundamental_folder.exists():
        fundamental_folder.mkdir()

    json_path = fundamental_folder / 'fundamentals.json'
    
    if json_path.exists() and not override:
        print("from saved json")
        with open(json_path, 'r') as f:
            r_json = json.load(f)
        
    else:    
        exchange, code = from_isin_to_code(ISIN, API_KEY)
        url_fundamentals = f'https://eodhistoricaldata.com/api/fundamentals/{code}.{exchange}?api_token={API_KEY}'
        
        r = requests.get(url_fundamentals)
        r_json = r.json()
        
        with open(json_path, 'w') as f: 
            json.dump(r.json(), f)
        
    return r_json



def get_asset_price(ISIN, API_KEY, DATA, override=False):
    
    date_from = None
    date_to = None
    
    str_from = None
    str_to = None

    data_folder =  DATA / 'EOD Historical data' / 'SYMBOL_EXCHANGE' / ('%s.%s' % (self.symbol, self.exchange))
    if not data_folder.exists():
        data_folder.mkdir(parents=True)
    
    df_path = data_folder / 'eod_historical_data.xlsx'
    
    if df_path.exists() and not override:
        print("loaded from existing excel")
        df = pandas.read_excel(df_path, index_col=0, engine='openpyxl')
    else:
        url = r'https://eodhistoricaldata.com/api/eod/%s.%s?period=d&fmt=json&api_token=%s' % (ticker_code, exchange_code, API_KEY)
        r = requests.get(url)
        
        df_eod = pandas.DataFrame(r.json())
    
        df_eod['date_dt'] = pandas.to_datetime(df_eod['date'])
    
        s_close = df_eod.loc[:,['date','close']].set_index('date')
        
        return s_close, df_eod









    