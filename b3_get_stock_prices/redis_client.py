import redis
from configurations import HOST, PORT

r_cli = redis.Redis(host=HOST, port=PORT, db=0)


def set_stock_price_and_description(stock, description, price, time):
    r_cli.set(f'price:{stock}', str(description) + ':' + str(price) + ':' + str(time))