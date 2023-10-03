from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_buttons = ReplyKeyboardMarkup([[KeyboardButton("Начисление Кэшбэка")], [KeyboardButton("Cписание Кэшбэка")],
                                    [KeyboardButton("Баланс"), KeyboardButton("Кэшбэки")]],
                                   resize_keyboard=True)
home_button = ReplyKeyboardMarkup([[KeyboardButton("🏠Главный страница")]],
                                  resize_keyboard=True)

qr_button = ReplyKeyboardMarkup([[KeyboardButton("Генерация QR-кода")], [KeyboardButton("🏠Главный страница")]],
                                  resize_keyboard=True)

report_button = ReplyKeyboardMarkup([[KeyboardButton("Посмотреть последние кэшбэки")], [KeyboardButton("Полный список кэшбэков и выплат")],
                                     [KeyboardButton("🏠Главный страница")]], resize_keyboard=True)