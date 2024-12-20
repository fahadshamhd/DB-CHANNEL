import re
from os import environ
from pymongo import MongoClient, errors
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, ChannelInvalid, UsernameInvalid, UsernameNotModified
import asyncio

#    """Handle the /start command."""
@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    await message.reply("Bot is in work!")


@Client.on_message(filters.private)  # Filters only private messages
def handle_message(client, message):
    user_text = message.text.strip() if message.text else ""

    if user_text.startswith("/"):  # Ignore commands starting with "/"
        return
    else:
        message.reply_text("Bot is in work!")
