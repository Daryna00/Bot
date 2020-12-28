from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode

from config import TOKEN
import requests


####

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import TestStates

from json import dump, load
import keyboards as kb

HOLIDAY_TOKEN = '2a5b2f8affc54233ed8a933772dee40f'
QUOTE_URL = 'https://favqs.com/api/qotd'


# Создание бота по токену
bot = Bot(token=TOKEN)
# dispatcherz
# dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
###############

@dp.message_handler(commands=["start"])
async def in1(message: types.Message):
    await message.reply('Чем я могу вам помочь?', reply_markup=kb.payment)


@dp.callback_query_handler(lambda c: c.data == 'button_1')
async def payment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Если у вас не проходит платеж, пожалуйста обратитесь в ваш банк.\n\n'
                                                        'Если вам не пришел счет или сам пресет посмотрите сообщение на вашей почте в спаме.\n\n'
                                                        'В другом случае обратитесь через сайт или через этого бота с заявкой и мы рассмотрим ее в ближайшее время!')

@dp.callback_query_handler(lambda c: c.data == 'button_2')
async def payment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Пресеты в Лайтруме значительно упрощают обработку фотографий.\n\n'
                                                        ' Комплекс настроек можно применить как к отдельно взятому изображению,'
                                                        ' так и для нескольких десятков фотографий.\n\n Для того чтобы воспользоваться'
                                                        ' пресетами нужно находиться в рабочей области Develop.\n\n Слева от изображений'
                                                        ' в списке функций нужно открыть вкладку «Presets».\n\n Выберите из нескольких настроек'
                                                        ' нужный пресет и кликните на него левой кнопкой мыши.\n\n Изменения сразу отобразятся на фотографии.')

@dp.callback_query_handler(lambda c: c.data == 'button_3')
async def payment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Заказать пресет вы можете через "Стол заказов" в вашем лично кабинете '
                                                        'или в данном боте введите "/order" и оставте ваши данные мы с вами свяжимся в ближайшее время.')


@dp.callback_query_handler(lambda c: c.data == 'button_5')
async def payment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           'Мы рады что вас заинтересовал данный раздел, на данном этапе'
                           ' мы открыты ко всем предложениям если вы фотограф прошу написать в раздел вопросов'
                           ' свое предложение, если же вы из фирмы или имеете более коммерческое предложение'
                           ' прошу оставить свои данные в этом боте "/order" и мы ответим как можно быстрее.')


@dp.callback_query_handler(lambda c: c.data == 'button_4')
async def payment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           'Для получения бесплатного пресета зарегестрируйтесь на сайте!')



@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply('Буду рад помочь!')
    await bot.send_message(message.from_user.id, """
Доступные команды:
/start,
/help,
/quote
    """)


@dp.message_handler(state="*", commands=["setstate"])
async def process_setstate(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    return await message.reply('Состояние успешно сброшено')

def file_fill(user_id, data=None):
    print(data)
    if not data:
        data = {
            "Имя": "",
            "e-mail": "",
            "Организация": "",
        }
    with open(f'user_data/{user_id}.json', 'w', encoding='utf-8') as file:
        dump(data, file)

@dp.message_handler(state="*", commands=["order"])
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[0])
    await message.reply('Остевте ваши данные для дальнейшей связи с нами.', reply=False)
    await message.reply('Напишите Ваше имя!', reply=False)
    file_fill(message.from_user.id)

def change_user_file(user_id, field, content: str):
    with open(f'user_data/{user_id}.json', 'r', encoding='utf-8') as file:
        data = load(file)
    data[field] = content.encode('utf-8').decode('utf-8')
    file_fill(user_id, data=data)


@dp.message_handler(state=TestStates.TEST_STATE_0)
async def state0(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    change_user_file(message.from_user.id, 'Имя', message.text)
    await message.reply('Спасибо!', reply=False)
    await message.reply('Напишите Ваш e-mail!', reply=False)
    await state.set_state(TestStates.all()[1])

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def state1(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    change_user_file(message.from_user.id, 'e-mail', message.text)
    await message.reply('Спасибо!', reply=False)
    await message.reply('Напишите свою организацию!', reply=False)
    await state.set_state(TestStates.all()[2])


@dp.message_handler(state=TestStates.TEST_STATE_2)
async def state2(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    change_user_file(message.from_user.id, 'Организация', message.text)
    await message.reply('Спасибо!', reply=False)
    await message.reply('Опрос окончен', reply=False)
    return await state.reset_state()


@dp.message_handler(commands=["quote"])
async def quote(message: types.Message):
    await message.reply('Узнайте цитату этого дня.', reply_markup=kb.inline_kb2)

@dp.callback_query_handler(lambda c: c.data.startswith('quote'))
async def inline_kb2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    data = requests.get(url=QUOTE_URL)
    print(data.json())
    quote = data.json()['quote']['body']
    author = data.json()['quote']['author']
    await bot.send_message(callback_query.from_user.id, f' {quote} \n  {author} \n Цитата дня!')

# echo
@dp.message_handler()
async def echo(message: types.Message):
    msg_text = message.text
    await bot.send_message(message.from_user.id, message.text)
    # print(message)


# stickers, photos and other
@dp.message_handler(content_types=ContentType.ANY)
async def any_format(message: types.Message):
    msgtext = text(emojize("Я не знаю, что с этим делать :astonished:"),
                    italic('Я просто напомню, что есть'),
                    code('команда'), "/help"
                                )
    await bot.send_message(message.from_user.id, msgtext, parse_mode=ParseMode.MARKDOWN)
#
if __name__ == '__main__':
    executor.start_polling(dp)