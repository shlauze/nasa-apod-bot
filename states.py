import logging

# pyrefly: ignore [missing-import]
from aiogram.fsm.state import State, StatesGroup


class ApodStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_birthday = State()
