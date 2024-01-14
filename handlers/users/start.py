import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, InputFile
import random
from loader import *
from keyboards.default.default_keyboards import *
from keyboards.inline.inline_keyboards import *
from states.states import *

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    db_manager.create_table()
    # db_manager.delete_admins()
    # db_manager.insert_admin()
    # db_manager.delete_table(chat_id=message.chat.id)
    if db_manager.is_admin(chat_id=message.chat.id):
        await message.answer(text="Botga Xush Kelibsiz", reply_markup=admin_panel)
    else:
        if db_manager.get_user(chat_id=message.chat.id):
            await message.answer(text=f"Assalomu Alaykum: {message.from_user.full_name} Botga Xush Kelibsiz!",
                                 reply_markup=user_main_menu)
        else:
            await message.answer(
                f"Assalomu Alaykum: {message.from_user.full_name} Yuksalish Maktabining Asosiy Botiga Xush Kelibsiz! "
                f"Iltimos: {message.from_user.full_name} Botdan Foydalanish Uchun Ro'yxatdan O'ting!",
                reply_markup=register)

@dp.message_handler(state="*", text="❌ Bekor Qilish")
async def cancelling(message: types.Message, state: FSMContext):
    text = f"❌ Bekor Qilindi!"
    await message.answer(text=text, reply_markup=admin_panel)
    await state.finish()

@dp.message_handler(text="🪪 Ro'yxatdan O'tish")
async def register_handler(message: types.Message, state: FSMContext):
    text = f"✍️ Iltimos Toliq Ismingizni Kiriting!"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterStates.full_name.set()

@dp.message_handler(state=RegisterStates.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    text = f"📞 Iltimos: {message.from_user.full_name} Telefon Raqamingizni Jonating Tugma Orqali!"
    await state.update_data({
        "full_name": message.text
    })
    await message.answer(text=text, reply_markup=phone_number)
    await RegisterStates.phone_number.set()

@dp.message_handler(state=RegisterStates.phone_number, content_types=types.ContentType.CONTACT)
async def get_phone_number_handler(message: types.Message, state: FSMContext):
    text = f"📍 Iltimos: {message.from_user.full_name} Joylashuingizni Jonating!"
    await state.update_data({
        "phone_number": message.contact.phone_number
    })
    await message.answer(text=text, reply_markup=location_send)
    await RegisterStates.location.set()

@dp.message_handler(state=RegisterStates.location, content_types=types.ContentType.LOCATION)
async def get_location_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "longitude": message.location.longitude,
        "latitude": message.location.latitude,
        "chat_id": message.chat.id
    })
    data = await state.get_data()
    if db_manager.insert_new_user(data=data):
        text = f"😊 Siz Botdan Muvaffaqqiyatli Ro'yxatdan O'tdingiz Botdan Foydalanishingiz Mumkin!"
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        text = f"😔 Kechirasiz Xatolik Yuz Berdi.Iltimos /start Bosib Qayta Urinib Ko'ring!"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(text="📍 Filiallar")
async def locations_handler(message: types.Message):
    text = f"Marxamat Bizning Filiallarimizdan Birini Tanlang"
    await message.answer(text=text, reply_markup=locations)

@dp.callback_query_handler(text="toshkent_filial")
async def uzb_filial_handler(call: types.CallbackQuery):
    text = f"😊 Toshkentagi Filialimiz"
    await call.message.answer_location(latitude=41.308052, longitude=69.217661)
    await call.message.answer(text=text)

@dp.callback_query_handler(text="samarqand_filial")
async def samarqand_filial_handler(call: types.CallbackQuery):
    text = f"😊 Samarqandagi Filialimiz"
    photo = InputFile(path_or_bytesio="./rasmlaaaaaaaaaaaaarrrrrrrrrrrrrrrrrrr/samarqand.png")

    await call.message.answer_photo(photo=photo, caption=text)

@dp.callback_query_handler(text="fargona_filial")
async def fargona_filial_handler(call: types.CallbackQuery):
    text = f"😊 Fargonadagi Filialimiz"
    photo = InputFile(path_or_bytesio="./rasmlaaaaaaaaaaaaarrrrrrrrrrrrrrrrrrr/fargona.png")
    await call.message.answer_photo(photo=photo, caption=text)

@dp.message_handler(text="📞 Biz Bilan Aloqa")
async def biz_bilan_aloqa_handler(message: types.Message):
    text = f"""
😊 Biz Bilan Boglasnish Uchun!

📞 +998951010600
📨 @yuksalish_maktab_admin
👨‍👩‍👧‍👦 @yuksalishmaktabi_news
"""
    await message.answer(text=text)

@dp.message_handler(text="📨 Shartnoma Tuzish")
async def shartnoma_handler(message: types.Message, state: FSMContext):
    text = f"😊 Biz Bilan Oqishga Rozimisiz?"
    await state.update_data({
        "page": "shartnoma"
    })
    photo = f""
    await message.answer(text=text, reply_markup=yes_no)

@dp.message_handler(text="✅ Xa")
async def ha_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data["page"] == "shartnoma":
        text = f"😊 Test Ishlashga Tayyormisiz?"
        await state.update_data({
            "page": "testga"
        })
        await message.answer(text=text, reply_markup=yes_no)
    elif data["page"] == "testga":
        fanlar = ["Biologiya", "Matematika", "Ona Tili"]
        random_fan = random.choice(fanlar)
        text = f"Sizning Testingiz: {random_fan} Dan Tayyormisiz?"
        if random_fan == "Ona Tili":
            await state.update_data({
                "page": "fandan_test",
                "fan": "ona_tili",
                "pagee": 1
            })
        else:
            await state.update_data({
                "page": "fandan_test",
                "fan": random_fan.lower(),
                "pagee": 1
            })
        await message.answer(text=text, reply_markup=yes_no)
    elif data["page"] == "fandan_test":
        fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
        db_manager.create_table_subject_result(chat_id=message.chat.id)
        if fann:
            db_manager.insert_table_sub(data=data, chat_id=message.chat.id)
            for i in fann:
                savol = i[1]
                idsi = i[0]
                a = i[2]
                b = i[3]
                d = i[4]
                true = i[-1]
                text = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                await message.answer(text=text, reply_markup=a_b_d)
                await state.update_data({
                    "pagee": int(idsi),
                    "fan": data["fan"],
                    "truesi": true,
                    "score": 0
                })
        else:
            await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!", reply_markup=user_main_menu)
            db_manager.delete_user(chat_id=message.chat.id)


@dp.message_handler(text="A")
async def a_variant_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sovol = db_manager.select_quest(idsi=data["pagee"], fan=data["fan"], true="A")
    data["pagee"] += 1
    fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
    if sovol:
        text = f"✅ To'g'ri Javob"
        db_manager.update_score(chat_id=message.chat.id)
        await message.answer(text=text, reply_markup=a_b_d)
        if data["pagee"] <= 10:
            if fann:
                for i in fann:
                    savol = i[1]
                    idsi = i[0]
                    a = i[2]
                    b = i[3]
                    d = i[4]
                    true = i[-1]
                    textt = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                    await message.answer(text=textt, reply_markup=a_b_d)
                    await state.update_data({
                        "pagee": int(idsi),
                        "fan": data["fan"],
                        "truesi": true
                    })
            else:
                await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!",
                                     reply_markup=user_main_menu)
                db_manager.delete_user(chat_id=message.chat.id)
        else:
            score = db_manager.is_accepted(chat_id=message.chat.id)
            if score != None:
                user = db_manager.select_user(chat_id=message.chat.id)
                lala = db_manager.select_65_score(chat_id=message.chat.id)
                await message.answer(text=f"Savol Berish Toxtatildi. Sizning Balingiz: {score[0]}\n😊 Siz Oqishga Qabul Qilindingiz Siz Haqingizda Ma'lumot Adminlarga Yuborildi Javob Kelishini Kuting!", reply_markup=ReplyKeyboardRemove())
                admins = db_manager.select_admin()
                text = f"""
🆔 ID Raqami: {user[0]}
📞 Telefon Raqam: {user[2]}
📕 Fani: {lala[1]}
⭐️ Ball: {lala[-1]}
"""
                for i in admins:
                    idsi = i[0]
                    await dp.bot.send_message(chat_id=idsi, text=text)
            else:
                scores = db_manager.select_score(chat_id=message.chat.id)
                text = f"😕 Kechirasiz: {message.from_user.full_name} Sizning Balingiz 65 Balldan Kam Bolgani Uchun Yuksalish Maktabida Oqiy Olmaysiz!.\nSizning Ballingiz: <b>{scores[0]}</b>"
                await message.answer(text=text)
                db_manager.delete_user(chat_id=message.chat.id)
    else:
        text = f"❌ Siz Notogri Variant Tanladingiz"
        fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
        await message.answer(text=text, reply_markup=a_b_d)
        if fann:
            for i in fann:
                savol = i[1]
                idsi = i[0]
                a = i[2]
                b = i[3]
                d = i[4]
                true = i[-1]
                textt = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                await message.answer(text=textt, reply_markup=a_b_d)
                await state.update_data({
                    "pagee": int(idsi),
                    "fan": data["fan"],
                    "truesi": true
                })
        else:
            await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!", reply_markup=user_main_menu)
            db_manager.delete_user(chat_id=message.chat.id)





@dp.message_handler(text="B")
async def a_variant_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sovol = db_manager.select_quest(idsi=data["pagee"], fan=data["fan"], true="B")
    data["pagee"] += 1
    fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
    if sovol:
        text = f"✅ To'g'ri Javob"
        db_manager.update_score(chat_id=message.chat.id)
        await message.answer(text=text, reply_markup=a_b_d)
        if data["pagee"] <= 10:
            if fann:
                for i in fann:
                    savol = i[1]
                    idsi = i[0]
                    a = i[2]
                    b = i[3]
                    d = i[4]
                    true = i[-1]
                    textt = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                    await message.answer(text=textt, reply_markup=a_b_d)
                    await state.update_data({
                        "pagee": int(idsi),
                        "fan": data["fan"],
                        "truesi": true
                    })
            else:
                await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!",
                                     reply_markup=user_main_menu)
                db_manager.delete_user(chat_id=message.chat.id)
        else:
            score = db_manager.is_accepted(chat_id=message.chat.id)
            if score != None:
                user = db_manager.select_user(chat_id=message.chat.id)
                lala = db_manager.select_65_score(chat_id=message.chat.id)
                await message.answer(
                    text=f"Savol Berish Toxtatildi. Sizning Balingiz: {score[0]}\n😊 Siz Oqishga Qabul Qilindingiz Siz Haqingizda Ma'lumot Adminlarga Yuborildi Javob Kelishini Kuting!",
                    reply_markup=ReplyKeyboardRemove())
                admins = db_manager.select_admin()
                text = f"""
🆔 ID Raqami: {user[0]}
📞 Telefon Raqam: {user[2]}
📕 Fani: {lala[1]}
⭐️ Ball: {lala[-1]}
"""
                for i in admins:
                    idsi = i[0]
                    await dp.bot.send_message(chat_id=idsi, text=text)
            else:
                scores = db_manager.select_score(chat_id=message.chat.id)
                text = f"😕 Kechirasiz: {message.from_user.full_name} Sizning Balingiz 65 Balldan Kam Bolgani Uchun Yuksalish Maktabida Oqiy Olmaysiz!.\nSizning Ballingiz: <b>{scores[0]}</b>"
                await message.answer(text=text)
                db_manager.delete_user(chat_id=message.chat.id)
    else:
        text = f"❌ Siz Notogri Variant Tanladingiz"
        fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
        await message.answer(text=text, reply_markup=a_b_d)
        if fann:
            for i in fann:
                savol = i[1]
                idsi = i[0]
                a = i[2]
                b = i[3]
                d = i[4]
                true = i[-1]
                textt = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                await message.answer(text=textt, reply_markup=a_b_d)
                await state.update_data({
                    "pagee": int(idsi),
                    "fan": data["fan"],
                    "truesi": true
                })
        else:
            await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!",
                                 reply_markup=user_main_menu)
            db_manager.delete_user(chat_id=message.chat.id)



@dp.message_handler(text="D")
async def a_variant_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sovol = db_manager.select_quest(idsi=data["pagee"], fan=data["fan"], true="D")
    data["pagee"] += 1
    fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
    if sovol:
        text = f"✅ To'g'ri Javob"
        db_manager.update_score(chat_id=message.chat.id)
        await message.answer(text=text, reply_markup=a_b_d)
        if data["pagee"] <= 10:
            if fann:
                for i in fann:
                    savol = i[1]
                    idsi = i[0]
                    a = i[2]
                    b = i[3]
                    d = i[4]
                    true = i[-1]
                    textt = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                    await message.answer(text=textt, reply_markup=a_b_d)
                    await state.update_data({
                        "pagee": int(idsi),
                        "fan": data["fan"],
                        "truesi": true
                    })
            else:
                await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!",
                                     reply_markup=user_main_menu)
                db_manager.delete_user(chat_id=message.chat.id)
        else:
            score = db_manager.is_accepted(chat_id=message.chat.id)
            if score != None:
                user = db_manager.select_user(chat_id=message.chat.id)
                lala = db_manager.select_65_score(chat_id=message.chat.id)
                await message.answer(
                    text=f"Savol Berish Toxtatildi. Sizning Balingiz: {score[0]}\n😊 Siz Oqishga Qabul Qilindingiz Siz Haqingizda Ma'lumot Adminlarga Yuborildi Javob Kelishini Kuting!",
                    reply_markup=ReplyKeyboardRemove())
                admins = db_manager.select_admin()
                text = f"""
🆔 ID Raqami: {user[0]}
📞 Telefon Raqam: {user[2]}
📕 Fani: {lala[1]}
⭐️ Ball: {lala[-1]}"""
                for i in admins:
                    idsi = i[0]
                    await dp.bot.send_message(chat_id=idsi, text=text)
            else:
                scores = db_manager.select_score(chat_id=message.chat.id)
                text = f"😕 Kechirasiz: {message.from_user.full_name} Sizning Balingiz 65 Balldan Kam Bolgani Uchun Yuksalish Maktabida Oqiy Olmaysiz!.\nSizning Ballingiz: <b>{scores[0]}</b>"
                await message.answer(text=text)
                db_manager.delete_user(chat_id=message.chat.id)
    else:
        text = f"❌ Siz Notogri Variant Tanladingiz"
        fann = db_manager.select_question(fan=data["fan"], idsi=data["pagee"])
        await message.answer(text=text, reply_markup=a_b_d)
        if fann:
            for i in fann:
                savol = i[1]
                idsi = i[0]
                a = i[2]
                b = i[3]
                d = i[4]
                true = i[-1]
                textt = f"Savol: {savol}\n\nVariantlar:\nA){a}\nB){b}\nD){d}"
                await message.answer(text=textt, reply_markup=a_b_d)
                await state.update_data({
                    "pagee": int(idsi),
                    "fan": data["fan"],
                    "truesi": true
                })
        else:
            await message.answer(text="😔 Bizda Savollar Hali Mavjud Emas Qayta Urinib Koring!",
                                 reply_markup=user_main_menu)
            db_manager.delete_user(chat_id=message.chat.id)



@dp.message_handler(text="➕ Savol Qoshish")
async def add_question_handler(message: types.Message, state: FSMContext):
    if db_manager.is_admin(chat_id=message.chat.id):
        text = f"😊 Savol Qaysi Fandan Tanlang!"
        await message.answer(text=text, reply_markup=subjects)
    else:
        text = f"😕 Kechirasiz Siz Admin Xuquqiga Ega Emassiz!"
        await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(text="1️⃣ Matematika")
async def math_question_handler(message: types.Message, state: FSMContext):
    if db_manager.is_admin(chat_id=message.chat.id):
        await state.update_data({
            "matematika": dict()
        })
        text = "Savolingizni Kiriting!"
        await message.answer(text=text, reply_markup=cancel)
        await Make_Question.question.set()
    else:
        text = f"😕 Kechirasiz Siz Admin Xuquqiga Ega Emassiz!"
        await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(text=f"2️⃣ Biologiya")
async def biologiya_question_handler(message: types.Message, state: FSMContext):
    if db_manager.is_admin(chat_id=message.chat.id):
        await state.update_data({
            "biologiya": dict()
        })
        text = "Savolingizni Kiriting!"
        await message.answer(text=text, reply_markup=cancel)
        await Make_Question.question.set()
    else:
        text = f"😕 Kechirasiz Siz Admin Xuquqiga Ega Emassiz!"
        await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(text="3️⃣ Ona Tili")
async def ona_tili_question_handler(message: types.Message, state: FSMContext):
    if db_manager.is_admin(chat_id=message.chat.id):
        await state.update_data({
            "ona_tili": dict()
        })
        text = "Savolingizni Kiriting!"
        await message.answer(text=text, reply_markup=cancel)
        await Make_Question.question.set()
    else:
        text = f"😕 Kechirasiz Siz Admin Xuquqiga Ega Emassiz!"
        await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(text="👥 Sinflar")
async def classes_handler(message: types.Message):
    if db_manager.is_admin(chat_id=message.chat.id):
        text = f"Sinflardan Birini Tanlang!"
        await message.answer(text=text, reply_markup=classes)
        await Admin_States.classes.set()
    else:
        text = f"😕 Kechirasiz Siz Admin Xuquqiga Ega Emassiz!"
        await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(text="➕🧑‍🎓 O'quvchi Qoshish")
async def add_student_handler(message: types.Message, state: FSMContext):
    text = f"Yangi Oquvchini Qaysi Sinfga Qoshmoqchisiz Tanlang!"
    await message.answer(text=text, reply_markup=classes)
    await Admin_States.add_setudent.set()

@dp.message_handler(state=Admin_States.add_setudent)
async def add_students_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "class": message.text
    })
    text = f"✍️ Yangi Oquvchini Ism Familyasini Toliq Kiriting!"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await Admin_States.stu_name.set()

@dp.message_handler(state=Admin_States.stu_name)
async def get_student_name(message: types.Message, state: FSMContext):
    text = f"📞 Oquvchini Telefon Raqamini Kiriting!"
    await state.update_data({
        "full_name": message.text
    })
    await message.answer(text=text)
    await Admin_States.stu_phone.set()

@dp.message_handler(state=Admin_States.stu_phone)
async def get_stu_phone(message: types.Message, state: FSMContext):
    text = f"📍 Yangi Oquvchini Yashash Joyini Kiriting!"
    await state.update_data({
        "phone_number": message.text
    })
    await message.answer(text=text)
    await Admin_States.stu_location.set()

@dp.message_handler(state=Admin_States.stu_location)
async def get_stu_location_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "location": message.text
    })
    data = await state.get_data()
    text = f""
    if db_manager.add_student(data=data):
        text = f"O'quvchi {data['class']} Sinfiga Muvaffaqqiyatli Qoshildi"
    else:
        text = f"😔 Kechirasiz Xatolik Yuz Berdi Iltimos Keyinroq Urinib Koring!"
    await message.answer(text=text, reply_markup=admin_panel)
    await state.finish()



@dp.message_handler(state=Admin_States.classes)
async def classes_handler_1(message: types.Message, state: FSMContext):
    # await state.update_data({
    #     "class": message.text
    # })
    # data = await state.get_data()
    classs = db_manager.get_class(class_num=message.text)
    if classs != False:
        son = db_manager.max_son(class_num=message.text)
        text = f"Oquvchilar Soni: {son[0]} Ta\nIsm Familya \t\t\t|Telefon Nomer \t\t\t|Yashash Joy\t\t\t\t|\n"
        for n in classs:
            full_name = n[1]
            tel = n[2]
            location = n[3]
            text += f"""
{full_name} \t|{tel} \t| {location} \n
"""
        await message.answer(text=text, reply_markup=admin_panel)
    else:
        db_manager.create_class(class_num=message.text)
        await message.answer(text=f"Yangi Sinf Qoshildi!")
    await state.finish()

@dp.message_handler(state=Make_Question.question)
async def insert_question(message: types.Message, state: FSMContext):
    text = f"A) Variant Uchun Javob Kiriting!"
    data = await state.get_data()
    fan1 = data.get("matematika")
    fan2 = data.get("biologiya")
    fan3 = data.get("ona_tili")
    if fan1 == {}:
        await state.update_data({
            "matematika": {
                "savol": message.text
            }
        })
    elif fan2 == {}:
        await state.update_data({
            "biologiya": {
                "savol": message.text
            }
        })
    elif fan3 == {}:
        await state.update_data({
            "ona_tili": {
                "savol": message.text
            }
        })
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await Make_Question.a_variant.set()

@dp.message_handler(state=Make_Question.a_variant)
async def a_variant_handler(message: types.Message, state: FSMContext):
    text = f"B) Variant Uchun Javob Kiriting"
    data = await state.get_data()
    fan1 = data.get("matematika")
    fan2 = data.get("biologiya")
    fan3 = data.get("ona_tili")
    if fan1 != None:
        await state.update_data({
            "matematika": {
                "savol": data["matematika"]["savol"],
                "a": message.text
            }
        })
    elif fan2 != {}:
        await state.update_data({
            "biologiya": {
                "savol": data["biologiya"]["savol"],
                "a": message.text
            }
        })
    elif fan3 != {}:
        await state.update_data({
            "ona_tili": {
                "savol": data["ona_tili"]["savol"],
                "a": message.text
            }
          })
    await message.answer(text=text)
    await Make_Question.b_variant.set()


@dp.message_handler(state=Make_Question.b_variant)
async def b_variant_handler(message: types.Message, state: FSMContext):
    text = f"D) Variant Uchun Javob Kiriting"
    data = await state.get_data()
    fan1 = data.get("matematika")
    fan2 = data.get("biologiya")
    fan3 = data.get("ona_tili")
    if fan1 != None:
        await state.update_data({
            "matematika": {
                "savol": data["matematika"]["savol"],
                "a": data["matematika"]["a"],
                "b": message.text
            }
        })
    elif fan2 != None:
        await state.update_data({
            "biologiya": {
                "savol": data["biologiya"]["savol"],
                "a": data["biologiya"]["a"],
                "b": message.text
            }
        })
    elif fan3 != None:
        await state.update_data({
            "ona_tili": {
                "savol": data["ona_tili"]["savol"],
                "a": data["ona_tili"]["a"],
                "b": message.text
            }
        })
    await message.answer(text=text)
    await Make_Question.d_variant.set()

@dp.message_handler(state=Make_Question.d_variant)
async def d_variant_handler(message: types.Message, state: FSMContext):
    text = f"Togri Variantni Tanlang!"
    data = await state.get_data()
    fan1 = data.get("matematika")
    fan2 = data.get("biologiya")
    fan3 = data.get("ona_tili")
    if fan1 != None:
        await state.update_data({
            "matematika": {
                "savol": data["matematika"]["savol"],
                "a": data["matematika"]["a"],
                "b": data["matematika"]["b"],
                "d": message.text
            }
        })
    elif fan2 != None:
        await state.update_data({
            "biologiya": {
                "savol": data["biologiya"]["savol"],
                "a": data["biologiya"]["a"],
                "b": data["biologiya"]["b"],
                "d": message.text
            }
        })
    elif fan3 != None:
        await state.update_data({
            "ona_tili": {
                "savol": data["ona_tili"]["savol"],
                "a": data["ona_tili"]["a"],
                "b": data["ona_tili"]["b"],
                "d": message.text
            }
        })
    await message.answer(text=text, reply_markup=a_b_d)
    await Make_Question.true_variant.set()

@dp.message_handler(state=Make_Question.true_variant)
async def true_variant_handler(message: types.Message, state: FSMContext):
    if message.text in ["A", "B", "D"]:
        data = await state.get_data()
        fan1 = data.get("matematika")
        fan2 = data.get("biologiya")
        fan3 = data.get("ona_tili")
        text = ""
        if fan1 != None:
            await state.update_data({
                "matematika": {
                    "savol": data["matematika"]["savol"],
                    "a": data["matematika"]["a"],
                    "b": data["matematika"]["b"],
                    "d": data["matematika"]["d"],
                    "true": message.text
                }
            })
            dataa = await state.get_data()
            if db_manager.insert_question(data=dataa, fan="matematika"):
                text = f"✅ Testingiz Qo'shildi!"
            else:
                text = "❌ Kechirasiz Xatolik Yuz Berdi Qayta Urinib Koring!"
        elif fan2 != None:
            await state.update_data({
                "biologiya": {
                    "savol": data["biologiya"]["savol"],
                    "a": data["biologiya"]["a"],
                    "b": data["biologiya"]["b"],
                    "d": data["biologiya"]["d"],
                    "true": message.text
                }
            })
            dataa = await state.get_data()
            if db_manager.insert_question(data=dataa, fan="biologiya"):
                text = f"✅ Testingiz Qo'shildi!"
            else:
                text = "❌ Kechirasiz Xatolik Yuz Berdi Qayta Urinib Koring!"
        elif fan3 != None:
            await state.update_data({
                "ona_tili": {
                    "savol": data["ona_tili"]["savol"],
                    "a": data["ona_tili"]["a"],
                    "b": data["ona_tili"]["b"],
                    "d": data["ona_tili"]["d"],
                    "true": message.text
                }
            })
            dataa = await state.get_data()
            if db_manager.insert_question(data=dataa, fan="ona_tili"):
                text = f"✅ Testingiz Qo'shildi!"
            else:
                text = "❌ Kechirasiz Xatolik Yuz Berdi Qayta Urinib Koring!"
        await message.answer(text=text, reply_markup=admin_panel)
        await state.finish()
    else:
        text = f"Tugmalar Orqali Tanlang!"
        await message.answer(text=text, reply_markup=a_b_d)
        await Make_Question.true_variant.set()

@dp.message_handler(text="👤➕ Admin Qoshish")
async def add_admin_handler(message: types.Message, state: FSMContext):
    if db_manager.is_admin(chat_id=message.chat.id):
        text = f"😊 Yangi Adminning CHAT ID Raqamini Kiriting!"
        await message.answer(text=text, reply_markup=cancel)
        await Admin_States.add_admin.set()
    else:
        text = f"😕 Kechirasiz Siz Admin Xuquqiga Ega Emassiz!"
        await message.answer(text=text, reply_markup=user_main_menu)

@dp.message_handler(state=Admin_States.add_admin)
async def add_new_admin_handler(message: types.Message, state: FSMContext):
    try:
        textt1 = f"😊 Yangi Admin Muvaffaqqiyatli Qoshildi!"
        text = f"🥳 Siz Botda Yangi Admin Bo'ldingiz Tabriklaymiz!\nBotga Qayta /start Buyrugini Bering!"
        await dp.bot.send_message(chat_id=int(message.text), text=text, reply_markup=admin_panel)
        db_manager.add_admin(chat_id=int(message.text))
        await message.answer(text=textt1)
        await state.finish()
        return True
    except Exception as exc:
        textt2 = "😕 Kechirasiz Xatolik Yuz Berdi Qayta Urinib Koring!"
        await message.answer(text=textt2, reply_markup=admin_panel)
        await state.finish()
        return False