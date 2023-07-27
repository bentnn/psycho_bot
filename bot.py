from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from app.base_funcs import send_psycho_site_request, run_cocos_in_loop
from aiogram.dispatcher import FSMContext
import asyncio
import app
from aiogram.utils.markdown import text, hbold, hitalic
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.start_and_stop import startup, shutdown
from app.keyboards import *
from app.states import *
from app.db.save_msgs_midlware import SaveMessagesMiddleware
import app.const as const

bot = Bot(token=app.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(SaveMessagesMiddleware())


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state, state_data = await asyncio.gather(
        state.get_state(),
        state.get_data()
    )
    tasks_to_remove_msgs = [asyncio.create_task(bot.delete_message(chat_id=message.chat.id, message_id=msg_id))
                            for msg_id in state_data.get('remove_msgs', [])]
    if current_state is None:
        await message.answer('Нечего завершать', reply_markup=keyboard_remove)
    else:
        await asyncio.gather(
            message.answer('Завершено', reply_markup=keyboard_remove),
            state.finish()
        )
    if tasks_to_remove_msgs:
        await asyncio.wait(tasks_to_remove_msgs)


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(message: types.Message):
    await message.answer('Привет! Этот бот позволяет проходить тесты для сайта psycho_test из telegram.\n'
                         'Здесь можно проходить тесты и отслеживать свои результаты', reply_markup=keyboard_remove)
    await message.answer('Для активации бота вам необходимо зарегистрироваться/авторизоваться на сайте, '
                         'перейти в профиль и ввести ID вашего telegram аккаунта в специальную графу')
    await message.answer('Ваш ID:')
    await message.answer(message.from_user.id)
    await message.answer('Ссылка на сайт:')
    await message.answer(app.PSYCHO_SITE_URL)


@dp.message_handler(commands=['check_id'])
async def process_check_id_command(message: types.Message):
    (status, response), _send_message = await asyncio.gather(
        send_psycho_site_request('GET', f'telegramid/{message.from_user.id}'),
        message.answer('Проверяю информацию...', reply_markup=keyboard_remove)
    )
    if status == 200:
        await message.answer(f'Вы привязаны к сайту:\nUsername: {response["username"]}\n'
                             f'Имя: {response["first_name"] or "-"}\nФамилия: {response["last_name"] or "-"}')
    else:
        await message.answer('Ваш ID не привязан к сайту')


@dp.message_handler(commands=['manage_account'])
async def process_manage_account_command(message: types.Message):
    await asyncio.gather(
        ManageAccount.method.set(),
        message.answer('Подскажите, какой вариант управления вам интересен', reply_markup=manage_account_kb)
    )
    # await asyncio.gather(
    #     message.reply("Подскажите, вы уверены?\n"
    #                   "Для повторного подключения необходимо будет зайти на сайт и ввести ваш ID на странице профиля",
    #                   reply_markup=are_you_sure_rm_id_keyboard),
    #     RecoverAccount.are_you_sure.set()
    # )


@dp.message_handler(lambda message: message.text not in const.manage_account_methods,
                    state=ManageAccount.method)
async def process_manage_account_choose_method_incorrect_command(message: types.Message, state: FSMContext):
    await message.answer('Не могу разобрать ваш ответ, выберите, пожалуйста, один из предложенных вариантов',
                         reply_markup=manage_account_kb)


@dp.message_handler(state=ManageAccount.method)
async def process_manage_account_choose_method_correct_command(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(lambda message: message.text not in {'Да, отвязать профиль', 'Нет, не нужно'},
                    state=ManageAccount.are_you_sure)
async def process_rm_id_incorrect(message: types.Message, state: FSMContext):
    await message.answer('Не могу разобрать ваш ответ, выберите, пожалуйста, один из предложенных вариантов',
                         reply_markup=are_you_sure_rm_id_keyboard)


@dp.message_handler(state=ManageAccount.are_you_sure)
async def process_rm_id_correct(message: types.Message, state: FSMContext):
    finish_state_task = asyncio.create_task(state.finish())
    if message.text == 'Да, отвязать профиль':
        _send_message, (status, response) = await asyncio.gather(
            message.answer('Хорошо, удаляю привязку...', reply_markup=keyboard_remove),
            send_psycho_site_request('delete', f'telegramid/{message.from_user.id}', return_json=False)
        )
        if status == 200:
            await message.answer('Привязка вашего ID и сайта успешно удалена')
        elif status == 404:
            await message.answer('Ваш ID не был привязан к аккаунту на сайте, удаление не потребовалось')
        else:
            await message.answer(f'Произошла ошибка, сервис вернул статус {status}\n'
                                 f'прошу прощения за неудобство, администратору уже уведомлен о случившемся')
    else:
        await message.answer('Хорошо, отменяю удаление', reply_markup=keyboard_remove)
    await finish_state_task


@dp.message_handler(commands=['run_test'])
async def process_run_test_command(message: types.Message):
    set_state_task = asyncio.create_task(RunningTest.test_name.set())
    # kb = InlineKeyboardMarkup()
    # for test_name, info in app.psycho_tests.items():
    #     kb.add(InlineKeyboardButton(info['name'], callback_data=test_name))
    # kb.add(InlineKeyboardButton('cancel', callback_data='cancel'))
    msg = await message.answer('Список тестов:', reply_markup=choose_test_kb)
    msg2 = await message.answer('Выберите  тест из списка', reply_markup=only_cancel_keyboard)
    await set_state_task
    await dp.get_current().current_state().update_data(remove_msgs=[msg.message_id, msg2.message_id])
    # await message.answer(f'Выберите тест из списка:', reply_markup=only_cancel_keyboard)
    # msgs = await asyncio.gather(
    #     *(message.answer(text(bold(info['name']), info['info'], sep='\n'),
    #                      reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Выбрать',
    #                                                                                   callback_data=test_name)),
    #                      parse_mode=ParseMode.MARKDOWN
    #                      ) for test_name, info in app.psycho_tests.items()
    #       )
    # )
    # await set_state_task
    # await dp.get_current().current_state().update_data(remove_msgs=[i.message_id for i in msgs])


@dp.callback_query_handler(state=RunningTest.test_name)
async def process_callback_choose_test(callback_query: types.CallbackQuery, state: FSMContext):
    test_info = app.psycho_tests[callback_query.data]
    msgs_task = asyncio.create_task(
        run_cocos_in_loop(
            bot.send_message(
                chat_id=callback_query.from_user.id,
                text=text(hbold(f'Тест `{test_info["name"]}`'), hitalic(test_info['info'] + '\n'),
                          test_info["instruction"], sep='\n'),
                parse_mode=ParseMode.HTML
            ),
            bot.send_message(
                chat_id=callback_query.from_user.id, text=test_info["questions"][0],
                reply_markup=tests_keyboard[callback_query.data]
            )
        )
    )
    state_data = await state.get_data()
    await asyncio.gather(
        *(
            bot.delete_message(chat_id=callback_query.from_user.id, message_id=msg_id)
            for msg_id in state_data.get('remove_msgs', [])
        ),
        state.update_data(remove_msgs=[], test_name=callback_query.data, last_question_number=0),
        callback_query.answer('Тест ' + test_info["name"]),
        # bot.send_message(chat_id=callback_query.from_user.id,
        #                  text=text(hbold(f'Тест `{test_info["name"]}`'), hitalic(test_info['info'] + '\n'), test_info["instruction"], sep='\n'),
        #                  # text=f'Тест `{test_info["name"]}`\n{test_info["instruction"]}',
        #                  parse_mode=ParseMode.HTML),
        RunningTest.next(),
        msgs_task
    )
    # await bot.send_message(chat_id=callback_query.from_user.id,
    #                        text=test_info["questions"][0],
    #                        reply_markup=tests_keyboard[callback_query.data])


@dp.message_handler(lambda message: message.text != 'cancel', state=RunningTest.next_answer)
async def process_test_answer_command(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    test_info = app.psycho_tests[state_data['test_name']]
    if message.text not in test_info['answers']:
        await message.answer('Не понимаю ответа')
    else:
        this_question_number = state_data['last_question_number'] + 1
        answers = state_data.get('answers', [])
        answers.append(test_info['answers'][message.text])
        if this_question_number == len(test_info['questions']):
            # TODO: доделать
            *_, (status, res) = await asyncio.gather(
                state.finish(),
                message.answer('Завершено, подождите, пожалуйста, получаю результаты', reply_markup=keyboard_remove),
                send_psycho_site_request('post', f'passtest/{message.from_user.id}/{state_data["test_name"]}',
                                         json=answers)
            )
            await message.answer(res)
        else:
            await asyncio.gather(
                state.update_data(answers=answers),
                state.update_data(last_question_number=this_question_number),
                message.answer(test_info['questions'][this_question_number])
            )


@dp.message_handler(commands=['stats'])
async def process_stats_command(message: types.Message):
    await asyncio.gather(
        message.answer('По какому тесту выгрузить статистику?', reply_markup=all_tests_keyboard),
        GetStats.test_name.set()
    )


@dp.message_handler(lambda message: message.text in app.normal_test_name_to_technical or message.text == 'all',
                    state=GetStats.test_name)
async def process_stats_correct(message: types.Message, state: FSMContext):
    test_name = app.normal_test_name_to_technical[message.text] if message.text != 'all' else 'all'
    (status, stats), *_ = await asyncio.gather(
        send_psycho_site_request('GET', f'stats/{message.from_user.id}/{test_name}',
                                 return_json=True, raise_if_not_ok=True),
        state.finish(),
        message.answer('Пожалуйста, подождите, выгружаю статистику...', reply_markup=keyboard_remove)
    )
    await asyncio.gather(
        *(message.answer(hitalic(test_name) + '\n\n' + '\n\n'.join(hbold(date) + '\n' + msg for date, msg in test_stats.items()),
                         parse_mode=ParseMode.HTML)
          for test_name, test_stats in stats.items())
    )


@dp.message_handler(lambda message: message.text not in app.normal_test_name_to_technical and
                    message.text not in {'all', 'cancel'},
                    state=GetStats.test_name)
async def process_stats_incorrect(message: types.Message):
    await message.answer('Не могу разобрать ответ\nПожалуйста, выберите название теста из списка',
                         reply_markup=all_tests_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
