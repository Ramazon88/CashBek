from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_buttons = ReplyKeyboardMarkup([[KeyboardButton("Начать")]], resize_keyboard=True)
home_button = ReplyKeyboardMarkup([[KeyboardButton("🏠Главный страница")]],
                                  resize_keyboard=True)
link = ReplyKeyboardMarkup([[KeyboardButton("Нет ссылки")], [KeyboardButton("🏠Главный страница")]],
                           resize_keyboard=True)

confirm = ReplyKeyboardMarkup([[KeyboardButton("Отправить")], [KeyboardButton("🏠Главный страница")]],
                              resize_keyboard=True)

report_button = ReplyKeyboardMarkup(
    [[KeyboardButton("Посмотреть последние кэшбэки")], [KeyboardButton("Полный список кэшбэков и выплат")],
     [KeyboardButton("🏠Главный страница")]], resize_keyboard=True)
