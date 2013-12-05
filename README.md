# Sharpefolio

Stock portfolio optimizer in Python based on least correlated moving sharpe / sortino ratios. 

## Wait, what?

The Sharpefolio engine can analyze thousands of stocks and suggests a portfolio of n stocks with the highest moving Sharpe/Sortino ratio and the least correlation between each stock. 

The ratios tell us whether a portfolio's returns are due to smart investment decisions or a result of excess risk. This measurement is very useful because although one portfolio can reap higher returns than its peers, it is only a good investment if those higher returns do not come with too much additional risk. The greater a portfolio's Sharpe/Sortino ratio, the better its risk-adjusted performance has been. 

However, one can't just simply pick the stocks with the highest individual ratios. The portfolio needs to balanced by picking the stocks that have the least correlation with each other to reduce the risk of negative macro-economic changes. A portfolio with stocks that have a high individual  ratio and a low correlation between each stock therefore has a high Sharpe/Sortino ratio overall. 

## What's a Sharpe/Sortino?

Sharpe and Sortino ratios have been invented to compare a portfolio's health with other portfolios. However, they can also be used "ex-ante" to estimate future prices.

http://en.wikipedia.org/wiki/Sharpe_ratio

http://en.wikipedia.org/wiki/Sortino_ratio

## LICENSE AND DISCLAIMER

Copyright (c) 2013, [Melvin Tercan](https://github.com/melvinmt), [Lorenzo Pisani](https://github.com/Zeelot)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
* Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
