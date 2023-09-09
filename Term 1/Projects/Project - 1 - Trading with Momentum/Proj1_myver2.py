import sys 

import pandas as pd
import numpy as np
import helper
import project_helper
import project_tests

df = pd.read_csv('eod-quotemedia.csv', parse_dates=['date'], index_col=False)
close = df.reset_index().pivot(index='date', columns='ticker', values='adj_close')
print('Loaded Data')
print(close.head(5))

apple_ticker = 'AAPL'
project_helper.plot_stock(close[apple_ticker], '{} Stock'.format(apple_ticker))
def resample_prices(close_prices, freq='M'):
    """
    Resample close prices for each ticker at specified frequency.
    
    Parameters
    ----------
    close_prices : DataFrame
        Close prices for each ticker and date
    freq : str
        What frequency to sample at
        For valid freq choices, see http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    
    Returns
    -------
    prices_resampled : DataFrame
        Resampled prices for each ticker and date
    """
    # TODO: Implement Function
    # <DataFrame or Series>.resample(arguments).<aggregate function>
    resampled_close_prices = close_prices.resample(freq).last()
    
    return resampled_close_prices

project_tests.test_resample_prices(resample_prices)


monthly_close = resample_prices(close)
# print(type(monthly_close))
# project_helper.plot_resampled_prices(
#     monthly_close.loc[:, apple_ticker],
#     close.loc[:, apple_ticker],
#     '{} Stock - Close Vs Monthly Close'.format(apple_ticker))


def compute_log_returns(prices):
    """
    Compute log returns for each ticker.
    
    Parameters
    ----------
    prices : DataFrame
        Prices for each ticker and date
    
    Returns
    -------
    log_returns : DataFrame
        Log returns for each ticker and date
    """
    # TODO: Implement Function

    print(prices)
    print(prices.shift(-1))
    log_return = np.log(prices)-np.log(prices.shift(1))
    
    return log_return

project_tests.test_compute_log_returns(compute_log_returns)


# monthly_close_returns = compute_log_returns(monthly_close)
# project_helper.plot_returns(
#     monthly_close_returns.loc[:, apple_ticker],
#     'Log Returns of {} Stock (Monthly)'.format(apple_ticker))

def get_top_n(prev_returns, top_n):
    """
    Select the top performing stocks
    
    Parameters
    ----------
    prev_returns : DataFrame
        Previous shifted returns for each ticker and date
    top_n : int
        The number of top performing stocks to get
    
    Returns
    -------
    top_stocks : DataFrame
        Top stocks for each ticker and date marked with a 1
    """
    # TODO: Implement Function
    top_stocks_df = pd.DataFrame(0, index=prev_returns.index, columns=prev_returns.columns)
    
    print(top_stocks_df.head())
    
    for idx, row in prev_returns.iterrows():
        top_stock_idxs = list(row.nlargest(top_n).index)
        # loc for lables and iloc for integer
        top_stocks_df.loc[idx][top_stock_idxs]=1
        
    print(top_stocks_df)
    return top_stocks_df

project_tests.test_get_top_n(get_top_n)

def portfolio_returns(df_long, df_short, lookahead_returns, n_stocks):
    """
    Compute expected returns for the portfolio, assuming equal investment in each long/short stock.
    
    Parameters
    ----------
    df_long : DataFrame
        Top stocks for each ticker and date marked with a 1
    df_short : DataFrame
        Bottom stocks for each ticker and date marked with a 1
    lookahead_returns : DataFrame
        Lookahead returns for each ticker and date
    n_stocks: int
        The number number of stocks chosen for each month
    
    Returns
    -------
    portfolio_returns : DataFrame
        Expected portfolio returns for each ticker and date
    """
    # TODO: Implement Function
    long_position = df_long * lookahead_returns
    short_position = df_short * lookahead_returns
    
    portfolio_returns = long_position - short_position
    
    return portfolio_returns/n_stocks

project_tests.test_portfolio_returns(portfolio_returns)

expected_portfolio_returns = portfolio_returns(df_long, df_short, lookahead_returns, 2*top_bottom_n)
project_helper.plot_returns(expected_portfolio_returns.T.sum(), 'Portfolio Returns') 