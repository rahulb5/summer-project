# summer-project
algorithmic trading platform
```
The program contains the following apps:
1.streak
2.main
3.backtest
4.deploy
5.indicators
```

```
streak is the main app having the settings.py file
```

```
main is a false app just to initialise the variable at the very start of the program
and serves as the homepage in the server. (can be used as the page to get to the actual
program)
```


```
backtest, accessed through get data on the homepage 

opens up with get data, where user can enter the conditions (explained how on the web page)
exception handled to take only acceptable input from the drop down or a numeric value.
The acceptable inputs can be changed by adding keys to the dictionary datapoints in backtest/main.py
in the main funcation. 

On submit, the program backtests on the data taken from the api feed in backtest/main function and 
displays results saved in an object of trade model (See model description for details)

details show the data stored in trade object in a tabular format

deploy deploys the strategy in a parallel thread and calls deployed function from deploy/deploy.py
running the entered condition on get data page on the data from the api in delpoyed function.

deploy details appear only when a strategy is deployed and displays the details of trading activity 
stored in results model of deploy app

truncate kills the deploy thread and truncates the data from results model.
```

```
indicators app was made to calculate on the go indicator values
```

```
if any error occurs, check if variables are being created or not or empty the migrations
```
