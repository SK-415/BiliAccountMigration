import base64
from typing import Dict

import rsa

from .utils import get, post

BASE_URL = "https://passport.bilibili.com/x/passport-tv-login/"


def get_qrcode():
    """获取登录的二维码链接和 auth_code
    url: (qrcode url), auth_code"""

    return post(f"{BASE_URL}qrcode/auth_code", encrypt=True)


def login_qrcode(auth_code):

    return post(f"{BASE_URL}qrcode/poll",
                        encrypt=True, params={'auth_code': auth_code})


def send_sms(tel, cid=86):
    """发送短信验证码并返回 captcha_key"""

    resp = post(f"{BASE_URL}sms/send", params={'tel': tel, 'cid': cid}, encrypt=True)
    return resp['captcha_key']


def login_sms(code, *, tel, cid, captcha_key):
    params = {
        'code': code,
        'tel': tel,
        'cid': cid,
        'captcha_key': captcha_key,
    }
    return post(f"{BASE_URL}login/sms", params=params, encrypt=True)


def encrypt_pwd(pwd: str):
    """加密密码"""

    resp = post("https://passport.bilibili.com/api/oauth2/getKey", encrypt=True)
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(resp["key"].encode())
    msg = (resp["hash"] + pwd).encode()
    return base64.b64encode(rsa.encrypt(msg, pub_key)).decode('ascii')


def login_pwd(name, pwd):
    """密码登录"""
    
    params = {
        'username': name,
        'password': encrypt_pwd(pwd)
    }
    return post(f"{BASE_URL}login", params=params, encrypt=True)

def login(type_='qrcode'):
    """使用二维码、短信或密码登录 B站"""

    if type_ == 'sms':
        cid = input("请输入你的区号（86）：")
        cid = int(cid) if cid else 86
        tel = input("请输入要登录的手机号：")
        captcha_key = send_sms(tel, cid)
        code = input("请输入验证码：")
        return login_sms(code, tel=tel, cid=cid, captcha_key=captcha_key)
    elif type_ == 'pwd':
        pwd = input("请输入密码：")
        