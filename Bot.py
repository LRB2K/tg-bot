import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Bot token (Replace with your bot token)
TOKEN = "7673544377:AAE3BA3mVEP8wIdhhuW3KV9-tBvk_8mdxac"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# User data storage
users = {}
waiting_users = []
active_chats = {}

def get_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Start Chat"),
        KeyboardButton("Stop Chat"),
        KeyboardButton("Switch Chat")
    )

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    users[message.from_user.id] = {'gender': None, 'chatting_with': None}
    await message.answer("Welcome! Use the buttons below to start chatting.", reply_markup=get_keyboard())

@dp.message_handler(lambda message: message.text == "Start Chat")
async def start_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_chats:
        await message.answer("You're already in a chat. Type 'Stop Chat' to leave.")
        return
    
    if waiting_users:
        partner_id = waiting_users.pop(0)
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id
        await bot.send_message(partner_id, "You are now connected! Say hi!")
        await message.answer("You are now connected! Say hi!")
    else:
        waiting_users.append(user_id)
        await message.answer("Waiting for a partner...")

@dp.message_handler(lambda message: message.text == "Stop Chat")
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        del active_chats[user_id]
        del active_chats[partner_id]
        await bot.send_message(partner_id, "Your partner has disconnected.")
        await message.answer("Chat ended.")
    elif user_id in waiting_users:
        waiting_users.remove(user_id)
        await message.answer("You left the queue.")
    else:
        await message.answer("You're not in a chat.")

@dp.message_handler()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        await bot.send_message(partner_id, message.text)
    else:
        await message.answer("You're not in a chat. Type 'Start Chat' to find a partner.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
