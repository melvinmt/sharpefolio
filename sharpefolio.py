import numpy as np
import math
from numpy import recfromcsv
from itertools import combinations
import os

portfolio_size=10

# Get an array of file names in the current directory ending with csv
files = [fi for fi in os.listdir('data') if fi.endswith(".csv")]

symbols = [os.path.splitext(fi)[0] for fi in files]

# Load one file so we can find out how many days of data are in it.
for file in files:
    firstfile = recfromcsv("data/"+file)
    if len(firstfile) > 0:
        break

print "firstfile:", files[0]

datalength = len(firstfile['close'])

print "datalength:", datalength

# Creates a 'record array', which is like a spreadsheet with a header.
closes = np.recarray((datalength,), dtype=[(symbol, 'float') for symbol in symbols])

# Do the same for daily returns, except one row smaller than closes.
daily_ret = np.recarray((datalength-1,), dtype=[(symbol, 'float') for symbol in symbols])

# Initialize some arrays for storing data
average_returns = np.zeros(len(files))
return_stdev = np.zeros(len(files))
sharpe_ratios = np.zeros(len(files))
cumulative_returns = np.recarray((datalength,), dtype=[(symbol, 'float') for symbol in symbols])

for i, file in enumerate(files):
    # Read in the data from the file
    data = recfromcsv("data/"+file)
    ndata = np.copy(data)
    ndata.resize(datalength)
    data = np.atleast_1d(data)
    print file + ":", data
    if len(data) == 0:
        continue
    if(len(data) < datalength):
        for i in range(len(data), len(ndata)):
            ndata[i] = data[-1]

    # Read the 'close' column of the data and reverse the numbers
    closes[symbols[i]] = ndata['adj_close'][::-1]  

    print "closes:", closes[symbols[i]]

    if sum(closes[symbols[i]]) <= 0:
        print "skipping!"
        continue

    # Get the closing price for the symbol
    daily_ret[symbols[i]] = (closes[symbols[i]][1:]-closes[symbols[i]][:-1])/closes[symbols[i]][:-1]

    print "daily_ret:", daily_ret[symbols[i]]

    # Now that we have the daily returns in %, calculate the relevant stats.  
    average_returns[i] = np.mean(daily_ret[symbols[i]])
    return_stdev[i] = np.std(daily_ret[symbols[i]])
    if return_stdev[i] == 0:
        print "continue!"
        continue
    sharpe_ratio = (average_returns[i] / return_stdev[i]) * np.sqrt(datalength)
    if math.isnan(sharpe_ratio):
        print "continue!"
        continue
    sharpe_ratios[i] = sharpe_ratio
    


# Stocks are sorted by sharpe ratio, then the top n stocks are analysed for cross-correlation
# top_n_equities=int(len(sharpe_ratios)*0.17)
top_n_equities=20



# Sort the indexes of the sharpe_ratios array in order.
sorted_sharpe_indices = np.argsort(sharpe_ratios)[::-1][0:top_n_equities]
print "sorted_sharpe_indices", sorted_sharpe_indices

all_stocks = [symbols[i] for i in sorted_sharpe_indices]
print all_stocks

all_sharpe_ratios = [sharpe_ratios[i] for i in sorted_sharpe_indices]
sharpe_ratios = all_sharpe_ratios
print "sharpe_ratios:", sharpe_ratios[0:top_n_equities]
print all_sharpe_ratios

check_all_sharpe_ratios = []
check_all_stocks = []

for i, sharpe_ratio in enumerate(all_sharpe_ratios):
    if math.isnan(sharpe_ratio) == False:
        check_all_sharpe_ratios.append(sharpe_ratio)
        check_all_stocks.append(all_stocks[i])
print check_all_stocks
print check_all_sharpe_ratios

all_stocks = check_all_stocks
all_sharpe_ratios = check_all_sharpe_ratios

print "sorted_sharpe_indices", sorted_sharpe_indices

# Next we create a datastructure to hold the daily returns of the top n equities
cov_data = np.zeros((datalength-1, top_n_equities))

# Grab the daily returns for those stocks and put them in cov_data index (cov stands for
# covariate)
for i, symbol_index in enumerate(sorted_sharpe_indices):
    cov_data[:,i] = daily_ret[symbols[symbol_index]]

# Make a correlation matrix for the top n equities
cormat = np.corrcoef(cov_data.transpose())

# Create all possible combinations of the n top equites for the given portfolio size.  
portfolios = list(combinations(range(0, top_n_equities), portfolio_size))

# For each possible combination of the top n equities, add up all the correlations
# between the four instruments
total_corr = [sum([cormat[x[0]][x[1]] for x in combinations(p, 2)]) for p in portfolios]

# Find the portfolio with the smallest sum of correlations, and convert that back into 
# the instrument names via a lookup in the symbols array
best_portfolio=[symbols[sorted_sharpe_indices[i]] for i in portfolios[total_corr.index(np.nanmin(total_corr))]]
print("stocks:")
print(best_portfolio)

best_sharpe_ratios = [sharpe_ratios[sorted_sharpe_indices[i]] for i in portfolios[total_corr.index(np.nanmin(total_corr))]]
print("sharpe ratios:")
print(best_sharpe_ratios)

allocation = [best_sharpe_ratios/sum(best_sharpe_ratios)]
print("allocation:")
print(allocation)
