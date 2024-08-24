"""
This module defines state management classes for the finite state machine (FSM) 
used in the application. 

It includes different states for various processes:
- Registration process
- Translation process
- Testing process
- ABC test process
"""

from aiogram.fsm.state import State, StatesGroup


class FSMRegister(StatesGroup):
    """
    States for the registration process.
    """
    first_name = State()
    last_name = State()
    lng_lvl = State()


class FSMTranslate(StatesGroup):
    """
    State for the translation process.
    """
    text = State()


class FSMTest(StatesGroup):
    """
    States for the testing process.
    """
    translation = State()
    phrase = State()


class FSMABCTest(StatesGroup):
    """
    States for the ABC test process.
    """
    start_of_test = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()
    q14 = State()
    q15 = State()
    q16 = State()
    q17 = State()
    q18 = State()
    q19 = State()
    q20 = State()
    q21 = State()
    q22 = State()
    q23 = State()
    q24 = State()
    q25 = State()
    q26 = State()
    final_q = State()
