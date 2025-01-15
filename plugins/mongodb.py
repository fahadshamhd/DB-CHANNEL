from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
from pyrogram.errors import FloodWait 
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
skip_count = 0  # Default skip count

@Client.on_message(filters.command("setskip"))
async def set_skip(client, message):
    """
    Command to set the number of files to skip before starting the send process.
    """
    global skip_count
    try:
        # Extract the skip count from the message
        skip_count = int(message.text.split(" ")[1])
        await message.reply_text(f"✅ Skip count set to {skip_count} files.")
    except (IndexError, ValueError):
        await message.reply_text("❌ Invalid format! Use `/setskip <number>` (e.g., `/setskip 5`).")

@Client.on_message(filters.command("sendmovies"))
async def send_movies(client, message):
    global cancel_process, skip_count
    cancel_process = False  # Reset cancel flag
    failed_count = 0  # Counter for failed sends
    skipped_count = 0  # Counter for skipped duplicate files
    sent_file_ids = set()  # Set to track sent file IDs

    movies = list(movies_collection.find())
    if not movies:
        await client.send_message(message.chat.id, "No movies found in the database.")
        return

    # Notify user about the process start with cancel button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Cancel", callback_data="cancel_process")]]
    )
    status_message = await client.send_message(
        message.chat.id,
        f"Starting to send {len(movies)} movies to the channel after skipping {skip_count} files...",
        reply_markup=keyboard
    )

    # Apply the skip count
    movies_to_send = movies[skip_count:] if skip_count < len(movies) else []

    for index, movie in enumerate(movies_to_send, start=1):
        if cancel_process:
            await status_message.edit_text(
                f"❌ Process canceled by the user.\nFailed sends: {failed_count}\nSkipped duplicates: {skipped_count}"
            )
            return

        file_id = movie.get("file_id")
        file_name = movie.get("file_name", "Unknown File Name")
        file_size = movie.get("file_size", "Unknown Size")
        caption = movie.get("caption", "No caption provided.")

        # Skip duplicate files
        if file_id in sent_file_ids:
            skipped_count += 1
            continue

        # Format file size for readability
        file_size_mb = round(file_size / (1024 * 1024), 2) if isinstance(file_size, int) else file_size

        # Create the message
        movie_message = f"🎬 **{file_name}**\n📦 Size: {file_size_mb} MB\n\n{caption}"

        sent_successfully = False

        while not sent_successfully:
            try:
                # Send the file to the channel
                await client.send_document(
                    chat_id=CHANNEL_ID,
                    document=file_id,
                    caption=movie_message
                )
                sent_file_ids.add(file_id)  # Track sent file ID
                sent_successfully = True
            except FloodWait as e:
                # Handle flood wait error
                delay = e.value
                err_message = await client.send_message(
                    message.chat.id,
                    f"⏳ Flood wait detected. Waiting for {delay} seconds..."
                )
                await asyncio.sleep(delay)  # Wait for the flood wait time
                await err_message.delete()  # Delete the flood wait message
            except Exception as e:
                # Log the error and increment failed count
                logging.error(f"Error sending file {file_name}: {e}")
                failed_count += 1
                sent_successfully = True  # Break the loop even on other errors

        # Update status in the user chat
        await status_message.edit_text(
            f"Sent {index}/{len(movies_to_send)} movies to the channel...\nFailed sends: {failed_count}\nSkipped duplicates: {skipped_count}",
            reply_markup=keyboard
        )

    # Notify completion
    await status_message.edit_text(
        f"✅ All movies have been sent successfully!\nFailed sends: {failed_count}\nSkipped duplicates: {skipped_count}"
    )

@Client.on_callback_query()
async def handle_callbacks(client, callback_query):
    global cancel_process

    if callback_query.data == "cancel_process":
        cancel_process = True
        await callback_query.message.edit_text(
            f"❌ Process canceled by the user."
        )
        await callback_query.answer("Process canceled!")