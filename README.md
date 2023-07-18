
# Mql5_python_broker

## Introduction

The "Mql5_python_broker" project aims to simplify the integration between MQL5 and Python by providing a broker-like interface. It allows you to send and receive data between MetaTrader (MQL5) and Python, enabling the development of custom trading strategies using Python's extensive libraries and capabilities.

## Setup

To set up the "Mql5_python_broker" project, follow these steps:

1. Install the PyZMQ library by running the following command:
   ```
   pip install zmq
   ```

2. Copy the files in the "lib" folder to your MetaTrader directory.

3. In the MetaEditor, compile the "zmq_server.mq5" file.

4. In the MetaTrader terminal, attach the expert advisor to a chart and check the box for "Allow DLL imports," "Allow Algo Trading," and "Allow modification of signals setting."

5. Inside the "mt5_tools.py" file, update the `SERVER` variable to your localhost IP or the IP where the server is running.

## Usage

The "Mql5_python_broker" project provides the following classes for interacting with MetaTrader from Python:

### `mt5_currentprice`

This class retrieves the bid and ask prices for a given symbol (or ticker). Here's an example of how to use it:

```python
price = mt5_currentprice('MGLU3')
bid_price = price[0]
ask_price = price[1]
```

### `mt5_historicaldata`

This class retrieves historical data for specified symbols within a given timeframe. First, create a file called "symbols.csv" and write all the symbols you want to fetch data for. Here's an example:

**symbols.csv**
```
MGLU3
AZUL4
ITUB4
```

Then, you can use the class as follows:

```python
data = mt5_historicaldata('5', '2020.10.1', '2020.10.5')

MGLU3_close = data['MGLU3']['close']
```

### Opening and Closing Positions

To open a long position, you can use the `mt5_buy` class, which requires the symbol, stop loss (sl), take profit (tp), and volume (vol). If you don't want to set a stop loss or take profit, you can pass 0. Here's an example:

```python
order = mt5_buy('MGLU3', 0, 0, 500)
```

The `order` variable will contain a list with the ticket, price, and volume. Make sure to save the ticket value because it will be necessary to close the position.

To close the position, call the `mt5_close` class and pass the ticket as a parameter. The `mt5_close` class will return the status, price, and volume. Here's an example:

```python
ret = mt5_close(ticket_code)
print('Position closed at ${}'.format(ret[1]))
```

## License

The "Mql5_python_broker" project is licensed under the [MIT License](LICENSE).

```
```

Please note that this is a general improvement based on the information provided. Feel free to modify it further to fit your specific project requirements.
