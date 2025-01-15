from pyrogram import Client
from pymongo import MongoClient
from info import *
import asyncio

CHANNEL_ID = "@FsTesy"    # Your Telegram channel username or ID

# MongoDB Configuration
MONGO_URI = "mongodb+srv://fsbotz:fsbotztg@fsbotz.s3jw7.mongodb.net/?retryWrites=true&w=majority&appName=FsBotz")  # Replace with your MongoDB URI
DB_NAME = "fsbotz"                # Replace with your database name
COLLECTION_NAME = "Telegram_files"                # Replace with your collection name

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
movies_collection = db[COLLECTION_NAME]

@Client.on_message()
async def send_movies(client, message):
    if message.text.lower() == "/sendmovies":
        movies = list(movies_collection.find())
        if not movies:
            await client.send_message(message.chat.id, "No movies found in the database.")
            return
        
        # Notify user about the process start
        status_message = await client.send_message(message.chat.id, f"Starting to send {len(movies)} movies to the channel...")

        for index, movie in enumerate(movies, start=1):
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
                # Handle errors gracefully and notify the user
                await client.send_message(message.chat.id, f"Error sending file {file_name}: {e}")
                continue

            # Update status in the user chat
            await status_message.edit_text(f"Sent {index}/{len(movies)} movies to the channel...")

            # Add a 1-second delay
            await asyncio.sleep(1)

        # Notify completion
        await status_message.edit_text("✅ All movies have been sent successfully!")