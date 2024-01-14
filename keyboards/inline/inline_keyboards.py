from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

locations = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Toshkentdagi Filiali", callback_data="toshkent_filial")
        ],
        [
            InlineKeyboardButton(text="Samarqandagi Filiali", callback_data="samarqand_filial")
        ],
        [
            InlineKeyboardButton(text="Fargonadagi Filiali", callback_data="fargona_filial")
        ]
    ]
)

admin_panel_send = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑‍🎓 O'quvchiga Xabar Yuborish", callback_data="send_message_stu")
        ]
    ]
)