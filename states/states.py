from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    full_name = State()
    phone_number = State()
    location = State()

class Make_Question(StatesGroup):
    question = State()
    a_variant = State()
    b_variant = State()
    d_variant = State()
    true_variant = State()

class Admin_States(StatesGroup):
    add_admin = State()
    add_class = State()
    classes = State()
    add_setudent = State()
    stu_name = State()
    stu_phone = State()
    stu_location = State()
