# Sharpefolio

Stock picker algorithm based on least correlated historical Sharpe/Sortino ratios.

## Wait, what?

The Sharpefolio engine can analyze thousands of US stocks and suggests a portfolio of n stocks with the highest Sharpe/Sortino ratio and the least correlation between each stock. 

The ratios tell us whether a portfolio's returns are due to smart investment decisions or a result of excess risk. This measurement is very useful because although one portfolio can reap higher returns than its peers, it is only a good investment if those higher returns do not come with too much additional risk. The greater a portfolio's Sharpe/Sortino ratio, the better its risk-adjusted performance has been. 

However, one can't just simply pick the stocks with the highest individual ratios. The portfolio needs to balanced by picking the stocks that have the least correlation with each other to reduce the risk of negative macro-economic changes. A portfolio with stocks that have a high individual  ratio and a low correlation between each stock therefore has a high Sharpe/Sortino ratio overall. 

## What's a Sharpe/Sortino?

Sharpe and Sortino ratios have been invented to compare a portfolio's health with other portfolios. However, they can also be used "ex-ante" to estimate future prices.

http://en.wikipedia.org/wiki/Sharpe_ratio

http://en.wikipedia.org/wiki/Sortino_ratio
