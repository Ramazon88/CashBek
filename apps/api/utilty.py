import re

import requests
from django.utils.translation import gettext_lazy as _

from apps.api.exceptions import CustomError
from config.settings import SMS_TOKEN, SMS_URL

phone_regex = re.compile(r"^(!?){0}([998]){3}([3-9]){1}([0-9]){1}([0-9]){7}$")


def check_phone(phone):
    if re.fullmatch(phone_regex, phone):
        return phone

    else:
        data = {
            "success": False,
            'message': _("The phone number is incorrect")
        }
        raise CustomError(data)


def send_sms(phone, code):
    headers = {"Authorization": SMS_TOKEN}
    data = {
                          "messages": [
                              {
                                  "recipient": phone,
                                  "message-id": "omo000000001",
                                  "sms": {
                                      "originator": "3700",
                                      "content": {
                                          "text": f"CashBek code: {code}"
                                      }
                                  }
                              }
                          ]
                      }
    url = SMS_URL
    data = requests.post(url=url, headers=headers, json=data)
    return True
