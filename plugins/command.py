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


