import time
from datetime import datetime, timedelta
import backtrader as bt
from ccxtbt import CCXTBroker
from ccxtbt import CCXTStore
from pytz import timezone
import Telegram_Bot

class FixedSizeMoney_01(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0])
        else:
            size = position.size
        print( '01 = ',size )
        return size

class FixedSizeMoney_02(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0])
        else:
            size = position.size
        print( '02 = ',size )
        return size

class FixedSizeMoney_03(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0])
        else:
            size = position.size
        print( '03 = ',size )
        return size

class FixedSizeMoney_04(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0])
        else:
            size = position.size
        print( '04 = ',size )
        return size

class FixedSizeMoney_21(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0], 2)
        else:
            size = position.size
        print( '21 = ',size )
        return size

class FixedSizeMoney_22(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0], 2)
        else:
            size = position.size
        print( '22 = ',size )
        return size

class FixedSizeMoney_23(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0], 2)
        else:
            size = position.size
        print( '23 = ',size )
        return size

class FixedSizeMoney_4(bt.Sizer):

    params = (
        ('money', 80),
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = round(self.params.money / data.close[0], 4)
        else:
            size = position.size
        print( '4 = ', size )
        return size

class Graal(bt.Indicator):
    
    lines = ('value1', 'value2',  'value3',)
    params = (('period', None),)
    #plotinfo = {"subplot":True}

    def __init__(self):

        self.i = 0
        self.period = self.p.period

    def next(self):

        if self.i >= 2: 
            self.lines.value1[0] = self.data.close[0] - self.data.close[-2]
            if self.i >= (self.period + 1):
                sum_value1 = 0
                for idx in range(1-self.period, 1):
                    sum_value1 = sum_value1 + self.lines.value1[idx]
                self.lines.value2 [0] = sum_value1 / self.period 
            if self.i >= (self.period + 2):
                self.lines.value3[0] = self.lines.value2[0] - self.lines.value2[-1]
        self.i = self.i + 1

class StrategyBase(bt.Strategy):

    def __init__(self):

        self.order = None
        self.isLive = False

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статуса приходящих баров"""
        dataStatus = data._getstatusname(status)  # Получаем статус (только при LiveBars=True)
        print(dataStatus)  # Не можем вывести в лог, т.к. первый статус DELAYED получаем до первого бара (и его даты)
        self.isLive = dataStatus == 'LIVE'

    def notify_order(self, order):
        """Изменение статуса заявки"""
        if order.status in [order.Submitted, order.Accepted]:  # Если заявка не исполнена (отправлена брокеру или принята брокером)
            self.log(f'Order Status: {order.getstatusname()}. TransId={order.ref}')
            return  # то выходим, дальше не продолжаем

        if order.status in [order.Canceled]:  # Если заявка отменена
            self.log(f'Order Status: {order.getstatusname()}. TransId={order.ref}')
            return  # то выходим, дальше не продолжаем

        if order.status in [order.Completed]:  # Если заявка исполнена
            if order.isbuy():  # Заявка на покупку
                self.log(f'Bought @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():  # Заявка на продажу
                self.log(f'Sold @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
        elif order.status in [order.Margin, order.Rejected]:  # Нет средств, или заявка отклонена брокером
            self.log(f'Order Status: {order.getstatusname()}. TransId={order.ref}')
        self.order = None  # Этой заявки больше нет

    def notify_trade(self, trade):
        """Изменение статуса позиции"""
        if not trade.isclosed:  # Если позиция не закрыта
            return  # то статус позиции не изменился, выходим, дальше не продолжаем
        self.log(f'Trade Profit, Gross={trade.pnl:.2f}, NET={trade.pnlcomm:.2f}')

    def _notify(self, qorders=[], qtrades=[]):
        pass


class Strategy_ETH(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'ETH/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def log_telegram(self, txt):
        """Вывод строки с датой в телеграмм"""
        Telegram_Bot.send (txt) #отправлять сообщение в бота

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[0].close
        self.Graal = Graal( self.datas[0], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)
        #print('ETH')

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем


        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[0]._dataname:
                
                dt = bt.num2date(self.datas[0].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                #print (f'Position main = {self.getposition(data = self.datas[0])}') #, broker = broker
                
                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[0]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_ETH')
                                self.order = self.buy(data = self.datas[0])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_ETH')
                            position = self.getposition(data = self.datas[0])
                            self.order = self.sell(data = self.datas[0], size = position.size)

                    self.log_telegram(f'DataClose ETH = {self.DataClose[0]:.5f}')

                self.log(f'DataClose ETH = {self.DataClose[0]:.5f}')

class Strategy_BAT(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'BAT/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[1].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[1].close
        self.Graal = Graal( self.datas[1], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[1]._dataname:
                
                dt = bt.num2date(self.datas[1].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[1]):      
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_BAT')
                                self.order = self.buy(data = self.datas[1])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_BAT')
                            position = self.getposition(data = self.datas[1])
                            self.order = self.sell(data = self.datas[1], size = position.size)

                #self.log(f'DataClose BAT = {self.DataClose[0]:.5f}')

class Strategy_LUNA(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'LUNA/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[2].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[2].close
        self.Graal = Graal( self.datas[2], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

        self.order = None
        self.isLive = False

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[2]._dataname:
                
                dt = bt.num2date(self.datas[2].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[2]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_LUNA')
                                self.order = self.buy(data = self.datas[2])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_LUNA')
                            position = self.getposition(data = self.datas[2])
                            self.order = self.sell(data = self.datas[2], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_MATIC(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'MATIC/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[3].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[3].close
        self.Graal = Graal( self.datas[3], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[3]._dataname:
                
                dt = bt.num2date(self.datas[3].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[3]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_MATIC')
                                self.order = self.buy(data = self.datas[3])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_MATIC')
                            position = self.getposition(data = self.datas[3])
                            self.order = self.sell(data = self.datas[3], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_SOL(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'SOL/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[4].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[4].close
        self.Graal = Graal( self.datas[4], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[4]._dataname:
                
                dt = bt.num2date(self.datas[4].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[4]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_SOL')
                                self.order = self.buy(data = self.datas[4])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_SOL')
                            position = self.getposition(data = self.datas[4])
                            self.order = self.sell(data = self.datas[4], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_GALA(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'GALA/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[5].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[5].close
        self.Graal = Graal( self.datas[5], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[5]._dataname:
                
                dt = bt.num2date(self.datas[5].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[5]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_GALA')
                                self.order = self.buy(data = self.datas[5])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_GALA')
                            position = self.getposition(data = self.datas[5])
                            self.order = self.sell(data = self.datas[5], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_AVAX(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'AVAX/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[6].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[6].close
        self.Graal = Graal( self.datas[6], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[6]._dataname:
                
                dt = bt.num2date(self.datas[6].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[6]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_AVAX')
                                self.order = self.buy(data = self.datas[6])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_AVAX')
                            position = self.getposition(data = self.datas[6])
                            self.order = self.sell(data = self.datas[6], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_DOT(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'DOT/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[7].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[7].close
        self.Graal = Graal( self.datas[7], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[7]._dataname:
                
                dt = bt.num2date(self.datas[7].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[7]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_DOT')
                                self.order = self.buy(data = self.datas[7])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_DOT')
                            position = self.getposition(data = self.datas[7])
                            self.order = self.sell(data = self.datas[7], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_XRP(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'XRP/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[8].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[8].close
        self.Graal = Graal( self.datas[8], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)
        #print('XRP')

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0] == self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[8]._dataname:
                
                dt = bt.num2date(self.datas[8].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[8]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_XRP')
                                self.order = self.buy(data = self.datas[8])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_XRP')
                            position = self.getposition(data = self.datas[8])
                            self.order = self.sell(data = self.datas[8], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

class Strategy_NEAR(StrategyBase):
    params = (
        ('Period', 100),
        ('ticker_id', 'NEAR/USDT')
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[9].datetime[0], tz = timezone('Europe/Moscow')) if dt is None else dt # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        StrategyBase.__init__(self)
        self.DataClose = self.datas[9].close
        self.Graal = Graal( self.datas[9], period = 100)
        self.Trend  = bt.talib.SMA(self.DataClose, timeperiod=self.p.Period)
        self.CrossUp = bt.indicators.CrossUp( self.Graal.value3, 0.0 )
        self.CrossDown = bt.indicators.CrossDown( self.Graal.value2, 0.0)
        #print('XRP')

    def next(self):

        if not self.isLive:
            return

        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то выходим, дальше не продолжаем

        if self.datas[0].datetime[0] == self.datas[1].datetime[0] == self.datas[2].datetime[0] == self.datas[3].datetime[0] == self.datas[4].datetime[0] == self.datas[5].datetime[0] == self.datas[6].datetime[0] == self.datas[7].datetime[0] == self.datas[8].datetime[0]== self.datas[9].datetime[0]:
        
            if self.params.ticker_id==self.datas[9]._dataname:
                
                dt = bt.num2date(self.datas[9].datetime[0], tz = timezone('Europe/Moscow'))
                timezon = timezone('Europe/Moscow')
                timeOpen = timezon.localize(dt)  # Биржевое время открытия бара
                timeNextClose = timeOpen + timedelta(minutes=30*2)  # Биржевое время закрытия следующего бара
                timeMarketNow = datetime.now(timezon)  # Текущее биржевое время

                if self.isLive and timeNextClose > timeMarketNow: #

                    if not self.getposition(data = self.datas[9]):     
                        if self.DataClose[0] > self.Trend[0]:
                            if self.CrossUp==1.0:
                                print('Buy_NEAR')
                                self.order = self.buy(data = self.datas[9])
                    else:
                        if self.CrossDown==1.0:
                            print('Sell_NEAR')
                            position = self.getposition(data = self.datas[9])
                            self.order = self.sell(data = self.datas[9], size = position.size)

                #self.log(f'DataClose ADA = {self.DataClose[0]:.5f}')

if __name__ == '__main__':  # Точка входа при запуске этого скрипта

    BINANCE = {
    "key": "",
    "secret": ""
    }

    COIN_REFER = "USDT"

    cerebro = bt.Cerebro( tz = timezone('Europe/Moscow')) # quicknotify=True ,

    idx0 = cerebro.addstrategy(Strategy_ETH)
    cerebro.addsizer_byidx(idx0, FixedSizeMoney_4, money=65)

    idx1 = cerebro.addstrategy(Strategy_BAT)
    cerebro.addsizer_byidx(idx1, FixedSizeMoney_01, money=65)

    idx2 = cerebro.addstrategy(Strategy_LUNA)
    cerebro.addsizer_byidx(idx2, FixedSizeMoney_21, money=65)

    idx3 = cerebro.addstrategy(Strategy_MATIC)
    cerebro.addsizer_byidx(idx3, FixedSizeMoney_02, money=65)

    idx4 = cerebro.addstrategy(Strategy_SOL)
    cerebro.addsizer_byidx(idx4, FixedSizeMoney_22, money=65)

    idx5 = cerebro.addstrategy(Strategy_GALA)
    cerebro.addsizer_byidx(idx5, FixedSizeMoney_03, money=65)

    idx6 = cerebro.addstrategy(Strategy_AVAX)
    cerebro.addsizer_byidx(idx6, FixedSizeMoney_23, money=65)

    idx7 = cerebro.addstrategy(Strategy_DOT)
    cerebro.addsizer_byidx(idx7, FixedSizeMoney_23, money=65)

    idx8 = cerebro.addstrategy(Strategy_XRP)
    cerebro.addsizer_byidx(idx8, FixedSizeMoney_01, money=65)

    idx9 = cerebro.addstrategy(Strategy_NEAR)
    cerebro.addsizer_byidx(idx9, FixedSizeMoney_04, money=65)

    config = {'apiKey': BINANCE.get("key"),
            'secret': BINANCE.get("secret"),
            'enableRateLimit': True,
            'nonce': lambda: str(int(time.time() * 1000)),
            'adjustForTimeDifference': True, #добавил из за ошибки
            
        }
    store = CCXTStore(exchange='binance', currency=COIN_REFER, config=config,  retries=7, debug=False) #, debug=True 

    broker = CCXTBroker() 
    cerebro.setbroker(broker)


    data0 = store.getdata(dataname='ETH/USDT', name="ETHUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )  # , historical=True) , drop_newest=True, historical=True ,ohlcv_limit=10,
    
    data1 = store.getdata(dataname='BAT/USDT', name="BATUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )
    
    data2 = store.getdata(dataname='LUNA/USDT', name="LUNAUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )
    
    data3 = store.getdata(dataname='MATIC/USDT', name="MATICUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )
    
    data4 = store.getdata(dataname='SOL/USDT', name="SOLUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )
    
    data5 = store.getdata(dataname='GALA/USDT', name="GALAUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )
    
    data6 = store.getdata(dataname='AVAX/USDT', name="AVAXUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )

    data7 = store.getdata(dataname='DOT/USDT', name="DOTUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )

    data8 = store.getdata(dataname='XRP/USDT', name="XRPUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )

    data9 = store.getdata(dataname='NEAR/USDT', name="NEARUSDT", 
                        timeframe=bt.TimeFrame.Minutes, fromdate=datetime(2022, 3, 10, 0, 0),
                        compression=30 )
  
    cerebro.adddata(data0)
    cerebro.adddata(data1)
    cerebro.adddata(data2)
    cerebro.adddata(data3)
    cerebro.adddata(data4)
    cerebro.adddata(data5)
    cerebro.adddata(data6)
    cerebro.adddata(data7)
    cerebro.adddata(data8)
    cerebro.adddata(data9)

    cerebro.run()