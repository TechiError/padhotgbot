# Idea By @ProgrammingError
# Made By @ProgrammingError
# Thanks To Google😂😂😂

import io
import logging
import random
import sys
import traceback

import redis
import requests
from decouple import config
from telethon import Button, TelegramClient, events

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
REDIS_URI = config("REDIS_URI", default=None)
REDIS_PASS = config("REDIS_PASS", default=None)
SUDOS = config("SUDOS", default=None)
APIS = config("APIS", default=None)

tgbot = TelegramClient("Botzhub", APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

try:
    redis_info = REDIS_URI.split(":")
    ud = redis.StrictRedis(
        host=redis_info[0],
        port=redis_info[1],
        password=REDIS_PASS,
        charset="utf-8",
        decode_responses=True,
    )
except BaseException:
    pass

apis = APIS.split(" ")

SEARCH_ENGINE_IDS = ["d99e58572df67b77a", "c1b78ad46b86b5213"]


print("Successfully deployed!")
print(f"Your Bot is now running! 🥳🥳🥳")
print("Enjoy! Do join @BotzHub 🥺👉👈")


@tgbot.on(
    events.NewMessage(incoming=True, pattern="/start", func=lambda e: e.is_private)
)
async def start(event):
    await event.reply(
        "Hello!\nI am a bot to search answers for your questions.\nUse me Inline\n\nPlease Join @BotzHub 🥺👉👈",
        buttons=[[Button.switch_inline("Search Answer", query="", same_peer=True)]],
    )


@tgbot.on(
    events.NewMessage(incoming=True, pattern="/stats", func=lambda e: e.is_private)
)
async def start(event):
    x = ud.get("USERS")
    y = x.split(" ")
    count = 0
    for xx in y:
        count += 1
    sudo = SUDOS.split(" ")
    if str(event.sender_id) in sudo:
        await event.reply(f"The Total Number of users is {count}")


@tgbot.on(
    events.NewMessage(incoming=True, pattern="/destroydb", func=lambda e: e.is_private)
)
async def destroy(event):
    sudo = SUDOS.split(" ")
    if str(event.sender_id) in sudo:
        try:
            ud.delete("USERS")
            await event.reply("Destroyed DataBase successfully!")
        except:
            await event.reply(traceback.print_exc(file=sys.stdout))


@tgbot.on(
    events.NewMessage(incoming=True, pattern="/users", func=lambda e: e.is_private)
)
async def users(e):
    x = ud.get("USERS")
    y = x.split(" ")
    users_list = "List Of Total Users In Bot. \n\n"
    for xx in y:
        try:
            fname = (await tgbot.get_entity(int(xx))).first_name
        except ValueError:
            fname = "User"
        name = f"[{fname}](tg://user?id={xx})"
        users_list += f"=> Name: {name}| ID: {xx}\n"
    sudo = SUDOS.split(" ")
    if str(e.sender_id) in sudo:
        if len(users_list) < 4096:
            await e.reply(users_list)
        else:
            with io.BytesIO(str.encode(users_list)) as tedt_file:
                tedt_file.name = "userlist.txt"
                await tgbot.send_file(
                    e.chat_id,
                    tedt_file,
                    force_document=True,
                    caption="Total Users In Your Bot.",
                    allow_cache=False,
                )


@tgbot.on(events.NewMessage(incoming=True))
async def add(event):
    x = ud.get("USERS")
    if x:
        y = x.split(" ")
        for xx in y:
            if str(event.sender_id) not in y:
                ud.set("USERS", x + " " + str(event.sender_id))
            else:
                pass
    else:
        ud.set("USERS", str(SUDOS))


@tgbot.on(events.InlineQuery(pattern=r"(.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    API_KEY = random.choice(apis)
    SEARCH_ENGINE_ID = random.choice(SEARCH_ENGINE_IDS)
    query = event.text
    try:
        x = ud.get("USERS")
        if x:
            y = x.split(" ")
            for xx in y:
                if str(event.query.user_id) not in y:
                    ud.set("USERS", x + " " + str(event.query.user_id))
                else:
                    pass
        else:
            ud.set("USERS", str(SUDOS))

        padhai = []

        if query:
            programmingerror = f"https://customsearch.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&start=1&key={API_KEY}"
            shivambro = requests.get(programmingerror).json()
            search_items = shivambro.get("items")
            if search_items is not None:
                for search_item in search_items:
                    title = search_item.get("title")
                    # Idea By @ProgrammingError
                    # Made By @ProgrammingError
                    # Thanks To Google😂😂😂# https://www.googleapis.com/customsearch/v1?key=AIzaSyAyDBsY3WRtB5YPC6aB_w8JAy6ZdXNc6FU&cx=d99e58572df67b77a&q=vector
                    danish_00 = search_item.get("link")
                    atul_xd = search_item.get("snippet")
                    # Idea By @ProgrammingError
                    # Made By @ProgrammingError
                    # Thanks To Google😂😂😂
                    toppers = f"{title}\n\nAnswer in Short:\n\n{atul_xd}"
                    padho = f"{title}"
                    padhai.append(
                        await event.builder.article(
                            title=padho,
                            description=f"{atul_xd}",  # Idea By @ProgrammingError
                            # Made By @ProgrammingError
                            # Thanks To Google😂😂😂
                            text=toppers,
                            buttons=[
                                [Button.url("Answer", f"{danish_00}")],
                                [
                                    Button.switch_inline(
                                        "Search Again", query=" ", same_peer=True
                                    )
                                ],
                            ],
                        )
                    )
                await event.answer(padhai)
            else:
                print(shivambro)
        else:
            padhai.append(
                await event.builder.article(
                    title="Give Something to search.",
                    description="Please write some queries to Search Answer.",
                    text="Please write some queries to Search Answer.",
                    buttons=[
                        [
                            Button.switch_inline(
                                "Search Again", query=" ", same_peer=True
                            )
                        ],
                    ],
                )
            )
            await event.answer(padhai)
    except:
        traceback.print_exc(file=sys.stdout)


try:
    tgbot.run_until_disconnected()
except:
    traceback.print_exc(file=sys.stdout)
