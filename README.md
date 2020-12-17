## Introduction 
MetaTrader is a very powerful and useful tool. Most of programmers interested in developing investment robots have problems because it require to learn Mql programming language in order to implement trade strategies. This repository contains two scripts, first one is a server written in MQL5, and the second one is a python script containing multiple classes that works like an interface between your python trade strategy and MetaTrader.

## Setup
Install PyZMQ throught <i>pip install zmq</i> and copy the files in lib folder to your MataTrader directory. In MetaEditor you should compile <i>zmq_server.mq5</i> and attach the expert advisor in a chart, check the box ". Also important to mention, you should allow it to import all DLL's, allow Algo Trading and Allow Modification of Signals Setting. Also it's important to change the SERVER variable inside mt5_tools.py to your localhost ip, or the ip were the server is running. 

## using it

<b>mt5_currentprice</b><br>
it receive the Symbol ( or ticker) as a parameter, and it returns a list with the bid price and ask price. For example
```python

price = mt5_currentprice('MGLU3')
bid_price = price[0]
ask_price = price[1]
```


<b>mt5_historicaldata</b><br>
first creat a file called <i>symbols.csv</i> and write all symbols you wanna get data from. The class receives <i>timeframe</i> (for more details check the zmq_server.mq5), <i>start_datetime</i> and <i>end_datetime</i> it sets the time interval for the data, for example :

<i>symbols.csv</i>
```text
MGLU3
AZUL4
ITUB4
```
```python
data = mt5_historicaldata('5', '2020.10.1', '2020.10.5')

MGLU3_close = data['MGLU3']['close']
```

<b>opening and closing positions<\b>

To open a long position you can use the class mt5_buy, it receives the symbol, stoploss, takeprofit and volume. If you dont want to set a stoploss or stopgain you can just set as 0. 
```python

order = mt5_buy('MGLU3', 0, 0, 500)

```

<i>order</i> will get a list containing the <i>ticket, price and volume</i> you need to save the ticket because it's necessary to close the position.

```python

ticket_code = order[0]

```

Now to close this position you just need to call mt5_close, and pass the ticket as parameter. the mt5_close class will return the status, price and volume.

```python

ret = mt5_close(ticket_code)
print('position closed at ${}'.format(ret[1]))


```
