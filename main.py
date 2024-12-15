from asyncio import run, sleep
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram import types, F, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from admin_functions import *
from message_commands import *
from bot_token import *

dp = Dispatcher()
print('Format of info about users is Full_name:tgID')



#Запуск бота командой /start
@dp.message(Command('start'))
async def start_bot(message: types.Message):
    full_name, user_id, username = message.from_user.full_name, message.from_user.id, message.from_user.username
    await add_user_to_data_base(user_id, full_name, username)
    print(f'{message.from_user.full_name}:{message.from_user.id} started this bot')

    kb = [
        [types.InlineKeyboardButton(text='Меню📖', callback_data='main_menu')], # Меню
        [
        types.InlineKeyboardButton(text='Информация👨‍💻', callback_data='information'), # Инфо
        types.InlineKeyboardButton(text='Список Админов👑', callback_data='list_of_admins') # Список Адм
        ]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
    text_data = f"\n<b>Здравствуйте, {html.escape(message.from_user.full_name)}!</b>\nНиже кнопки которые вам понадобятся\n"
    await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

class Addtask(StatesGroup):
    addtask = State()

class Deltask(StatesGroup):
    deltask = State()

class AdminNews(StatesGroup):
    adm_newsletter = State()
#=====================================================================================# Начало кода основанного на F.Data

# Список админов, когда человек нажал на кнопку 'Список Админов👑'
@dp.callback_query( F.data == 'list_of_admins' )
async def admin_list(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_start")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = 'Список администраторов данного бота:\n1.@Marzkv👑'
    await callback.message.edit_caption(caption=text_data,reply_markup=keyboard)

# Информация о боте, когда человек нажал на кнопку 'Информация👨‍💻'
@dp.callback_query( F.data == 'information' )
async def information(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_start")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = '1. Запуск первой адекватной бета-версии: 13.12.2024\n2. Конец бета-версии 14.12.24'
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

# Возвращение пользователя в начальное меню
@dp.callback_query( F.data == 'back_to_start' )
async def start_bot_2(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text='Меню📖', callback_data='main_menu')], # Меню
        [types.InlineKeyboardButton(text='Информация👨‍💻', callback_data='information'),types.InlineKeyboardButton(text='Список Админов👑', callback_data='list_of_admins')], # Инфо , Список адм
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = f"\n<b>Здравствуйте, {html.escape(callback.from_user.full_name)}!</b>\nНиже кнопки которые вам понадобятся\n"
    await callback.message.edit_caption(caption=text_data,reply_markup=keyboard)

@dp.callback_query( F.data == 'commands_of_bot')
async def cmdlist(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = f'1./add - Добавить задачу.\n2. /list - Список задач.\n3. /complete или /del - Удалить задачу.\n4. /clist - Список выполненных задач.'
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == 'main_menu' )
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    kb = [
        [types.InlineKeyboardButton(text='Вернуться в начало', callback_data='back_to_start'), types.InlineKeyboardButton(text='Команды бота', callback_data='commands_of_bot')],
        [types.InlineKeyboardButton(text='Создать задачу', callback_data='create_task'), types.InlineKeyboardButton(text='Завершить задачу', callback_data='delete_task')],
        [types.InlineKeyboardButton(text='Список ваших задач', callback_data='list_of_active_tasks'), types.InlineKeyboardButton(text='Список завершенных задач', callback_data='list_of_completed_tasks')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = f'Вы находитесь в меню, ниже кнопки для удобной навигации'
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == "list_of_completed_tasks")
async def f_list_of_completed_tasks(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    user_id = callback.from_user.id
    text_data = await list_of_completed_tasks(user_id)
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)


@dp.callback_query( F.data == 'list_of_active_tasks')
async def f_list_of_active_tasks(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    user_id = callback.from_user.id
    tasks = await get_active_task_list(user_id)
    text_data = await get_task_list(tasks)
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == 'create_task')
async def f_add_task(callback: types.CallbackQuery, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = "Введите название задачи которую хотите добавить"
    await callback.message.edit_caption(caption=text_data,reply_markup=keyboard)
    await state.set_state(Addtask.addtask)

@dp.message(Addtask.addtask)
async def f_add_task_step_2(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu'), types.InlineKeyboardButton(text='Список ваших задач', callback_data='list_of_active_tasks')]
    ])
    msg = message.text
    user_id = message.from_user.id
    await add_task_to_database(msg, user_id)
    photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
    text_data = f'Ваша задача <b>"{html.escape(msg)}"</b> была добавлена. Чтобы увидеть список задач нажмите кнопку ниже.'
    await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == 'delete_task')
async def f_del_task(callback: types.CallbackQuery, state: FSMContext):
    kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = "Введите номер задачи которую хотите завершить"
    await callback.message.edit_caption(caption=text_data,reply_markup=keyboard)
    await state.set_state(Deltask.deltask)

@dp.message(Deltask.deltask)
async def f_del_task_step_2(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu'), types.InlineKeyboardButton(text='Список завершенных задач.', callback_data='list_of_completed_tasks')]])
    msg = message.text
    task_id = await isvalid(msg, 'fdelete')
    if task_id:
        user_id = message.from_user.id
        text_data = await mark_task_in_db(task_id, user_id)
        if '/clist' in text_data:
            text_data = text_data[:-7]
            text_data += ". Воспользуйтесь кнопкой ниже"
    elif not task_id:
        text_data = f'Чтобы удалить задачу нужно ввести её номер, вы же ввели: {msg}'
    photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
    await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

#=====================================================================================# Конец кода основанного на F.Data



#=====================================================================================# Начала кода основанного на командах

# Команды в message_commands.py

# Добавление задачи в список задач
@dp.message( Command( 'add' ) )
async def add_task(message: types.Message):
    msg = html.escape(message.text)
    user_id = message.from_user.id
    text_data = await add_task_to_list(msg, user_id)
    await message.answer(text_data)

# Получение списка задач
@dp.message( Command ('list') )
async def get_list(message: types.Message):
    user_id = message.from_user.id
    tasks = await get_active_task_list(user_id)
    text_data = await get_task_list(tasks)
    await message.answer(text=text_data)

# Завершение задачи
@dp.message( Command( 'del' ) )
@dp.message( Command( 'complete' ) )
async def del_task(message: types.Message):
    msg = html.escape(message.text)
    user_id = message.from_user.id
    text_data = await delete_task_from_task_list(msg, user_id)
    await message.answer(text_data)

# Получение списка выполненных задач
@dp.message( Command ('Clist') )
@dp.message( Command ('clist') )
async def get_clist(message: types.Message):
    user_id = message.from_user.id
    text_data = await list_of_completed_tasks(user_id)
    await message.answer(text_data)

#===================================================================================# Конец кода основанного на командах

#===================================================================================# Админ-панель

@dp.message( Command ("admin"))
async def enter_admin_menu(message:types.Message):
    if await isAdmin(message.from_user.id):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Войти в админ меню', callback_data='admin_menu')]])
        photo_data, text_data = 'AgACAgIAAxkBAAIDQGddvnuopuYcJgHfzNGmBDCHFO2ZAAJH5zEbz43oStTOu4SkTrHEAQADAgADeQADNgQ', 'Войти в Админ-меню'
        await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Команды бота', callback_data='commands_of_bot')]])
        text_data = await wrong_admin(message.from_user.id, message.text, message.from_user.username)
        photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
        await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == 'admin_menu')
async def administration_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if await isAdmin(callback.from_user.id):
        kb = [[types.InlineKeyboardButton(text='Статистика', callback_data='admin_stats'), types.InlineKeyboardButton(text='Рассылка', callback_data='admin_news')]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        text_data = f'Здравствуйте, администратор <b>{html.escape(callback.from_user.full_name)}</b>.'
        await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == 'admin_stats')
async def administration_statistics(callback: types.CallbackQuery):
    if await isAdmin(callback.from_user.id):
        kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='admin_menu')]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.edit_caption(caption=await get_admin_statistics(), reply_markup=keyboard)

@dp.callback_query( F.data == 'admin_news')
async def admin_newsletter(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if await isAdmin(callback.from_user.id):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=([[types.InlineKeyboardButton(text='Вернуться назад', callback_data='admin_menu')]]))
        await state.set_state(AdminNews.adm_newsletter)
        await callback.message.edit_caption(caption='Введите сообщения для всеобщей рассылки',reply_markup=keyboard)

@dp.message(AdminNews.adm_newsletter)
async def admin_newsletter_step2(message: types.Message, state: FSMContext):
    await state.clear()
    if await isAdmin(message.from_user.id):
        good_try = 0
        all_ids = await get_all_users_id()
        for user_id in all_ids:
            try:
                await message.send_copy(user_id[0])
                good_try += 1
                await sleep(0.1)
            except:
                continue
        user_count = len(all_ids)
        await message.answer(f'Рассылка завершена.\nВсего пользователей: {user_count}.\nУдалось отправить: {good_try}.\nНе удалось отправить: {user_count - good_try}.')

#===================================================================================# Конец админ-панели

# Если была введена неверная команда.
@dp.message(F.text[0] == '/')
async def wrong_command(message: types.Message):
    msg = message.text
    kb = [[types.InlineKeyboardButton(text='Команды бота', callback_data='commands_of_bot')]]
    text_data = f'Введенной вами команды "{msg}" - не существует\nНажав на кнопку ниже вы увидете доступные команды'
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
    await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

# Запуск бота
async def main():
    print('Введите пароль от бота')
    token_of_bot = await get_token(input())
    bot = Bot(token=token_of_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # API бота
    await dp.start_polling(bot)
if __name__ == "__main__":
    run( main() )