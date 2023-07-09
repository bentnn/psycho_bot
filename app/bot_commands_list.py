from aiogram.types import BotCommand


bot_commands = [
    BotCommand(command="/start", description="Информация о боте"),
    BotCommand(command="/run_test", description="Пройти тест"),
    BotCommand(command="/stats", description="Посмотреть статистику по тестам"),
    BotCommand(command="/check_id", description="Проверить связку бота и профиля на сайте"),
    BotCommand(command="/rm_id", description="Отвязать бота от аккаунта"),
]
