from aiogram.dispatcher.filters.state import State, StatesGroup


class RmID(StatesGroup):
    are_you_sure = State()


class RunningTest(StatesGroup):
    test_name = State()
    next_answer = State()
    answers = []
    test = None
