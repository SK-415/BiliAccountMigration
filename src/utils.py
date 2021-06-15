import time
from hashlib import md5
from urllib.parse import urlencode
from typing import Dict, Union
import httpx


class RequestError(Exception):
    def __init__(self, code, message=None, data=None):
        self.code = code
        self.message = message
        self.data = data
    
    def __repr__(self):
        return f"<RequestError code={self.code} message={self.message}>"
    
    def __str__(self):
        return self.__repr__()


def encrypt_params(params: Dict, local_id=0) -> Dict:
    
    params['local_id'] = local_id,
    params['appkey'] = "4409e2ce8ffd12b8"
    params['ts'] = int(time.time())
    resp = post("https://passport.bilibili.com/api/oauth2/getKey")
    params['sign'] = md5(
        f"{urlencode(sorted(params.items()))}59b43e04ad6965f34319062b478f83dd".encode('utf-8')
    ).hexdigest()
    return params


def request(method: str, url: str, encrypt=False, params={}, **kw) -> Dict:

    if encrypt:
        encrypt_params(params)
    resp = httpx.request(method, url, params=params, **kw).json()
    if resp['code'] != 0:
        raise RequestError(code=resp['code'], message=resp['message'], data=resp.get())
    return resp['data']


def get(url: str, **kw):

    return request('GET', url, **kw)


def post(url: str, **kw):

    return request('POST', url, **kw)