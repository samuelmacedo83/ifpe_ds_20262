import pandas as pd
import yfinance as yf

def download_data(
    tickers:str,
    multi_level_index:bool = False
) -> pd.DataFrame:
    
    """ 
    Downloads the data from yahoo finance.
    
    Args:
        tickers(str): The ticker.
        multi_level_index(bool): Remove/include row indexes.
    """

    result = yf.download(
        tickers = tickers,
        multi_level_index = multi_level_index
    ).reset_index()

    return result



