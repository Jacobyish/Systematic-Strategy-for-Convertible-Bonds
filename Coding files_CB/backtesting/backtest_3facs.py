import pandas as pd
import backtrader as bt
import pyfolio as pf
import backtrader.analyzers as btanalyzers
import pyfolio.plotting as plotting

path = '/Users/jacobyi/Desktop/工作/东兴证劵/可转债/data/factor_cal/data_2018_2023_ic_weighted_120.csv'
df = pd.read_csv(path)
df['time'] = pd.to_datetime(df['time'])
df['factor'] = df['factor_3']


class BondData(bt.feeds.PandasData):
    lines = ('factor',)
    params = (
        ('datetime', 'time'),
        ('open', 'ths_close_daily_settle_bond'),
        ('high', 'ths_close_daily_settle_bond'),
        ('low', 'ths_close_daily_settle_bond'),
        ('close', 'ths_close_daily_settle_bond'),
        ('factor', 'factor')
    )


class BondStrategy(bt.Strategy):
    params = (
        ('rebalance_days', 10),
        ('num_bonds', 20)
    )

    def __init__(self):
        self.day_count = 0
        self.last_selected_datafeeds = []  # To store the last rebalance's bonds

    def log(self, txt, dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def prenext(self):
        self.next() # 不然会用上个bar的指标值

    def next(self):
        self.day_count += 1

        if self.day_count % self.params.rebalance_days == 0:

            # Only consider bonds with data for today
            bond_factors = [(data, data.factor[0]) for data in self.datas if data.datetime[0] == self.data.datetime[0]]

            bond_factors.sort(key=lambda x: x[1])

            # # Calculate the number of bonds constituting the bottom 10%
            # bottom_30_percent_count = round(len(bond_factors) * 0.06)
            #
            # # Select the bottom 30% bonds based on the factor
            # selected_bonds = bond_factors[:bottom_30_percent_count]
            selected_bonds = bond_factors[:self.params.num_bonds]
            selected_datafeeds = [data[0] for data in selected_bonds]

            # Sell bonds that were in the last list but not in the new list
            for data in self.last_selected_datafeeds:
                if data not in selected_datafeeds:
                    # self.log('SELL ORDER CREATED for: %s' % data._name)
                    self.close(data)

            # For bonds that are newly entered or remained, adjust the position.
            for data in selected_datafeeds:
                if data not in self.last_selected_datafeeds:
                    # self.log(f'BUY ORDER CREATED for: {data._name}, {bt.num2date(data.datetime[0])}')
                    self.order_target_percent(data, target=1.0 / self.params.num_bonds)
                else:
                    # self.log('ADJUST ORDER CREATED for: %s' % data._name)
                    self.order_target_percent(data, target=1.0 / self.params.num_bonds)

            # Update the last_selected_datafeeds
            self.last_selected_datafeeds = selected_datafeeds


# run the backtest
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Load each bond as a separate data feed
    # for thscode in df['thscode'].unique()[:30]:
    data1 = None
    for thscode in df.sort_values(by='time')['thscode'].unique():
        data_subset = df[df['thscode'] == thscode]
        datafeed = BondData(dataname=data_subset)
        cerebro.adddata(datafeed, name=thscode)
        data1 = datafeed
        data1.plotinfo.plot=False

    cerebro.addstrategy(BondStrategy)

    cerebro.broker.set_cash(100000)
    # Print out starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # cerebro.broker.setcommission(commission=0.002)  # 0.2%
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade_analysis')

    cerebro.addanalyzer(bt.analyzers.PyFolio)
    # Run the backtest
    results = cerebro.run()
    strat = results[0]

    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    # 加入中转债指数作为benchmark
    dfh = pd.read_csv('中证转债_2018_2023.csv')
    dfh['time'] = pd.to_datetime(dfh['time'])
    dfh = dfh[dfh['time'] > '2018-12-25']
    dfh = dfh[['time', 'close']]
    dfh.set_index('time', inplace=True)

    dfh['close_shift'] = dfh['close'].shift(1)
    dfh = dfh.fillna(method='bfill')  # Backward fill
    dfh['changeval'] = dfh['close'] - dfh['close_shift']
    dfh['change'] = dfh['changeval'] / dfh['close_shift']
    dfh = dfh.round({'change': 6})
    benchmark_rets = dfh['change'].tz_localize('UTC')
    benchmark_rets.name = 'CSI'

    # generate pyfolio results
    pf.create_full_tear_sheet(
        returns,
        positions=positions,
        transactions=transactions,
        benchmark_rets=benchmark_rets,
        live_start_date = '2023-07-01',
        round_trips=True)

    # Print out final conditions
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()

# Performance Statistics
results_stat = plotting.show_perf_stats(returns, positions=positions, transactions=transactions)

# p_c ratio
p_c = strat.analyzers.trade_analysis.get_analysis().won.pnl.total/strat.analyzers.trade_analysis.get_analysis().lost.pnl.total

#win_rate
win_rate = strat.analyzers.trade_analysis.get_analysis().won.total/strat.analyzers.trade_analysis.get_analysis().total.closed


print('pc ratio', p_c)
print('win rate', win_rate)
print('win number', strat.analyzers.trade_analysis.get_analysis().won.total)
print('lost number', strat.analyzers.trade_analysis.get_analysis().lost.total)
results_stat