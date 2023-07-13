import requests
import logging
import base64
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOTKEY
import random

ammasso_coordinate = [(44.192984, 10.703535), (44.230757, 10.682370), (44.286048, 10.813874), (44.647134, 10.905563),
                      (44.629139, 10.908367), (44.631198, 10.929938)]

aiuto = "QUESTA E' LA LISTA DEI COMANDI DEL BOT\n\n"\
        "/pic {id_utente}: scarica foto dato un ID_utente\n\n" \
        "/info: scarica le informazioni relative ad un microcontrollore di cui si è in possesso\n\n" \
        "/create {nome utente} {email utente}: inserisce nel database un nuovo utente con chat_id\n\n" \
        "/statup {id micro} {stato}: aggiorna stato di un microcontrollore\n\n" \
        "/addmicro: aggiunge un micro associandolo ad un utente in base al chat ID"


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

updater = None

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(aiuto)

def add_micro(update, context):
    chatid = update.effective_chat.id
    existing_user = False
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    updater.bot.send_message(chat_id=chatid, text=response.status_code)
    utente = None
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if str(chatid) == str(dic["chat_id"]):
                utente = int(dic["id"])
                existing_user = True
    if not existing_user:
        updater.bot.send_message(chat_id=chatid, text="No account associated with this chat_id")
    else:
        numero = random.randint(0, 5)
        pillolone = {
            "lat": ammasso_coordinate[numero][0],
            "long": ammasso_coordinate[numero][1],
            "status": "false",
            "chat_id": utente
        }
        response = requests.post(f"https://insects_api-1-q3217764.deta.app/microcontroller/add/", pillolone)
        updater.bot.send_message(chat_id=chatid, text=response.status_code)

def status_update(update, context):
    receivedmessage = update.message.text
    receivedmessage = str(receivedmessage).split()
    id_micro = int(receivedmessage[1])

    pillolone = {
        "status": str(receivedmessage[2])
    }
    #pillolone_di_jasone = json.dumps(pillolone)
    response = requests.patch(f"https://insects_api-1-q3217764.deta.app/microcontroller/update_status/{id_micro}", pillolone)
    update.message.reply_text(response.status_code)

def ciataidi(update, context):
    chatid = update.effective_chat.id
    updater.bot.send_message(chat_id=chatid, text=chatid)

def crea(update, context):
    receivedmessage = update.message.text
    chatid = update.effective_chat.id
    receivedmessage = str(receivedmessage).split()
    pillolone = {
        "name": receivedmessage[1],
        "email": receivedmessage[2],
        "chat_id": str(chatid)
    }
    #pillolone_di_jasone = json.dumps(pillolone)
    print(pillolone)
    response = requests.post(f"https://insects_api-1-q3217764.deta.app/user/add/", json=pillolone)
    update.message.reply_text(response.status_code)

def info(update, context):
    chatid = update.effective_chat.id
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    updater.bot.send_message(chat_id=chatid, text=response.status_code)
    utente = None
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if str(chatid) == str(dic["chat_id"]):
                utente = str(dic["id"])

        response = requests.get(f"https://insects_api-1-q3217764.deta.app/microcontrollers/user/{utente}")
        updater.bot.send_message(chat_id=chatid, text=response.status_code)
        if response.status_code == 200:
            data = response.json()
            for dic in data:
                message = "id micro: " + str(dic["id"]) + "\n"
                message += "lat: " + str(dic["lat"]) + "\n"
                message += "long: " + str(dic["long"]) + "\n"
                message += "status: " + str(dic["status"])
                updater.bot.send_message(chat_id=chatid, text=message)
        else:
            update.message.reply_text('Failed to extract data')

def pics(update, context):
    hacker = True
    receivedmessage = update.message.text
    receivedmessage = str(receivedmessage).split()
    chatid = update.effective_chat.id
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    updater.bot.send_message(chat_id=chatid, text=response.status_code)
    utente = None
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if str(chatid) == str(dic["chat_id"]):
                utente = str(dic["id"])
        response = requests.get(f"https://insects_api-1-q3217764.deta.app/microcontrollers/user/{utente}")
        updater.bot.send_message(chat_id=chatid, text=response.status_code)
        if response.status_code == 200:
            data = response.json()
            for dic in data:
                if str(dic["id"]) == receivedmessage[1]:
                    hacker = False
    if hacker:
        updater.bot.send_message(chat_id=chatid, text="YOU SHALL NOT PASS")
    else:
        response = requests.get(f"https://insects_api-1-q3217764.deta.app/images/microcontroller/{receivedmessage[1]}")
        if response.status_code == 200:
            data = response.json()
            for dic in data:
                message = "id foto: " + str(dic["id"]) + "\n"
                message += "datetime: " + str(dic["datetime"]) + "\n"
                message += "specie: " + str(dic["species"])
                update.message.reply_text(message)
                image_bytes = base64.b64decode(dic["binaryimage"])
                context.bot.send_photo(chat_id=chatid, photo=image_bytes)
        else:
            update.message.reply_text(response.status_code)
            update.message.reply_text('Failed to extract data')


def main():

    global updater
    updater = Updater(token=BOTKEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("pic", pics))
    dp.add_handler(CommandHandler("addmicro", add_micro))
    dp.add_handler(CommandHandler("create", crea))
    dp.add_handler(CommandHandler("statup", status_update))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ciataidi))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

