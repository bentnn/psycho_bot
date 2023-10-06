import asyncio

from app import session, PSYCHO_SITE_REST_URL, normal_test_name_to_technical, proxy_server
from aiogram.utils.markdown import text, hbold, hitalic
from aiogram.types import ParseMode
from app.keyboards import tests_keyboard, help_kb


async def send_psycho_site_request(method, url, return_json=True, raise_if_not_ok=False, **kwargs):
    async with session.request(method=method, url=f'{PSYCHO_SITE_REST_URL}/{url}', proxy=proxy_server, **kwargs) as response:
        if not response.ok:
            if raise_if_not_ok and response.status != 404:
                raise RuntimeError(f'Failed to send {method} to psycho site (URl={url}): {await response.text()}')
            return_value = None
        else:
            return_value = (await response.json()) if return_json else None
        return response.status, return_value


async def run_cocos_in_loop(*coros):
    results = []
    for coro in coros:
        res = await coro
        if isinstance(coro, asyncio.Task):
            results.append(coro.result())
        else:
            results.append(res)
    return results


async def start_test(bot, from_user_id, test_info):
    await bot.send_message(
            chat_id=from_user_id,
            text=text(hbold(f'Тест `{test_info["name"]}`'), hitalic(test_info['info'] + '\n'),
                      test_info["instruction"], sep='\n'),
            parse_mode=ParseMode.HTML
        )
    await bot.send_message(
            chat_id=from_user_id, text=test_info["questions"][0],
            reply_markup=tests_keyboard[normal_test_name_to_technical[test_info["name"]]]
    )


async def send_help_msg(bot, chat_id):
    await bot.send_message(chat_id=chat_id,
                           text='Прошу прощения, оказалось, что вы не зарегистрированы на сайте.\n'
                                'Нажмите на кнопку help для получения инструкции',
                           reply_markup=help_kb)
