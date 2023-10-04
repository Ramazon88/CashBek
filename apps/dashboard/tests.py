from django.test import TestCase
# import qrcode
# from io import BytesIO
#
# from telegram import InputFile, Bot
#
# from config.settings import BOT_TOKEN
#
# # Data to encode into the QR code
# data = "JUJU"
#
# # Generate a QR code instance
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
#
# # Add data to the QR code
# qr.add_data(data)
# qr.make(fit=True)
#
# # Create a QR code image as an in-memory binary stream
# img_stream = BytesIO()
# qr.make_image(fill_color="black", back_color="white").save(img_stream)
#
# # Get the binary data from the in-memory stream
# binary_data = img_stream.getvalue()
# bot = Bot(token=BOT_TOKEN)
# bot.send_photo(chat_id=254118850, photo=InputFile(binary_data))


