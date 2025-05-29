from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import asyncio
import requests
import json
from config import BOT_TOKEN, OPENROUTER_API_KEY

bot = Bot(token=BOT_TOKEN, default=types.BotDefault(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

async def get_qwen_response(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "qwen/qwen3-30b-a3b:free",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "Ошибка: нет ответа от модели.")

@dp.message()
async def handle_message(message: Message):
    await message.answer("⏳ Подожди, думаю...")
    reply = await asyncio.to_thread(get_qwen_response, message.text)
    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())