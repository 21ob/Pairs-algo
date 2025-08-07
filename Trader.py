import pandas as pd

class TradingEngine:
    """
    Simulates a basic trading engine with buy/sell functionality.

    Attributes:
        balance (float): Available funds.
        position (int): Current position (positive for long, negative for short).
        position_tracker (array): Tracks the portfolio position
        trade_count (int): Number of executed trades.
        portfolio_tracker (array): Track total portfolio value (balance + unrealized P/L).
        returns (array): Track returns.
    """

    def __init__(self, balance, position=0):
        self.balance = balance
        self.position = position
        self.position_tracker = []
        self.trade_count = 0
        self.portfolio_tracker = []
        self.returns = []
        
    
    def sell(self, price, quantity):
        """
        Executes a sell trade and updates balance and position.
    
        Args:
            price (float): Price of the asset.
            quantity (float): Quantity of the asset to sell.
        """

        self.balance -= price * quantity
        self.position += quantity
        self.trade_count += 1
        
    
    def buy(self, price, quantity):
        """
        Executes a buy trade and updates balance and position.
        
        Args:
            price (float): Price of the asset.
            quantity (float): Quantity of the asset to buy.
        """

        self.balance -= price * quantity
        self.position += quantity
        self.trade_count += 1
        
    
    def close_position(self, price):
        """
        Executes a buy or sell trade to completely close net position to zero.
        
        Args:
            price (float): Price of the asset.
        """        
        self.balance += self.position * price
        self.position = 0
        
    
    def run_strategy(
        self, 
        buy_signal, 
        sell_signal, 
        price, 
        close_price, 
        dates, 
        allow_negative_balance=True):
        """
        Iterates over signals and executes trades accordingly. Position exit based on mean reversion.
    
        Args:
            buy_signal (array-like): Boolean array signaling when (and how much) to buy. Quantity should be a positive number.
            sell_signal (array-like): Boolean or array signaling when (and how much) to sell. Quantity should be a negative number.
            price (array-like): Array of asset prices at each timestep.
            close_price (array-like): Price at which the position will be closed if crossed.
            timesteps (int): Number of iterations or data points.
            allow_negative_balance (boolean): Whether or not the traders balance is allowed to run below zero, default=True
            
        Returns:
            pd.Series of daily returns
        """
        timesteps = len(price)
        portfolio_prev = self.balance    # initial portfolio value

        for i in range(timesteps):
            if allow_negative_balance:
                if buy_signal[i]:
                    self.buy(price=price[i], quantity=buy_signal[i])
                    
                elif sell_signal[i]:
                    self.sell(price=price[i], quantity=sell_signal[i])
            
                elif (((self.position > 0) & (price[i] > close_price[i])) | ((self.position < 0) & (price[i] < close_price[i]))):
                    self.close_position(price[i])

            else:
                if self.balance == 0:
                    break
                elif buy_signal[i]:
                    self.buy(price=price[i], quantity=buy_signal[i])
                    
                elif sell_signal[i]:
                    self.sell(price=price[i], quantity=sell_signal[i])
            
                elif (((self.position > 0) & (price[i] > close_price[i])) | ((self.position < 0) & (price[i] < close_price[i]))):
                    self.close_position(price[i])


            # Track portfolio value and returns
            portfolio_value = self.balance + self.position * price[i]
            self.portfolio_tracker.append(portfolio_value)
            
            daily_return = (portfolio_value / portfolio_prev) - 1 if portfolio_prev != 0 else 0
            self.returns.append(daily_return)
            portfolio_prev = portfolio_value
            self.position_tracker.append(self.position)

        self.close_position(price[-1])  #Close any outstanding positions
        
        return pd.Series(self.returns, index=pd.to_datetime(dates))
