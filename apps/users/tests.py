import requests
a = requests.post("http://80.80.212.224:8080/ut3/hs/radius_bot/type_report",
                  auth=("django_admin", "DJango_96547456"),
                  json={"start": "20230602", "end": "20230505"})
# # b = requests.get("http://80.80.212.224:8080/ut3/hs/radius_bot/cash_flow",
# #                   headers={"Authorization": "Basic ZGphbmdvX2FkbWluOjE0Nzc4OQ=="},
# #                   json={"start": "20230428", "end": "20230504"})
with open("juju.xls", 'wb') as destination:
    destination.write(a.content)
import excel2img

excel2img.export_img(fn_excel="juju.xls", fn_image="daily.png")
