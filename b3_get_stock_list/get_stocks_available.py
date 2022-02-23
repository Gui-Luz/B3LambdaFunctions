import urllib3
import base64
import json
from configurations import SYMBOLS_ENDPOINT

urllib3.disable_warnings()


def json_base64_encoder(json_object):
    string_encoded = base64.b64encode(bytes(str(json_object), 'utf-8')).decode("utf-8")
    return string_encoded


def request_page_return_json(url):
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
    r = http.request('GET', url)
    j = json.loads(r.data)
    return j


def get_symbols_total_pages():
    base64_json = {'language': 'en-us', 'pageNumber': 1, 'pageSize': 100}
    string_encoded = json_base64_encoder(base64_json)
    j = request_page_return_json(SYMBOLS_ENDPOINT + string_encoded)
    total_pages = j['page']['totalPages']
    return total_pages


def get_symbols():
    total_pages = get_symbols_total_pages()
    symbols_list = []
    for page in range(total_pages):
        page += 1
        base64_json = {'language': 'en-us', 'pageNumber': page, 'pageSize': 100}
        string_encoded = json_base64_encoder(base64_json)
        j = request_page_return_json(SYMBOLS_ENDPOINT + string_encoded)
        results = j['results']
        for result in results:
            symbol = result['code']
            symbols_list.append(symbol)
    return sorted(symbols_list)