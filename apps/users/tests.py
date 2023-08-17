import requests
a = requests.post("https://billing.radius.uz:4012/radius_ut/hs/radius_bot/type_report",
                  auth=("django_admin", "DJango_96547456"),
                  json={"start": "20230813", "end": "20230708"})
# # a = requests.post("http://80.80.212.224:8080/ut3/hs/radius_bot/type_report",
# #                   auth=("django_admin", "DJango_96547456"),
# #                   json={"start": "20230611", "end": "20230622"})
with open("juju.xls", 'wb') as destination:
    destination.write(a.content)
import excel2img

excel2img.export_img(fn_excel="juju.xls", fn_image="daily.png")


