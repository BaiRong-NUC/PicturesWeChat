import json
import requests
import os
from dotenv import load_dotenv
from message import Message


class TokenInfo:
    # refresh参数用于决定是否强制刷新token，默认为False
    def __init__(self, refresh=False):
        load_dotenv()
        self.app_id = os.getenv("APP_ID")
        self.app_secret = os.getenv("APP_SECRET")
        self.user_id = os.getenv("USER_ID")
        if refresh == False:
            self.access_token = os.getenv("ACCESS_TOKEN")
        else:  # 重新获取access_token
            access_token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
            self.access_token = (
                requests.get(access_token_url).json().get("access_token")
            )


class User:
    def __init__(self, refresh_token=False):
        self.token_info = TokenInfo(refresh=refresh_token)
        self.message = Message(self.token_info.access_token, self.token_info.user_id)

    def send_message(self, content):
        errcode, error_message = self.message.send_message(content)
        if errcode == 0:
            print("Message sent successfully!")
        else:
            print(
                f"Failed to send message, error code: {errcode}, error message: {error_message}"
            )
