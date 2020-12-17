"""
Created on Wed Nov  4 18:47:01 2020

@author: jeremias junior
@coauthor: gabriel cordeiro
"""

import zmq
import pandas as pd
import datetime


SERVER = 'tcp://25.21.110.40:10000' 


log_dict = dict()

def openLog(_type, _price, _volume, _symbol):
    
    ticket_dict = {'symbol':_symbol,
                   'type':_type,
                   'status':'open',
                   'time':[str(datetime.datetime.now()), None],
                   'price':[_price, None],
                   'volume':_volume,
                   'lucro':None
                   }
    
    return ticket_dict

def closeLog(_ticket, _price):
    
    
    log_dict[str(_ticket)]['status'] = 'close'
    log_dict[str(_ticket)]['time'][1] = str(datetime.datetime.now())
    log_dict[str(_ticket)]['price'][1] = _price
    
    if log_dict[_ticket]['type'] == 'long':
        log_dict[str(_ticket)]['lucro'] = (float(log_dict[str(_ticket)]['price'][1]) - float(log_dict[str(_ticket)]['price'][0]))
    if log_dict[_ticket]['type'] == 'short':
        log_dict[str(_ticket)]['lucro'] = (float(log_dict[str(_ticket)]['price'][0]) - float(log_dict[str(_ticket)]['price'][1]))
    
    return True
    
    
def savelog(_dict, name='log.json'):
    df = pd.DataFrame(_dict)
    df.to_json(name)


class mt5_currentprice:
    
    '''
    ticker :
        
        ticker da ação que tu quer pegar o bid, ask.
    
    exemplo:
    mt5_buy('LTCUSD', 0, 0, 5) -> compra 5 ltc
        retorna um codigo por exemplo 4567
    mt5_close('4567')
        fecha a posição.
    '''
    
    def __new__(self,
                ticker,
                ):
        
        context = zmq.Context()
        reqSocket = context.socket(zmq.REQ)
        connect = reqSocket.connect(SERVER)
        
        flag = str('RATES|'+ticker)
        
        
        try:
            reqSocket.send_string(flag)
            data = reqSocket.recv_string()
        except zmq.Again as e:
            print('waiting MT5...')
        
        
        trash_, bid_, ask_ =  data.strip('\n').split(',')
        
        #bid é o preco da venda 
        #ask é o preco da compra
        
        ret_ = [float(bid_), float(ask_)]
        
        return ret_


class mt5_historicaldata:
    
    '''
         
    start_datetime :
        ex:'2020.10.01' : pega dados a partir de 2020.10.01 excluindo 
                          2020.10.01
    idem para end_datetime
    
    server : O ip do servidor que ta ligado no MT5
    
    csv_list : Arquivo contendo os tickers que você quer pegar os dados historicos
    
    '''
    
    def __new__(self,
                 timeframe,
                 start_datetime,
                 end_datetime,
                 csv_list = 'symbols.csv'
                 ):
        
        context = zmq.Context()
        reqSocket = context.socket(zmq.REQ)
        
        
        
        connect = reqSocket.connect(SERVER)
        
        ticker_list = list()
        file = open(csv_list, 'r')
        
        for i in file.readlines():
            
            ticker_list.append(i.strip('\n'))
            file.close()

           
        
        symbol__ = dict({'date':[],
                         'open':[],
                         'low':[],
                         'high':[],
                         'close':[],
                         'volume1':[],
                         'volume2':[]})
             
        symbol_data = dict()
        
                
        for t in ticker_list:
            
            print(t)         
            
            
            symbol_data[t]={'date':[],
                            'open':[],
                            'low':[],
                            'high':[],
                            'close':[],
                            'volume1':[],
                            'volume2':[]}
        
            
             
            flag = str("DATA|"+str(t)+"|"+str(timeframe)+"|"+str(start_datetime)+" [00:00:00]|"+str(end_datetime)+" [00:00:00]")             
                       
            
            try:
                reqSocket.send_string(flag)
                data = reqSocket.recv_string()
            except zmq.Again as e:
                print("waiting MT5...")
             
            data = str(data).split('|')
            data.reverse()
            del data[-1]

            for i in data:
                
                symbol_data[t]['date'].append(i.split(',')[0])
                symbol_data[t]['open'].append(float(i.split(',')[1]))
                symbol_data[t]['low'].append(float(i.split(',')[2]))
                symbol_data[t]['high'].append(float(i.split(',')[3]))
                symbol_data[t]['close'].append(float(i.split(',')[4]))
                symbol_data[t]['volume1'].append(float(i.split(',')[5]))
                symbol_data[t]['volume2'].append(float(i.split(',')[6]))
            
            symbol_data[t] = pd.DataFrame(symbol_data[t])
                
        return symbol_data


class mt5_buy:
    
    def __new__(self, symbol, sl, tp, vol):
    
        #TRADE|TYPE|SYMBOL|STOPLOSS|STOPGAIN|VOLUME
        flag = str('OPEN|'+'1'+'|'+str(symbol)+'|'+str(sl)+'|'+str(tp)+'|'+str(vol))
        context = zmq.Context()
        reqSocket = context.socket(zmq.REQ)
        
        
        connect = reqSocket.connect(SERVER)
        
        try:
            reqSocket.send_string(flag)
            msg = reqSocket.recv_string()
        except zmq.Again as e:
            print('Waiting for Push MT5...')
        
        
        ticket__, price__, bid__, ask__, volume__ = msg.split(',')
        
        ret__ = [int(ticket__), float(price__), float(volume__)]
        
        log_dict[str(ticket__)] = openLog('long', float(price__), float(volume__), symbol)
        savelog(log_dict)
        
        return ret__


class mt5_sell:
    
    def __new__(self, symbol, sl, tp, vol):
    
        #TRADE|TYPE|SYMBOL|STOPLOSS|STOPGAIN|VOLUME
        flag = str('OPEN|'+'-1'+'|'+str(symbol)+'|'+str(sl)+'|'+str(tp)+'|'+str(vol))
        
        context = zmq.Context()
        reqSocket = context.socket(zmq.REQ)
        
        
        connect = reqSocket.connect(SERVER)
        print(connect)
        
        try:
            reqSocket.send_string(flag)
            msg = reqSocket.recv_string()
        except zmq.Again as e:
            print('Waiting for Push MT5...')
        
        ticket__, price__, bid__, ask__, volume__ = msg.split(',')
        
        ret__ = [int(ticket__), float(price__), float(volume__)]
        
        
        log_dict[str(ticket__)] = openLog('short', float(price__), float(volume__), symbol)
        savelog(log_dict)
        return ret__

    

class mt5_close:
    
    def __new__(self, ticket):
    
        #CLOSE|TICKET 
        flag = str('CLOSE|'+str(ticket))
        
        context = zmq.Context()
        reqSocket = context.socket(zmq.REQ)
        connect = reqSocket.connect(SERVER)
        
        try:
            reqSocket.send_string(flag)
            msg = reqSocket.recv_string()
        except zmq.Again as e:
            print('Waiting for Push MT5...')

        status__, price__  ,bid__, ask__, volume__= msg.split(',')
        
        ret__ = [int(status__), float(price__), float(volume__)]
        
        close_flag = closeLog(str(ticket), price__)
        
        savelog(log_dict)
        return ret__

        
            

                        