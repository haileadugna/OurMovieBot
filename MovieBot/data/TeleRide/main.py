import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

TOKEN = "6515566757:AAGx1pPPz5qJCTi2xZ_eDxYmceqRMdPQdwU"

form_router = Router()


class Form(StatesGroup):
    name = State()
    ask_phone = State()
    drive_passenger = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        "Hi there! Welcome to TurboTwist! What's your name?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

# 1. Ask for name
# 2. Ask for to share there phone number
# 3. Ask for if they are registering as a driver or passenger
# 4. then return the summary of the information


@form_router.message(Form.name)
async def ask_phone_number(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.ask_phone)
    await message.answer(
        f"Nice to meet you, {html.quote(message.text)}!\nPlease share your phone number with me.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Share phone", request_contact=True),
                ],
                [
                    KeyboardButton(text="Cancel"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.drive_passenger)
    await message.answer(
        f"Thanks for your Input, {html.quote(message.text)}!\nAre you registering as a driver or passenger?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Driver"),
                    KeyboardButton(text="Passenger"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


# @form_router.message(Form.drive_passenger, F.text.casefold() == "no")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#     data = await state.get_data()
#     await state.clear()
#     await message.answer(
#         "Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await show_summary(message=message, data=data, positive=False)


@form_router.message(Form.drive_passenger)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.drive_passenger)

    await message.reply(
        # now returning the whole registration data
        "Thanks for your Input, {html.quote(message.text)}!\nAre you registering as a driver or passenger?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.like_bots)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("I don't understand you :(")


@form_router.message(Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(language=message.text)
    await state.clear()

    if message.text.casefold() == "python":
        await message.reply(
            "Python, you say? That's the language that makes my circuits light up! 😉"
        )

    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())