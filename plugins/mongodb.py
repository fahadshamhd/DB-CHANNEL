from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
from info import *
import asyncio

CHANNEL_ID = "@FsTesy"  # Your Telegram channel username or ID

# MongoDB Configuration
MONGO_URI = "mongodb+srv://fsbotz:fsbotztg@fsbotz.s3jw7.mongodb.net/?retryWrites=true&w=majority&appName=FsBotz"
DB_NAME = "fsbotz"
COLLECTION_NAME = "Telegram_files"

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
movies_collection = db[COLLECTION_NAME]

# Global control variables
cancel_process = False
skip_files = False

@app.on_message(filters.command("sendmovies"))
async def send_movies(client, message):
    global cancel_process, skip_files
    cancel_process = False  # Reset cancel flag
    skip_files = False      # Reset skip flag

    movies = list(movies_collection.find())
    if not movies:
        await client.send_message(message.chat.id, "No movies found in the database.")
        return

    # Notify user about the process start with cancel and skip buttons
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_process"),
            InlineKeyboardButton("⏭ Skip Files", callback_data="skip_files")
        ]]
    )
    status_message = await client.send_message(
        message.chat.id,
        f"Starting to send {len(movies)} movies to the channel...",
        reply_markup=keyboard
    )

    for index, movie in enumerate(movies, start=1):
        if cancel_process:
            await status_message.edit_text("❌ Process canceled by the user.")
            return

        if skip_files:
            continue  # Skip the file and move to the next one

        file_id = movie.get("file_id")
        file_name = movie.get("file_name", "Unknown File Name")
        file_size = movie.get("file_size", "Unknown Size")
        caption = movie.get("caption", "No caption provided.")

        # Format file size for readability
        file_size_mb = round(file_size / (1024 * 1024), 2) if isinstance(file_size, int) else file_size

        # Create the message
        movie_message = f"🎬 **{file_name}**\n📦 Size: {file_size_mb} MB\n\n{caption}"

        # Send the file to the channel
        try:
            await client.send_document(
                chat_id=CHANNEL_ID,
                document=file_id,
                caption=movie_message
            )
        except Exception as e:
            if "FloodWait" in str(e):
                # Extract flood wait time
                delay = int(str(e).split("FloodWait:")[1].split(" ")[1])
                await client.send_message(
                    message.chat.id,
                    f"⏳ Flood wait detected. Waiting for {delay} seconds..."
                )
                await asyncio.sleep(delay)  # Wait for the flood wait time
                continue  # Retry the same file
            else:
                # Handle other errors gracefully and notify the user
                await client.send_message(message.chat.id, f"Error sending file {file_name}: {e}")
                continue

        # Update status in the user chat
        await status_message.edit_text(
            f"Sent {index}/{len(movies)} movies to the channel...",
            reply_markup=keyboard
        )

    # Notify completion
    await status_message.edit_text("✅ All movies have been sent successfully!")


@app.on_callback_query()
async def handle_callbacks(client, callback_query):
    global cancel_process, skip_files

    if callback_query.data == "cancel_process":
        cancel_process = True
        await callback_query.message.edit_text("❌ Process canceled by the user.")
        await callback_query.answer("Process canceled!")

    elif callback_query.data == "skip_files":
        skip_files = True
        await callback_query.answer("Skipping remaining files!")