import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict
from data.movieApi import get_movies_by_genre

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
    InputMediaPhoto,
)
# Action, Comedy, Drama, Horror, Romance, Sci-Fi, Thriller
TOKEN = "6735935500:AAEsxVeWPu9qjveLOS8WZt0JINbrcXTNtZ4"

form_router = Router()

class Form(StatesGroup):
    name = State()
    like_genre = State()
    # language = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        "Hi there! What's your name?",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.like_genre)
    await message.answer(
        f"Nice to meet you, {html.quote(message.text)}!\nWhich kind of movies are your favorite?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    # keyboard buttons of the genre
                    KeyboardButton(text="Action"),
                    KeyboardButton(text="Comedy"),
                    KeyboardButton(text="Drama"),
                ],
            
                [
                    KeyboardButton(text="Romance"),
                    KeyboardButton(text="Sci-Fi"),
                    KeyboardButton(text="Thriller"),
                ],
            ],
            resize_keyboard=True,
        ),
    )

# year chosen

@form_router.message(Form.like_genre )
async def process_like_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    # call for api to get the movies by genre

    # Call the API function
    movies_data = get_movies_by_genre( message.text)
    print(movies_data)
    if movies_data:
        filtered = [movie['id'] for movie in movies_data['results']]
        images_link = [movie['primaryImage']['url'] for movie in movies_data['results'] if movie['primaryImage'] is not None]
        
        # Process the movies_data, you can send it as a response to the user, for example:
        await message.answer(f"Here are some drama movies: {' '.join(filtered[:200])}")
        
        # Send images in a media group
        media = [InputMediaPhoto(media=link) for link in images_link]
        await message.answer_media_group(media=media)
        
        # Return the images link along with filtered movie IDs
        return filtered, images_link
    else:
        await message.answer("Sorry, something went wrong with the movie API.")
    # await state.finish()
    
    


# @form_router.message(CommandStart())
# async def command_start(message: Message, state: FSMContext) -> None:
#     genre = "Romance"
    
#     # Call the API function
#     movies_data = get_movies_by_genre( genre)
    
#     # Handle the API response as needed
#     if movies_data:
#         filtered = [movie['id'] for movie in movies_data['results']]
#         images_link = [movie['primaryImage']['url'] for movie in movies_data['results'] if movie['primaryImage'] is not None]
        
#         # Process the movies_data, you can send it as a response to the user, for example:
#         await message.answer(f"Here are some drama movies: {' '.join(filtered[:200])}")
        
#         # Send images in a media group
#         media = [InputMediaPhoto(media=link) for link in images_link]
#         await message.answer_media_group(media=media)
        
#         # Return the images link along with filtered movie IDs
#         return filtered, images_link
#     else:
#         await message.answer("Sorry, something went wrong with the movie API.")
    






async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())