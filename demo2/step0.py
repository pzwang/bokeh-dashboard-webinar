"Create random stock prices, and some stats on those prices"

from numpy import asarray, cumprod, convolve, exp, ones
from numpy.random import lognormal, gamma, uniform

last_average = 100 
mean = 0
stddev = 0.04

def _create_prices(t):
    global last_average
    returns = asarray(lognormal(mean, stddev, 1))
    average =  last_average * cumprod(returns)
    last_average = average

    high = average * exp(abs(gamma(1, 0.03, size=1)))
    low = average / exp(abs(gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * uniform(0.05, 0.95, size=1)
    close = low + delta * uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0], average[0]

if __name__ == "__main__":
    for i in range(10):
        print _create_prices(i)


