from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

import keyboards as kb
from states import Reg

user = Router()


@user.message(CommandStart  ())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в бот\n\nВведите ваше имя!",
                         reply_markup=ReplyKeyboardRemove())

    await state.set_state(Reg.name)


@user.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Теперь отправьте ваш номер телефона!',
                         reply_markup=kb.get_number)
    await state.set_state(Reg.phone)


@user.message(Reg.phone, F.contact)
async def reg_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)

    data = await state.get_data()
    await message.answer(f'Вы успешно зарегистрировались!\n\nИмя: {data["name"]}\nНомер: {data["phone"]}',
                         reply_markup=kb.menu)
    await state.clear()


@user.message(Reg.phone)
async def reg_contact_incorrect(message: Message):
    await message.answer('Отправьте контакт по кнопке ниже!')


@user.message(F.text == "Каталог")
async def cmd_text(message: Message):
    await message.answer('Выберите категорию товара',
                         reply_markup=kb.catalog)


@user.callback_query(F.data.startswith("brand_"))
async def check_brand(callback: CallbackQuery):
    brand_name = callback.data.split('_')[1]
    await callback.answer(f'Вы выбрали {brand_name.capitalize()}!!', show_alert=True)
    await callback.message.answer(f'Вы выбрали {brand_name.capitalize()}!')


@user.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)