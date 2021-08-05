import logging
import os
import sys
import time
import spamwatch
from pyrogram import Client, errors
import telegram.ext as tg
from telethon import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Python_ARQ import ARQ
from redis import StrictRedis
import aiohttp
from aiohttp import ClientSession

StartTime = time.time()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get('INFOPIC', False))
    EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get('API_ID', None)
    ARQ_API = os.environ.get("ARQ_API", None)
    API_HASH = os.environ.get('API_HASH', None)
    DB_URI = os.environ.get('DATABASE_URL')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    REDIS_URL = os.environ.get('REDIS_URL')
  
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', True))
    WORKERS = int(os.environ.get('WORKERS', 8))
   
               
    GBAN_GIF = os.environ.get('GBAN_GIF',
                                 'https://telegra.ph/file/d36fee143a7d8152ab430.mp4')
    BAN_GIF = os.environ.get('BAN_GIF',
                                 'https://telegra.ph/file/9ca94d0bb6dab523ac0f0.mp4')
    UNGBAN_GIF = os.environ.get('UNGBAN_GIF',
                                 'https://telegra.ph/file/032d57f93e8d352270790.mp4')
    KICKME_STICKER = os.environ.get('KICKME_STICKER','CAACAgUAAxkBAAIqs2EMF_Cxa7cpoZ88I1rOoGcfyjb_AAJ-AwACX_wQVOdMZBOFAngRIAQ')



    TEST_STICKER = os.environ.get('TEST_STICKER', '')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    AI_API_KEY = os.environ.get('AI_API_KEY', None)
    WALL_API = os.environ.get('WALL_API', None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get('SPAMWATCH_SUPPORT_CHAT', None)
    SPAMWATCH_API = os.environ.get('SPAMWATCH_API', None)
    BOT_ID = 1412878118
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ARQ_API_URL = "TheARQ.Tech"

    try:
        BL_CHATS = set(int(x) for x in os.environ.get('BL_CHATS', "").split())
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

else:
    from SaitamaRobot.config import Development as Config
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
   

    GBAN_GIF = Config.GBAN_GIF
    TEST_STICKER = Config.TEST_STICKER
    
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    KICKME_STICKER = Config.KICKME_STICKER
    BAN_GIF= Config.BAN_GIF
    UNGBAN_GIF= Config.UNGBAN_GIF
  
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    INFOPIC = Config.INFOPIC

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("Your redis server is now alive!")

except BaseException:

    raise Exception("Your redis server is not alive, please check again.")

finally:

   REDIS.ping()

   LOGGER.info("Your redis server is now alive!")

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config.")
else:
    sw = spamwatch.Client(SPAMWATCH_API)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("Pain", API_ID, API_HASH)
pbot = Client("PainPyro", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
mongo_client = MongoClient(MONGO_DB_URI)
aiohttpsession = ClientSession()
arq = ARQ(ARQ_API, ARQ_API_URL, aiohttpsession)
db = mongo_client.SaitamaRobot
dispatcher = updater.dispatcher

DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from SaitamaRobot.modules.helper_funcs.handlers import (CustomCommandHandler,
                                                        CustomMessageHandler,
                                                        CustomRegexHandler)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
