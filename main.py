from requestModule import RequestModule
from queue import Queue
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


LONG_SMA = 20
SHORT_SMA = 9
SIGNAL = 9
GRAPH_LEN = 30

def isWeekend(datetime: datetime) -> bool:
    return datetime.weekday() >= 5

def isClose(datetime: datetime) -> bool:
    return datetime.hour < 9 or datetime.hour > 18

def ema(prices: list) -> float:
    alpha = 2 / (len(prices) + 1)
    ema = 0
    for i in range(len(prices)):
        if i == 0:
            ema = prices[0] * alpha
        else:
            ema = (ema - prices[i - 1]) * alpha + prices[i - 1]
    return ema

def avg(price):
    return sum(price) / len(price)

fig = plt.figure()
ax = plt.axes()
rm = RequestModule("https://api.example.com", "your_token", "your_stock_cd")
x = [0]
MACD_graph = [0]
signal_graph = [0]
price_graph = [0]
lma_graph = [0]
sma_graph = [0]
price_history = []
MACD_history = []
isBying = False

samsung_history = rm.get_history_price()

def animate(i):
    global x, MACD_graph, signal_graph, price_graph, lma_graph, sma_graph, price_history, MACD_history, isBying

    # price_history.append(rm.get_cur_price())
    price_history.append(samsung_history.pop())
    if len(price_history) >= LONG_SMA:
        lma = avg(price_history)
        sma = avg(price_history[LONG_SMA - SHORT_SMA:])
        macd = sma - lma
        MACD_history.append(macd)
        if len(MACD_history) >= SIGNAL:
            signal = ema(MACD_history)

            # 그래프
            x.append(x[-1] + 1)
            MACD_graph.append(macd)
            signal_graph.append(signal)
            price_graph.append(price_history[-1])
            lma_graph.append(lma)
            sma_graph.append(sma)
            x = x[-GRAPH_LEN:]
            MACD_graph = MACD_graph[-GRAPH_LEN:]
            signal_graph = signal_graph[-GRAPH_LEN:]
            price_graph = price_graph[-GRAPH_LEN:]
            lma_graph = lma_graph[-GRAPH_LEN:]
            sma_graph = sma_graph[-GRAPH_LEN:]

    
            if lma > sma and not isBying:
                isBying = True
                rm.buy_order(1)
                print('macd', macd)
                print('signal', signal)

                print('buy', price_history[-1])
                
            elif lma < sma and isBying:
                isBying = False
                rm.sell_order(1)
                print('macd', macd)
                print('signal', signal)
                print('sell', price_history[-1])
                print()
            
        price_history = price_history[-LONG_SMA:]
        MACD_history = MACD_history[-SIGNAL:]
        #  그래프 작성
        ax.clear()
        # plt.plot(x, MACD_graph, 'b', label = 'macd')
        # plt.plot(x, signal_graph, 'g--', label = 'signal')
        plt.plot(x, price_graph, color='black', linewidth=5)
        plt.plot(x, lma_graph, color='violet')
        plt.plot(x, sma_graph, color='red')




if __name__ == "__main__":
   animation = FuncAnimation(fig, animate, interval=1000)
   plt.plot(0, 1, label = 'macd')
   plt.plot(0, 1, label = 'signal')
   plt.show()