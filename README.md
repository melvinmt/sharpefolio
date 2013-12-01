# Sharpefolio

Stock picker algorithm based on least correlated historical Sharpe/Sortino ratios.

# Wait, what?

The Sharpefolio engine analyses thousands of US stocks and suggests a portfolio of n stocks with the highest Sharpe/Sortino ratio and the least correlation between each stock. 

The Sharpe ratio tells us whether a portfolio's returns are due to smart investment decisions or a result of excess risk. This measurement is very useful because although one portfolio can reap higher returns than its peers, it is only a good investment if those higher returns do not come with too much additional risk. The greater a portfolio's Sharpe/Sortino ratio, the better its risk-adjusted performance has been. 

However, one can't just simply pick the stocks with the highest individual Sharpe/Sortino ratio. The portfolio needs to balanced by picking the stocks that have the least correlation with each other to reduce the risk of negative macro-economic changes. A portfolio with stocks that have a high individual Sharpe/Sortino ratio and a low correlation between each stock therefore has a high Sharpe/Sortino ratio overall. 