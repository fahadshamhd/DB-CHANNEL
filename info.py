import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'FsBotz')
API_ID = int("17432758")
API_HASH = "c9e31fda0ce722e3f3033a9d4f140783"
BOT_TOKEN = environ.get('BOT_TOKEN', "7585998373:AAHH2L5DFj9ay5MQC4eENZUvKiIrdck-4Dk")


# This Pictures Is For Start Message Picture, You Can Add Multiple By Giving One Space Between Each.
PICS = (environ.get('PICS' ,'https://graph.org/file/9bc905986578fe468ced6.jpg https://graph.org/file/7230540148a6f704552de.jpg https://graph.org/file/1ef334e3cdfa368fae986.jpg https://graph.org/file/b9ffdf56741dcc5c508a7.jpg https://graph.org/file/a4bef533b0ee8815fc2cb.jpg https://graph.org/file/f11a9552706c0b490682f.jpg https://graph.org/file/2df3277be246d91205b4b.jpg https://graph.org/file/c5cbda8edb3f87c3c2639.jpg https://graph.org/file/a4ac39bb700ad227b090f.jpg https://graph.org/file/1aadf3219407df6a5aa4d.jpg https://graph.org/file/375fe73f23f6c6c099e80.jpg https://graph.org/file/10b80b514219cbded6e9e.jpg https://graph.org/file/a291f637768262bd52f5e.jpg')).split() #SAMPLE PIC


# Admins & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6666362904').split()] # For Multiple Id Use One Space Between Each.
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]  # For Multiple Id Use One Space Between Each.
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

# This Channel Is For When User Start Your Bot Then Bot Send That User Name And Id In This Log Channel, Same For Group Also.
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002113738933'))



# This Is Force Subscribe Channel, also known as Auth Channel 
auth_channel = environ.get('AUTH_CHANNEL', '-1002125899790') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# This Channel Is For When User Request File With command or hashtag like - /request or #request
reqst_channel = environ.get('REQST_CHANNEL_ID', '-1002283920177')
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None

# This Is Your Bot Support Group Id , Here Bot Will Not Give File Because This Is Support Group.
support_chat_id = environ.get('SUPPORT_CHAT_ID', '-1002034052245')
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None


# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://fsbotz:fsbotztg@fsbotz.s3jw7.mongodb.net/?retryWrites=true&w=majority&appName=FsBotz") 
DATABASE_NAME = environ.get('DATABASE_NAME', "fsbotz")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')


# Links
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/+Q3fLrCvhJ-Q3MjU1')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/ott_movies_here')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'Fs_Botz') # Support Chat Link Without https:// or @
OWNER_LNK = environ.get('OWNER_LNK', 'https://t.me/firossha')

# Start Command Reactions
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"] #don't add any emoji because tg not support all emoji reactions



