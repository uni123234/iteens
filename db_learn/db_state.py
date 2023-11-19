from aiogram.fsm.state import State, StatesGroup


class FSMRegister(StatesGroup):
    first_name = State()
    last_name = State()
    lng_lvl = State()
