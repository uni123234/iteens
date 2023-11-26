from aiogram.fsm.state import State, StatesGroup


class FSMRegister(StatesGroup):
    first_name = State()
    last_name = State()
    lng_lvl = State()


class FSMTranslate(StatesGroup):
    text = State()


class FSMTest(StatesGroup):
    translation = State()
    phrase = State()


class FSMTestABC(StatesGroup):
    question = State()
    tu = State()

