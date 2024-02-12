#forrarse con ethereums es el objetivo

#autor:Fran Carrasco
#email:francelta@gmail.com
#derechos: privados y pertenecientes al autor.



from datetime import datetime, timedelta
import time
# from binance import *
try:
    from pybit import spot
except:
    pip.main(['install', 'pybit'])
    from pybit import spot
import pip
try:
    import ccxt
except:
    pip.main(['install', 'ccxt'])
    import ccxt
try:
    import requests
except:
    pip.main(['install', 'requests'])
    import requests
try:
    import json
except:
    pip.main(['install', 'json'])
    import json

try :
    from decouple import config
except:
    pip.main(['install', 'python-decouple'])
    from decouple import config
try:
    import numpy as np
except:
    pip.main(['install', 'numpy'])
    import numpy as np
try:
    import sqlite3
except:
    pip.main(['install', 'sqlite3'])
    import sqlite3
    
    
#valores de número de decimales para ethereum (quantity, para número de monedas, value, para precio)):
decimal_quantity=4
decimal_value=2


apiKey = config('BYBIT_API_KEY')
apisecret = config('BYBIT_API_PASS')
max_estocastica=float(config('MAX_ESTOCASTICA'))
max_rsi=float(config('MAX_RSI'))
max_estocastica_rsi=float(config('MAX_ESTOCASTICA_RSI'))
limite_rsi=float(config('LIMIT_RSI'))
dinero_orden=float(config('DINERO_ORDEN'))
variable_venta=float(config('VARIABLE_VENTA'))
tiempo_espera=float(config('TIEMPO_COMPRA'))
perdidas_limit=float(config('PERDIDAS_LIMIT'))

session = spot.HTTP(
        endpoint='https://api.bybit.com', 
        api_key=apiKey,
        api_secret=apisecret)

session_unauth = spot.HTTP(
    endpoint='https://api.bybit.com'
)


print("Iniciando...")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")


##############################################################################################################
##############################################################################################################

    
    
def precio_mas_alto_24h():
    # Define el endpoint para obtener los precios
    endpoint = "https://api.bybit.com/v2/public/tickers"

    # Define los parámetros para la petición
    params = {
        "symbol": "ETHUSD"
    }

    # Realiza la petición
    response = requests.get(endpoint, params=params)

    # Verifica si la petición fue exitosa
    if response.status_code != 200:
        raise Exception("Error al obtener los precios")

    # Parsea la respuesta en formato JSON
    data = json.loads(response.text)
    

    # Obtiene el precio más alto y más bajo de los últimos 15 minutos
    high = data["result"][0]["high_price_24h"]


    return high


def calculate_stochastic():
    # Inicializa la instancia de la bolsa de valores
    exchange = getattr(ccxt, 'bybit')()

    # Obtiene los precios de los últimos 14 períodos (14 * 5 minutos)
    candles = exchange.fetch_ohlcv('ETHUSD', '5m', limit=14)

    # Obtiene el precio más alto y más bajo de los últimos 14 períodos
    high = max([candle[2] for candle in candles])
    low = min([candle[3] for candle in candles])

    # Obtiene el precio actual
    ticker = exchange.fetch_ticker('ETHUSD')
    last_price = ticker["last"]

    # Cálcula la variable estocástica
    stochastic = (last_price - low) / (high - low)

    return stochastic



def calculate_rsi():
    # Inicializa la instancia de la bolsa de valores
    exchange = getattr(ccxt, 'bybit')()

    # Obtiene los precios de los últimos 5 minutos
    candles = exchange.fetch_ohlcv('ETHUSD', '5m')

    # Obtiene los precios de cierre de los últimos 5 minutos
    closes = [candle[4] for candle in candles]

    # Obtiene las diferencias entre los precios de cierre
    diffs = [closes[i] - closes[i-1] for i in range(1, len(closes))]

    # Obtiene las ganancias y pérdidas
    gains = [diff if diff > 0 else 0 for diff in diffs]
    losses = [abs(diff) if diff < 0 else 0 for diff in diffs]

    # Obtiene las medias móviles de 14 períodos
    avg_gain = sum(gains[-14:]) / 14
    avg_loss = sum(losses[-14:]) / 14

    # Cálcula el RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_stochastic_rsi():
    # Cálcula la variable estocástica
    stochastic = calculate_stochastic()
    
    # Cálcula el RSI
    rsi = calculate_rsi()

    # Cálcula el RSI estocástico
    stochastic_rsi = stochastic * (100 - rsi) + rsi

    return stochastic_rsi/100

def calculate_probability_of_increase():
    # Calcular la variable estocástica de 14 períodos
    stochastic = calculate_stochastic()
    stochastic_rsi = calculate_stochastic_rsi()

    # Calcular el RSI de 14 períodos
    rsi = calculate_rsi()

    # Cálcula la probabilidad de que el precio suba
    if stochastic < max_estocastica and rsi < max_rsi and stochastic_rsi < max_estocastica_rsi:
        resultado=True
    else:
        resultado=False
    
    return resultado


def get_current_and_previous_price():
    # Inicializa la instancia de la bolsa de valores
    exchange = getattr(ccxt, 'bybit')()

    # Obtiene el precio actual
    ticker = exchange.fetch_ticker('ETHUSD')
    current_price = ticker["last"]
    
    # Obtiene el tiempo actual
    current_time = time.time()
    
    # Obtiene el precio hace 5 minutos
    five_minutes_ago = current_time - (5 * 60)
    
    candles = exchange.fetch_ohlcv('ETHUSD', '1m', limit=5, since=int(five_minutes_ago) * 1000)
    
    previous_price = candles[0][4]

    return current_price, previous_price


def get_max_and_min_price():
    exchange = ccxt.bybit()

    current_time = time.time()
        
        # Obtiene el precio hace 5 minutos
    five_minutes_ago = current_time - (5 * 60)

    ohlcv = exchange.fetch_ohlcv('ETHUSD', '1m', limit=50, since=int(five_minutes_ago) * 1000)

    # Calcular el precio máximo en los últimos 5 minutos
    prices = [candle[2] for candle in ohlcv]
    max_price = max(prices)

    # Calcular el precio mínimo en los últimos 5 minutos
    min_price = min(prices)
    
    return max_price, min_price

def get_eth_price():
    
    eth_price=session_unauth.latest_information_for_symbol(
    symbol="ETHUSDT")
    time.sleep(0.1)
    eth_price=eth_price['result']['lastPrice']
    eth_price=float(eth_price)
    return(float(eth_price))

def dame_saldo_usdt():
    
    qtys=session.get_wallet_balance(coin="USDT")
    time.sleep(0.1)
    for qty in qtys['result']['balances']:
        if qty['coin'] == 'USDT':
            qty=float(qty['free'])
            break
    
    return(float(qty))

def dame_saldo_eth():
        
    qtys=session.get_wallet_balance(coin="ETH")
    time.sleep(0.1)
    for qty in qtys['result']['balances']:
        if qty['coin'] == 'ETH':
            qty=float(qty['total'])
            break
    try:
        cantidad= qty
        return(float(cantidad))
    except:
        cantidad=0
    
        return(float(cantidad))

def dame_saldo_usdt_total():
        
    saldo_eth=dame_saldo_eth()*get_eth_price()
    saldo_usdt=dame_saldo_usdt()
    saldo_total=saldo_eth+saldo_usdt
    return(saldo_total)

##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
 
#----------------------------------------------------  M  A  I  N  ----------------------------------------------------#
def main():
    alerta_venta=False
    vender=False

    while True:
        
        print(f'SALDO TOTAL EN USDT: {round(dame_saldo_usdt_total(),2)}')
        lista_rsi=[]
        try:
            time.sleep(4)
            
            saldos=session.get_wallet_balance(coin="USDT")
            
            
            for saldo in saldos['result']['balances']:
                if saldo['coin'] == 'USDT':
                    saldo=float(saldo['total'])
                    break
            
            qtys=session.get_wallet_balance(coin="ETH")
            
            for qty in qtys['result']['balances']:
                
                if qty['coin'] == 'ETH':
                    qty=float(qty['free'])
                    qty=round(qty,decimal_quantity)
                    cantidad=qty
                    
                    break
                else:
                    cantidad=0
                    break
            
            
            if cantidad > 0.01:
                
                cotizacion=session_unauth.last_traded_price(symbol="ETHUSDT")
                    
                cotizacion=float(cotizacion['result']['price'])
                
                precio_venta=cotizacion+variable_venta
                
                print(f'voy a poner a la venta {cantidad} ETH\'s a {precio_venta} USDT')
                try:
                    order = session.place_active_order(
                        symbol="ETHUSDT",
                        side="Sell",
                        type="LIMIT_MAKER",
                        qty=cantidad,
                        price=precio_venta,
                        timeInForce="GTC"
                    )
                    time.sleep(0.1)
                except:
                    # print("2do intento:")
                    try: 
                        order = session.place_active_order(
                            symbol="ETHUSDT",
                            side="Sell",
                            type="LIMIT_MAKER",
                            qty='{:.4f}'.format(round(cantidad-0.0001,4)),
                            price=round(precio_venta,2),
                            timeInForce="GTC"
                        )

                    except:
                        print("no se ha podido colocar la orden de venta")
                        pass 
                try:
                    print(order)
                except:
                    pass
                    
        #   si el valor del RSI sube de 60, se activa una alerta de venta, en caso de que llegue a 70 se venderá, pero si vuelve a bajar de 60 y el precio 
        #   sigue siendo rentable, venderá
        
            valor_rsi=calculate_rsi()
        
        
            if (valor_rsi > 75) and (alerta_venta == False):
                    alerta_venta= True
                    vender=False
            if (valor_rsi < 75) and (valor_rsi> 70) and (alerta_venta == True):
                vender=True
                alerta_venta=False
            if valor_rsi < 70:
                alerta_venta=False
                vender=False
            
            dinero_orden=int(dame_saldo_usdt_total()/30)
            
            if dinero_orden < 10:
                dinero_orden=10
                
                
            if saldo > dinero_orden:
                
                historico=session_unauth.public_trading_records(symbol='ETHUSDT')
                time.sleep(0.1)
                cotizacion=session_unauth.last_traded_price(symbol="ETHUSDT")
                time.sleep(0.1)
                cotizacion=float(cotizacion['result']['price'])
                
                
    #-------------------------------------------  C O M P R A   N O R M A L    O    C    O -------------------------------------------#                   
                if  calculate_probability_of_increase()==True:
                    print("compra normal")
                    
                    n=dinero_orden
                    order=session.place_active_order(
                            symbol="ETHUSDT",
                            side="Buy",
                            type="MARKET",
                            qty=n,
                            timeInForce="GTC"
                        )
                    time.sleep(0.1)
                    print(order)
                    time.sleep(0.1)
                    try:
                        orderID=order['result'][0]['orderId']
                        print(orderID)
                        order=session.user_trade_records(symbol="ETHUSDT")
                        time.sleep(0.1)
                        for i in order['result']:
                            if str(i['orderId']) == str(orderID):
                                precio_compra=round(float(i['price']),2)
                                cantidad=float(i['qty'])
                                print("compra de ",cantidad," ETH's a ",precio_compra," USDT")
                                break
                    except:
                        precio_compra=float(cotizacion)
                        pass
                    
                    qtys=session.get_wallet_balance(coin="ETH")
                    time.sleep(0.1)
                    for qty in qtys['result']['balances']:
                        if qty['coin'] == 'ETH':
                            qty=float(qty['free'])
                            qty=round(qty,decimal_quantity)
                            break
                    cantidad=qty
                    precio_venta = precio_compra + variable_venta 
                    
                    print(f'voy a poner a la venta {cantidad} ETH\'s a {precio_venta} USDT')
                    try:
                        order = session.place_active_order(
                            symbol="ETHUSDT",
                            side="Sell",
                            type="LIMIT_MAKER",
                            qty=cantidad,
                            price=precio_venta,
                            timeInForce="GTC"
                        )
                        time.sleep(0.1)
                        
                    except:
                        # print("2do intento:")
                        try: 
                            order = session.place_active_order(
                                symbol="ETHUSDT",
                                side="Sell",
                                type="LIMIT_MAKER",
                                qty='{:.4f}'.format(round(cantidad-0.0001,4)),
                                price=round(precio_venta,2),
                                timeInForce="GTC"
                            )
                            time.sleep(0.1)

                        except:
                            print("no se ha podido colocar la orden de venta")
                            pass 
                    try:
                        print(order)
                    except:
                        pass
                    print('\n')
                    print('\n')
                    print('\n')
                    print('\n')
                    print(f' O R D E N   C O M P R A D A   C O N   E X I T O   A   {precio_compra} USDT')
                    print('\n')
                    print('\n')
                    print('\n')
                    print('\n')
                    time.sleep(int(tiempo_espera))
                
                # else:
                #     print("-----------------------------------------------------------------------------------------------")
                #     print(f'---------------------------------------------------------------------------- {cotizacion} USDT -----')
                #     print("-----------------------------------------------------------------------------------------------")
                #     print(f'----------- ESTOCÁSTICA     | máx {max_estocastica} |---------------------------------------------- {round(calculate_stochastic(),2)}  ---')
                #     print("-----------------------------------------------------------------------------------------------")
                #     print(f'------------R S I           | máx    {max_rsi} | ---------------------------------------- {round(calculate_rsi(),2)}  ---')
                #     print("-----------------------------------------------------------------------------------------------")
                #     print(f'----------- ESTOCASTICA_RSI | máx {max_estocastica_rsi} | --------------------------------------------- {round(calculate_stochastic_rsi(),2)}  ---')
                #     print("-----------------------------------------------------------------------------------------------")
        
            try:           
                saldos=session.get_wallet_balance(coin="USDT")
                time.sleep(0.1)
                for saldo in saldos['result']['balances']:
                    if saldo['coin'] == 'USDT':
                        saldo=float(saldo['total'])
                        break
                orders = session.query_active_order(symbol="ETHUSDT")
                time.sleep(0.1)
                cotizacion=session_unauth.last_traded_price(symbol="ETHUSDT")
                time.sleep(0.1)
                cotizacion=float(cotizacion['result']['price'])
                
                
                print("-----------------------------------------------------------------------------------------------")
                print(f'---------------------------------------------------------------------------- {cotizacion} USDT -----')
                print("-----------------------------------------------------------------------------------------------")
                print(f'----------- ESTOCÁSTICA     | máx {max_estocastica} |---------------------------------------------- {round(calculate_stochastic(),2)}  ---')
                print("-----------------------------------------------------------------------------------------------")
                print(f'----------- R S I           | máx    {max_rsi} | ---------------------------------------- {round(calculate_rsi(),2)}  ---')
                print("-----------------------------------------------------------------------------------------------")
                print(f'----------- ESTOCASTICA_RSI | máx {max_estocastica_rsi} | --------------------------------------------- {round(calculate_stochastic_rsi(),2)}  ---')
                print("-----------------------------------------------------------------------------------------------")
                
                if orders['result'] == []:
                    print('\n')
                    alerta_venta=False
                    vender=False
                else:
                    if alerta_venta == True:
                        print(f'A L E R T A   D E   V E N T A')
                    print("\n")
                    print(f'------------------------------------------------------------ S A L D O -------- {round(saldo,2)} USDT ---')
                    print("-----------------------------------------------------------------------------------------------")
                    print("        ID                     PRECIO VENTA                   FECHA COMPRA")
                    print("-----------------------------------------------------------------------------------------------")
                precios=[]   
                for i in orders['result']:
                    id_precio=[]
                    fecha_order=int(i['time'])                
                    order_id=i['orderId']
                    id_precio.append(order_id)
                    order_id=int(order_id)
                    price=float(i['price'])
                    id_precio.append(price)
                    precios.append(id_precio)
                    qty=float(i['origQty'])
                    
                    fecha_order=datetime.fromtimestamp(fecha_order/1000)
                    fecha_order=fecha_order.strftime('%d-%m-%Y %H:%M')
                    
                    quantity=float(i['origQty'])
                    
                    cotizacion=session_unauth.last_traded_price(symbol="ETHUSDT")
                    time.sleep(0.1)
                    cotizacion=float(cotizacion['result']['price'])
                    
                    rsi=float(calculate_rsi())
                    time.sleep(0.1)
                    
                    if (cotizacion < price-perdidas_limit-variable_venta) or ((rsi > limite_rsi) and (cotizacion > price-variable_venta)) or (vender ==True and cotizacion > price-variable_venta+12) or (cotizacion > price):
                  
                        session.cancel_active_order(orderId=order_id)
                        print(f'cancelada orden de venta  ETH con id {order_id} a {price} USDT, se venderá automáticamente a {cotizacion} USDT')
                        print(f'la compra fué de {price-variable_venta}, con lo cual arroja un beneficio/pérdida de {round((cotizacion-price+variable_venta)*qty,2)} USDT')
                        time.sleep(0.1)
                        qtys=session.get_wallet_balance(coin="ETH")
                        for qty in qtys['result']['balances']:
                            if qty['coin'] == 'ETH':
                                qty=float(qty['free'])
                                break
                        qty=round(qty,decimal_quantity)
                        
                        order=session.place_active_order(
                        symbol="ETHUSDT",
                        side="Sell",
                        type="LIMIT_MAKER",
                        qty='{:.4f}'.format(round(qty-0.0001,4)),
                        price=cotizacion,
                        timeInForce="GTC"
                    )
                        time.sleep(1)
                
                        order_id=order['result']['orderId']
                        precio_venta=float(order['result']['price'])
                        
                        print(order)
                    
                    print(" " +str(i['orderId'])+"           "+ str(round(float(i['price']),2))+"                        "+ str(fecha_order))
                    print("\n")
                
                print("-----------------------------------------------------------------------------------------------")
                print("-----------------------------  CALCULANDO... --------------------------------------------------")
                print("-----------------------------------------------------------------------------------------------")
                print(f'---------------------------------------------------------------------------- {cotizacion} USDT -----')
                print("-----------------------------------------------------------------------------------------------")
                
                print("\n")
                
            except:
                pass
            
                    
        except:
            print("reiniciando...")

while True:
    try:
        main()
    except:
        pass
                                                                                          