import requests
from telegram import Bot


a = requests.post("https://billing.radius.uz:4012/radius_ut/hs/radius_bot/type_report",
                  auth=("django_admin", "DJango_96547456"),
                  json={"start": '20230918'})
file_name = "report_.xls"

with open(file_name, 'wb') as destination:
    destination.write(a.content)

