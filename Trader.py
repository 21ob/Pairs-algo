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
        trade_log (2d array): Tracks date, direction, price and quantity of all trades executed by strategy
    """

    def __init__(self, balance, position=0):
        self.balance = balance
        self.position = position
        self.position_tracker = []
        self.trade_count = 0
        self.portfolio_tracker = []
        self.returns = []
        self.trade_log = []

    
    def _log_trade(self, date, action, price, quantity):
        """Internal method to log each trade."""
        self.trade_log.append({
            "date": pd.to_datetime(date),
            "action": action,
            "price": price,
            "quantity": quantity,
            "position": self.position,
            "balance": self.balance
        })

    
    def sell(self, price, quantity, date):
        """
        Executes a sell trade and updates balance and position.
    
        Args:
            price (float): Price of the asset.
            quantity (float): Quantity of the asset to sell.
        """

        self.balance -= price * quantity
        self.position += quantity
        self.trade_count += 1
        self._log_trade(date, "SELL", price, quantity)
        
    
    def buy(self, price, quantity, date):
        """
        Executes a buy trade and updates balance and position.
        
        Args:
            price (float): Price of the asset.
            quantity (float): Quantity of the asset to buy.
        """

        self.balance -= price * quantity
        self.position += quantity
        self.trade_count += 1
        self._log_trade(date, "BUY", price, quantity)
        
    
    def close_position(self, price, date):
        """
        Executes a buy or sell trade to completely close net position to zero.
        
        Args:
            price (float): Price of the asset.
        """        
        self.balance += self.position * price
        self._log_trade(date, "CLOSE", price, self.position)
        self.position = 0

    
    def get_trade_log(self):
        """Returns the trade log as a pandas DataFrame."""
        return pd.DataFrame(self.trade_log)

        
    def run_strategy(
        self, 
        buy_signal, 
        sell_signal, 
        price, 
        close_price, 
        dates, 
        allow_negative_balance=False):
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
                    self.buy(price=price[i], quantity=buy_signal[i], date=dates[i])
                    
                elif sell_signal[i]:
                    self.sell(price=price[i], quantity=sell_signal[i], date=dates[i])
            
                elif (((self.position > 0) & (price[i] > close_price[i])) | ((self.position < 0) & (price[i] < close_price[i]))):
                    self.close_position(price[i], date=dates[i])

            else:
                if self.balance < 0:
                    self.close_position(price[i], dates[i])
                    return pd.Series(self.returns, index=pd.to_datetime(dates[:i]))
                elif buy_signal[i]:
                    self.buy(price=price[i], quantity=buy_signal[i], date=dates[i])
                    
                elif sell_signal[i]:
                    self.sell(price=price[i], quantity=sell_signal[i], date=dates[i])
            
                elif (((self.position > 0) & (price[i] > close_price[i])) | ((self.position < 0) & (price[i] < close_price[i]))):
                    self.close_position(price[i], date=dates[i])


            # Track portfolio value and returns
            portfolio_value = self.balance + self.position * price[i]
            self.portfolio_tracker.append(portfolio_value)
            
            daily_return = (portfolio_value / portfolio_prev) - 1 if portfolio_prev != 0 else 0
            self.returns.append(daily_return)
            portfolio_prev = portfolio_value
            self.position_tracker.append(self.position)

        # Final close
        self.close_position(price[-1], dates[-1])
        
        return pd.Series(self.returns, index=pd.to_datetime(dates))
