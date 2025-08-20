# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
datr=wQ6maOGvef6jcDLkyr_TjaLd; 
ds_user_id=75861865943; 
csrftoken=pUOj0gtMsVITbYMPNrzQHVA4Mhib3QxX; 
ig_did=00E2FF1D-F3C9-40DC-9D87-7B9F4EF842FE; 
mid=aKYOwQABAAHm4vKbz9PMc1M97NOI; 
sessionid=75861865943%3ABka7r4v7ISODro%3A26%3AAYdMOur-fyoxwEX8vSZ4ZSiQBMNMvPlekVrG7q4aQg; 
rur="CLN\05475861865943\0541787249374:01fe44537cae11a4a86780fe7779407034112b7974d3523d5dfe0371b91261a9da277ad4"
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "21303916"))
API_HASH = getenv("API_HASH", "a95f38df3dc1f71b6497798a40b993ab")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6197171929").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://jackend44:1CamIKdwrLDXuhns@cluster0.nlnbwph.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002588585383")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002439642259"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "100"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "shrinkforearn.in")
AD_API = getenv("AD_API", "f673ecd2aa19a3013eadbd35bb85cdc61d6e6ed3")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
