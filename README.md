# Pairs-algo

**Pairs-algo** is a sample trading algorithm that simulates a cointegrated pairs trading strategy using different commodity futures contracts. The strategy attempts to exploit mean-reverting behavior in the spread between these two energy products.

---

## 📦 Components

### 🔧 `TradingEngine`
A core class responsible for:
- Executing buy/sell/close trades
- Tracking account balance, position size, returns, and portfolio value
- Maintaining a trade log for backtesting analysis

---

## 📈 Strategies

### `strat_1`: Simple 1:1 Spread
- Trades the **raw price spread** between BZ and HO (equal 1-1 weighting).
- **Buy Signal:** When the spread drops 2 standard deviations below its long-term moving average.
- **Sell Signal:** When the spread rises 2 standard deviations above its long-term moving average.

### `strat_2`: Dollar-Neutral Spread
- Trades a **dollar-neutral** version of the spread by estimating a **hedge ratio** using OLS regression.
- **Buy Signal:** When the spread drops 2 standard deviations below its long-term moving average.
- **Sell Signal:** When the spread rises 2 standard deviations above its long-term moving average.

### `strat_3`: Dollar-Neutral Spread with risk controls
- Trades a **dollar-neutral** version of the spread by estimating a **hedge ratio** using OLS regression. The order size at each signal is dependent on a scalable risk factor, and the strength of the buy / sell signal
- **Buy Signal:** When the spread drops 2 standard deviations below its long-term moving average.
- **Sell Signal:** When the spread rises 2 standard deviations above its long-term moving average.
---

## 📝 Notes
- The system assumes sufficient liquidity for position entry/exit.
- Designed for backtesting; real-time trading would require significant extension (e.g., slippage, latency, order routing).
- Negative balances are configurable and can be disallowed.
- `strat_2`

### Improvement ideas for next strat
- Implement simple risk management methods (stop loss / take profit)
- Implement dynamic order quantities proportional to signal strength
