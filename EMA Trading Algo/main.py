from AlgorithmImports import *

class EMACrossoverRSIAlgorithm(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetCash(10000)

        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.ema_fast = self.EMA(self.symbol, 10, Resolution.Daily)
        self.ema_slow = self.EMA(self.symbol, 30, Resolution.Daily)
        self.rsi = self.RSI(self.symbol, 14, MovingAverageType.Wilders, Resolution.Daily)

        self.SetWarmUp(30)
        
        self.previous_action = None

    def OnData(self, data):
        if not self.IsWarmingUp and data.ContainsKey(self.symbol):
            holdings = self.Portfolio[self.symbol].Quantity
            ema_fast_current = self.ema_fast.Current.Value
            ema_slow_current = self.ema_slow.Current.Value
            rsi_current = self.rsi.Current.Value

            if ema_fast_current > ema_slow_current and rsi_current < 30:
                if holdings <= 0:
                    self.SetHoldings(self.symbol, 1.0)
                    self.previous_action = "buy"
            elif ema_fast_current < ema_slow_current and rsi_current > 70:
                if holdings > 0:
                    self.SetHoldings(self.symbol, 0)
                    self.previous_action = "sell"
            else:
                self.previous_action = None
