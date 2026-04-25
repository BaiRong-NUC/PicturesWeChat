import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app_id = os.getenv("APP_ID")
app_secret = os.getenv("APP_SECRET")
user_id = os.getenv("USER_ID")
access_token = os.getenv("ACCESS_TOKEN")
# access_token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
# access_token = requests.get(access_token_url).json().get("access_token")
# print(f"Access Token: {access_token}")
# print(requests.get(url).json())

# 发送文本消息
# POST https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN


if __name__ == "__main__":
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"
    data = {
        "touser": user_id,
        "msgtype": "text",
        "text": {"content": "Hello, this is a test message!"},
    }
    data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    response = requests.post(url, data=data)
    # print(response.json())
    if response.json().get("errcode") != 0:
        print(f"Failed to send message: {response.json()}")
