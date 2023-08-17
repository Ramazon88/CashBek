import requests

response = requests.get(url=f"https://billing.radius.uz:4012/radius_ut/hs/radius_bot/order/delay_all",
                        auth=("django_admin", "DJango_96547456"), timeout=20).json()

print(len(response))