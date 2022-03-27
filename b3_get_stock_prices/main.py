import threading
from datetime import datetime
from configurations import HOST, PORT
from b3_get_stock_prices.stock import get_price_description
from b3_get_stock_prices.redis_client import set_stock_price_and_description
from rrcq.rrcq import RedisReadyCircularQueue


def main_routine(stock_symbol):
    j, description, price, time = get_price_description(stock_symbol)
    set_stock_price_and_description(stock_symbol, description, price, time)


def lambda_handler(event, context):
    start = datetime.now()
    batch_size = 20
    rrcq = RedisReadyCircularQueue(HOST, PORT)
    mybatch = rrcq.get_batch(batch_size)
    mybatch_copy = mybatch.copy()

    while mybatch:
        for i in range(10):
            stock_symbol = mybatch.pop(0)
            t = threading.Thread(target=main_routine, args=(stock_symbol,))
            t.start()

    delta = str(datetime.now() - start)

    result = {
        'statusCode': 200,
        'Processed Batch Size': batch_size,
        'Processed Batch': mybatch_copy,
        'Delta': delta
    }

    print(result)
    return None