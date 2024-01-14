from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🪪 Ro'yxatdan O'tish")
        ]
    ], resize_keyboard=True
)

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Telefon Raqamni Jo'natish", request_contact=True)
        ]
    ], resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📨 Shartnoma Tuzish")
        ],
        [
            KeyboardButton(text="📍 Filiallar")
        ],
        [
            KeyboardButton(text="📞 Biz Bilan Aloqa")
        ]
    ], resize_keyboard=True
)

location_send = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvni Jonatish", request_location=True)
        ]
    ], resize_keyboard=True
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Xa"),
            KeyboardButton(text="❌ Yo'q")
        ]
    ], resize_keyboard=True
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Savol Qoshish")
        ],
        [
            KeyboardButton(text="👤➕ Admin Qoshish")
        ],
        [
            KeyboardButton(text="📨 Shartnoma Tuzish")
        ],
        [
            KeyboardButton(text="📍 Filiallar")
        ],
        [
            KeyboardButton(text="📞 Biz Bilan Aloqa")
        ],
        [
            KeyboardButton(text="👥 Sinflar")
        ],
        [
            KeyboardButton(text="➕🧑‍🎓 O'quvchi Qoshish")
        ],
    ], resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor Qilish")
        ]
    ], resize_keyboard=True
)

subjects = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1️⃣ Matematika")
        ],
        [
            KeyboardButton(text="2️⃣ Biologiya")
        ],
        [
            KeyboardButton(text="3️⃣ Ona Tili")
        ]
    ], resize_keyboard=True
)

a_b_d = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A")
        ],
        [
            KeyboardButton(text="B")
        ],
        [
            KeyboardButton(text="D")
        ]
    ], resize_keyboard=True
)

classes = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor Qilish")
        ],
        [
            KeyboardButton(text="1-A")
        ],
        [
            KeyboardButton(text="1-B")
        ],
        [
            KeyboardButton(text="2-A")
        ],
        [
            KeyboardButton(text="2-B")
        ],
        [
            KeyboardButton(text="3-A")
        ],
        [
            KeyboardButton(text="3-B")
        ],
        [
            KeyboardButton(text="4-A")
        ],
        [
            KeyboardButton(text="4-B")
        ],
        [
            KeyboardButton(text="5-A")
        ],
        [
            KeyboardButton(text="5-B")
        ],
        [
            KeyboardButton(text="6-A")
        ],
        [
            KeyboardButton(text="6-B")
        ],
        [
            KeyboardButton(text="7-A")
        ],
        [
            KeyboardButton(text="7-B")
        ],
        [
            KeyboardButton(text="8-A")
        ],
        [
            KeyboardButton(text="8-B")
        ],
        [
            KeyboardButton(text="9-A")
        ],
        [
            KeyboardButton(text="9-B")
        ],
    ], resize_keyboard=True
)