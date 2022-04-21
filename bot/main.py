import asyncio
import logging
from datetime import datetime, timedelta

import aiohttp_jinja2
import jinja2
from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from aiogram.utils import executor
from aiogram.utils.exceptions import ChatNotFound
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from config import ENDPOINT, dp
from web_app import safe_parse_webapp_init_data

logging.basicConfig(level=logging.ERROR)

SEND_MESSAGE_DELTA = {}  # Prevent flood by `Send Message Function`


# /web-start
async def web_start(request):
    return await aiohttp_jinja2.render_template_async('start/start.html', request, {})


# /checkUserData
async def web_check_user_data(request: Request):
    data = await request.post()
    data = safe_parse_webapp_init_data(dp.bot._token, data["_auth"])
    return json_response({"ok": True, "user": data.as_json()})


# /sendMessage
async def web_send_message(request: Request):
    data = await request.post()

    try:
        web_app_data = safe_parse_webapp_init_data(token=dp.bot._token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "error": "Unauthorized"}, status=401)

    web_app_user_id = web_app_data["user"]["id"]

    if web_app_user_id not in SEND_MESSAGE_DELTA:
        SEND_MESSAGE_DELTA.update({web_app_user_id: datetime.utcnow() - timedelta(seconds=100)})

    delta = SEND_MESSAGE_DELTA.get(web_app_user_id)

    if (datetime.utcnow() - delta) < timedelta(seconds=5):
        return json_response({"ok": False, "error": "🥶 You are to fast. Please wait for 5 seconds"})

    user_id, text = data.get("user_id"), data.get("text")

    if user_id is None or not text:
        return json_response({"ok": False, "error": "💁‍♂️ UserID and Text inputs required"})

    try:
        SEND_MESSAGE_DELTA.update({web_app_user_id: datetime.utcnow()})
        await dp.bot.send_message(chat_id=user_id, text=text)

    except ChatNotFound:
        return json_response({"ok": False, "error": "Chat Not Found"})

    except Exception as exc:
        print(exc)
        return json_response({"ok": False, "error": "Exception caused"})

    else:
        return json_response({"ok": True})


app = web.Application()
app.add_routes([web.get('/web-start', web_start),
                web.post('/sendMessage', web_send_message),
                web.post('/checkUserData', web_check_user_data)])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('web'), enable_async=True)


async def on_startup(dps: Dispatcher):
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host="0.0.0.0", port=45678))  # WARN: Don't do this in production!


async def on_shutdown(dps: Dispatcher):
    await dps.storage.close()
    await dps.storage.wait_closed()


@dp.message_handler(CommandStart())
@dp.throttled(rate=2)
async def cmd_start(msg: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😎 WEB APP", web_app=WebAppInfo(url=f"{ENDPOINT}/web-start"))]
    ])
    await msg.reply("TEST WEB APP", reply_markup=keyboard)


def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    main()
