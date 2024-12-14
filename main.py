from pybit.unified_trading import HTTP, WebSocket
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime

all_instruments = ['10000000AIDOGEUSDT', '1000000BABYDOGEUSDT', '1000000CHEEMSUSDT', '1000000MOGUSDT', '1000000PEIPEIUSDT', '10000COQUSDT', '10000LADYSUSDT', '10000SATSUSDT', '10000WENUSDT', '10000WHYUSDT', '1000APUUSDT', '1000BONKPERP', '1000BONKUSDT', '1000BTTUSDT', '1000CATSUSDT', '1000CATUSDT', '1000FLOKIUSDT', '1000LUNCUSDT', '1000MUMUUSDT', '1000NEIROCTOUSDT', '1000PEPEPERP', '1000PEPEUSDT', '1000RATSUSDT', '1000TOSHIUSDT', '1000TURBOUSDT', '1000XECUSDT', '1000XUSDT', '1CATUSDT', '1INCHUSDT', 'A8USDT', 'AAVEUSDT', 'ACEUSDT', 'ACHUSDT', 'ACTUSDT', 'ACXUSDT', 'ADAUSDT', 'AERGOUSDT', 'AEROUSDT', 'AEVOPERP', 'AEVOUSDT', 'AGIUSDT', 'AGLDUSDT', 'AIOZUSDT', 'AIUSDT', 'AKROUSDT', 'AKTUSDT', 'ALEOUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALTUSDT', 'AMBUSDT', 'ANKRUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARBPERP', 'ARBUSDT', 'ARKMUSDT', 'ARKUSDT', 'ARPAUSDT', 'ARUSDT', 'ASTRUSDT', 'ATAUSDT', 'ATHUSDT', 'ATOMUSDT', 'AUCTIONUSDT', 'AUDIOUSDT', 'AVAILUSDT', 'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT', 'BALUSDT', 'BANANAUSDT', 'BANDUSDT', 'BANUSDT', 'BATUSDT', 'BBUSDT', 'BCHUSDT', 'BEAMUSDT', 'BELUSDT', 'BENDOGUSDT', 'BICOUSDT', 'BIGTIMEUSDT', 'BILLYUSDT', 'BLASTUSDT', 'BLURUSDT', 'BLZUSDT', 'BNBPERP', 'BNBUSDT', 'BNTUSDT', 'BNXUSDT', 'BOBAUSDT', 'BOMEUSDT', 'BONDUSDT', 'BRETTUSDT', 'BSVUSDT', 'BSWUSDT', 'BTC-13DEC24', 'BTC-20DEC24', 'BTC-26SEP25', 'BTC-27DEC24', 'BTC-27JUN25', 'BTC-28FEB25', 'BTC-28MAR25', 'BTC-31JAN25', 'BTCPERP', 'BTCUSDT', 'C98USDT', 'CAKEUSDT', 'CARVUSDT', 'CATIUSDT', 'CELOUSDT', 'CELRUSDT', 'CETUSUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHILLGUYUSDT', 'CHRUSDT', 'CHZUSDT', 'CKBUSDT', 'CLOUDUSDT', 'COMBOUSDT', 'COMPUSDT', 'COOKUSDT', 'COREUSDT', 'COSUSDT', 'COTIUSDT', 'COWUSDT', 'CROUSDT', 'CRVUSDT', 'CTCUSDT', 'CTKUSDT', 'CTSIUSDT', 'CVCUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT', 'DBRUSDT', 'DEEPUSDT', 'DEGENUSDT', 'DENTUSDT', 'DEXEUSDT', 'DGBUSDT', 'DODOUSDT', 'DOGEPERP', 'DOGEUSDT', 'DOGSUSDT', 'DOGUSDT', 'DOP1USDT', 'DOTPERP', 'DOTUSDT', 'DRIFTUSDT', 'DUSKUSDT', 'DYDXUSDT', 'DYMUSDT', 'EDUUSDT', 'EGLDUSDT', 'EIGENUSDT', 'ENAPERP', 'ENAUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCPERP', 'ETCUSDT', 'ETH-13DEC24', 'ETH-20DEC24', 'ETH-26SEP25', 'ETH-27DEC24', 'ETH-27JUN25', 'ETH-28FEB25', 'ETH-28MAR25', 'ETH-31JAN25', 'ETHBTCUSDT', 'ETHFIPERP', 'ETHFIUSDT', 'ETHPERP', 'ETHUSDT', 'ETHWUSDT', 'FBUSDT', 'FDUSDUSDT', 'FIDAUSDT', 'FILUSDT', 'FIOUSDT', 'FIREUSDT', 'FLMUSDT', 'FLOWUSDT', 'FLRUSDT', 'FLUXUSDT', 'FORTHUSDT', 'FOXYUSDT', 'FTMUSDT', 'FTNUSDT', 'FUSDT', 'FWOGUSDT', 'FXSUSDT', 'GALAUSDT', 'GASUSDT', 'GEMSUSDT', 'GLMRUSDT', 'GLMUSDT', 'GMEUSDT', 'GMTUSDT', 'GMXUSDT', 'GNOUSDT', 'GOATUSDT', 'GODSUSDT', 'GOMININGUSDT', 'GRASSUSDT', 'GRTUSDT', 'GTCUSDT', 'GUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT', 'HIPPOUSDT', 'HMSTRUSDT', 'HNTUSDT', 'HOOKUSDT', 'HOTUSDT', 'HPOS10IUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT', 'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IOUSDT', 'JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JTOUSDT', 'JUPUSDT', 'KAIAUSDT', 'KASUSDT', 'KAVAUSDT', 'KDAUSDT', 'KEYUSDT', 'KMNOUSDT', 'KNCUSDT', 'KOMAUSDT', 'KSMUSDT', 'L3USDT', 'LAIUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKPERP', 'LINKUSDT', 'LISTAUSDT', 'LITUSDT', 'LOOKSUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'LUCEUSDT', 'LUMIAUSDT', 'LUNA2USDT', 'MAGICUSDT', 'MAJORUSDT', 'MANAUSDT', 'MANEKIUSDT', 'MANTAUSDT', 'MASAUSDT', 'MASKUSDT', 'MAVIAUSDT', 'MAVUSDT', 'MAXUSDT', 'MBLUSDT', 'MBOXUSDT', 'MDTUSDT', 'MEMEFIUSDT', 'MEMEUSDT', 'MERLUSDT', 'METISUSDT', 'MEUSDT', 'MEWUSDT', 'MINAUSDT', 'MKRUSDT', 'MNTPERP', 'MNTUSDT', 'MOBILEUSDT', 'MOCAUSDT', 'MONUSDT', 'MOODENGUSDT', 'MORPHOUSDT', 'MOTHERUSDT', 'MOVEUSDT', 'MOVRUSDT', 'MTLUSDT', 'MVLUSDT', 'MYRIAUSDT', 'MYROUSDT', 'NEARUSDT', 'NEIROETHUSDT', 'NEOUSDT', 'NFPUSDT', 'NKNUSDT', 'NMRUSDT', 'NOTPERP', 'NOTUSDT', 'NTRNUSDT', 'NULSUSDT', 'NYANUSDT', 'OGNUSDT', 'OGUSDT', 'OLUSDT', 'OMGUSDT', 'OMNIUSDT', 'OMUSDT', 'ONDOPERP', 'ONDOUSDT', 'ONEUSDT', 'ONGUSDT', 'ONTUSDT', 'OPPERP', 'OPUSDT', 'ORBSUSDT', 'ORCAUSDT', 'ORDERUSDT', 'ORDIPERP', 'ORDIUSDT', 'OSMOUSDT', 'OXTUSDT', 'PAXGUSDT', 'PEAQUSDT', 'PENDLEUSDT', 'PENGUSDT', 'PEOPLEUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PIRATEUSDT', 'PIXELUSDT', 'PNUTUSDT', 'POLPERP', 'POLUSDT', 'POLYXUSDT', 'PONKEUSDT', 'POPCATPERP', 'POPCATUSDT', 'PORTALUSDT', 'POWRUSDT', 'PRCLUSDT', 'PRIMEUSDT', 'PROMUSDT', 'PROSUSDT', 'PUFFERUSDT', 'PYRUSDT', 'PYTHUSDT', 'QIUSDT', 'QNTUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RAREUSDT', 'RAYDIUMUSDT', 'RDNTUSDT', 'REEFUSDT', 'RENDERUSDT', 'RENUSDT', 'REQUSDT', 'REZUSDT', 'RIFSOLUSDT', 'RIFUSDT', 'RLCUSDT', 'RONUSDT', 'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RSS3USDT', 'RUNEUSDT', 'RVNUSDT', 'SAFEUSDT', 'SAGAUSDT', 'SANDUSDT', 'SCAUSDT', 'SCRTUSDT', 'SCRUSDT', 'SCUSDT', 'SDUSDT', 'SEIUSDT', 'SFPUSDT', 'SHIB1000PERP', 'SHIB1000USDT', 'SILLYUSDT', 'SKLUSDT', 'SLERFUSDT', 'SLFUSDT', 'SLPUSDT', 'SNTUSDT', 'SNXUSDT', 'SOL-13DEC24', 'SOL-20DEC24', 'SOL-27DEC24', 'SOL-31JAN25', 'SOLPERP', 'SOLUSDT', 'SPECUSDT', 'SPELLUSDT', 'SPXUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT', 'STPTUSDT', 'STRKPERP', 'STRKUSDT', 'STXUSDT', 'SUIPERP', 'SUIUSDT', 'SUNDOGUSDT', 'SUNUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SWEATUSDT', 'SWELLUSDT', 'SXPUSDT', 'SYNUSDT', 'SYSUSDT', 'TAIKOUSDT', 'TAIUSDT', 'TAOUSDT', 'THETAUSDT', 'THEUSDT', 'TIAPERP', 'TIAUSDT', 'TLMUSDT', 'TNSRUSDT', 'TOKENUSDT', 'TONPERP', 'TONUSDT', 'TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TWTUSDT', 'UMAUSDT', 'UNIUSDT', 'USDCUSDT', 'USDEUSDT', 'USTCUSDT', 'UXLINKUSDT', 'VANRYUSDT', 'VELOUSDT', 'VETUSDT', 'VIDTUSDT', 'VIRTUALUSDT', 'VOXELUSDT', 'VRAUSDT', 'VTHOUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WIFPERP', 'WIFUSDT', 'WLDPERP', 'WLDUSDT', 'WOOUSDT', 'WUSDT', 'XAIUSDT', 'XCHUSDT', 'XCNUSDT', 'XEMUSDT', 'XIONUSDT', 'XLMPERP', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT', 'XRDUSDT', 'XRPPERP', 'XRPUSDT', 'XTZUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT', 'YGGUSDT', 'ZBCNUSDT', 'ZECUSDT', 'ZENUSDT', 'ZETAUSDT', 'ZEUSUSDT', 'ZILUSDT', 'ZKJUSDT', 'ZKUSDT']


session = HTTP(
    demo=True,
    api_key="wwMOhb398inGsW39iL",
    api_secret="4yFNtazBdvGDspv30t5D6qKEVxF1orLbNMKR",
)
# Store the previously fetched message (to compare)
previous_message = ""
URL = "https://t.me/s/whalepumpgroup23"
# URL = "https://t.me/s/rian_ru"


# Function to get the latest message
def get_last_message():
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    messages = soup.find_all("div", class_="tgme_widget_message_text")
    last_message = messages[len(messages) - 1].text
    return last_message

def place_order(coin_name, position_type, tp_value, sl_value):
    price = session.get_kline(category="linear", symbol=coin_name, interval=1, limit=1)['result']['list'][0][1]
    qty = 1000 / float(price)

    print(qty)

    qtyStep = session.get_instruments_info(category="linear", symbol=coin_name, )['result']['list'][0]['lotSizeFilter']['qtyStep']

    print(qtyStep)

    # Round the divided value to the nearest multiple of qtyStep
    valid_qty = round(float(qty) / float(qtyStep)) * float(qtyStep)
    # Format the result to avoid floating-point precision issues
    valid_qty = float(f"{valid_qty:.10f}")
    print(f"Valid quantity: {valid_qty}")

    side = ""
    if position_type.upper() == "LONG":
        side = "Buy"
    else:
        side = "Sell"

    print(session.place_order(
        category="linear",
        symbol=coin_name,
        side=side,
        orderType="market",
        qty=str(valid_qty),
        takeProfit=tp_value,
        # takeProfit="2.220",
        stopLoss=sl_value
        # stopLoss="2.180"
    ))


while True:
    try:
        current_message = get_last_message()

        if current_message != previous_message:

            # Regular expression to search for SHORT or LONG
            pattern_one = r'\b(SHORT|LONG)\b'

            # Regular expression to check for words ending with .p or .P
            pattern_two = r'\b\w+\.p\b|\b\w+\.P\b'

            # Regular expression to extract the value after "TP1:" or "Take Profit 1:"
            pattern_three = r'(?:TP1:|Take Profit 1:)\s*([\d.]+)'

            # Regular expression to extract the value after "TP1:" or "Take Profit 1:"
            pattern_four = r'(?:SL:|Stop Loss:)\s*([\d.]+)'

            # Search for the pattern
            match_one = re.search(pattern_one, current_message, re.IGNORECASE)

            if match_one:
                position_type = match_one.group(1).upper()
                print(f"Position: {position_type}")

                # Search for the pattern
                match_two = re.search(pattern_two, current_message)

                if match_two:
                    word = match_two.group()
                    coin_name = word[:len(word) - 2]
                    print(f"Coin: {coin_name}")

                    if coin_name.upper() in all_instruments:

                        # Search for the pattern
                        tp_value = re.search(pattern_three, current_message, re.IGNORECASE).group(1)
                        sl_value = re.search(pattern_four, current_message, re.IGNORECASE).group(1)

                        print(f"TP: {tp_value}")
                        print(f"SL: {sl_value}")

                        place_order(coin_name, position_type, tp_value, sl_value)

                    else:
                        print("not found in the list")

                else:
                    print("No word ending with .p or .P found.")

            else:
                print("No position type found.")

            print("New message: ", current_message)
            previous_message = current_message

        # Sleep for a few seconds before checking again
        time.sleep(30)
        print("...check...")

    except Exception as e:
        print("Error occurred:", e)
        break

# print(all_instruments[0])
# x = "btcUSDT".upper()
# if x in all_instruments:
#     print("yes")
# else:
#     print("no")

# response = session.get_instruments_info(category="linear")
#
# instruments = response.get("result")['list']
# # print(instruments['list'])
# # Extract the instrument names
# instrument_names = [instrument['symbol'] for instrument in instruments]
# print(instrument_names)

# print(session.get_server_time())



# Convert server time (Unix timestamp) to a readable format
# server_time_unix = session.get_server_time() / 1000  # Convert milliseconds to seconds
# server_time_readable = datetime.utcfromtimestamp(server_time_unix)
#
# print(f"Readable Server Time: {server_time_readable}")






