import requests
import logging
import pandas as pd
import numpy as np
import base64
from sklearn.neighbors import NearestNeighbors
from math import radians, sin, cos, sqrt, atan2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOTKEY

API_URL_GET_USERS = "https://insects_api-1-q3217764.deta.app/users/"
API_URL_GET_MICROCONTROLLERS = "https://insects_api-1-q3217764.deta.app/microcontrollers/"
API_URL_GET_IMAGES = "https://insects_api-1-q3217764.deta.app/images/"
API_URL_ADD_USER = "https://insects_api-1-q3217764.deta.app/user/add/"


ammasso_coordinate = [(44.192984, 10.703535), (44.230757, 10.682370), (44.286048, 10.813874), (44.647134, 10.905563),
                      (44.629139, 10.908367), (44.631198, 10.929938)]

aiuto = "LISTA DEI COMANDI DEL BOT\n\n"\
        "/info: scarica le informazioni relative ad un microcontrollore di cui si è in possesso\n\n" \
        "/pic {id_micro}: scarica foto dato un ID_utente\n\n" \
        "/create {nome utente} {email utente}: inserisce nel database un nuovo utente con chat_id\n\n" \
        "/statup {id micro} {stato}: aggiorna stato di un microcontrollore\n\n" \
        "/chatid {name} {email}: inserisci il chatID date le proprie credenziali\n\n" \
        "/addmicro {latitudine} {longitudine}: inserimento di un microcontrollore nel database. RICORDARSI " \
        "DI SOSTITUIRE LA VIRGOLA CON IL PUNTO NELLE COORDINATE \n\n" \
        "{coordinate}: permette di sapere se ci sono infestazioni nell'arco di 10 km"\



def ritrieve_table(url):

    response = requests.get(url=url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
            return df
        elif isinstance(data, list):
            df = pd.DataFrame(data)
            return df
    return None


def haversine(point1, point2):
    # Convertire i punti in radianti
    lat1, lon1 = radians(point1[0]), radians(point1[1])
    lat2, lon2 = radians(point2[0]), radians(point2[1])

    # Calcolare la distanza tra i punti
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Ritornare la distanza in metri
    return c * 6371 * 1000


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


def location(update, context):
    chatid = update.effective_chat.id
    lat = update.message.location.latitude
    long = update.message.location.longitude

    # retrieve user table
    user_table = ritrieve_table(API_URL_GET_USERS)

    # retrieve microcontroller tables
    micro_table = ritrieve_table(API_URL_GET_MICROCONTROLLERS)
    micro_table = micro_table.rename(columns={"id": "micro_id", "user_id": "id"})

    # merging tables
    home_table = pd.merge(user_table, micro_table, on='id')

    # drop column
    home_table = home_table.drop(labels=["email", "microcontrollers", "images", "chat_id"], axis=1)

    # rename columns
    home_table = home_table.rename(columns={"id": "user_id"})

    # replace values in status columns
    home_table["status"] = home_table["status"].replace({False: "safe", True: "infested"})

    dataframe = home_table

    dataframe["status"] = dataframe["status"].replace({"safe": False, "infested": True})
    points = []
    labels = []

    new_point = np.array([lat, long])
    new_point = new_point.reshape(1, -1)

    for index, row, in dataframe.iterrows():
        points.append([row["lat"], row["long"]])
        labels.append([row["status"]])

    np_points = np.array(points)
    np_labels = np.array(labels)

    neigh = NearestNeighbors(n_neighbors=len(points), metric=haversine)

    neigh.fit(np_points, np_labels)
    distances, indices = neigh.kneighbors(new_point, return_distance=True)

    # get distances, indices, labels
    distances = distances[0]
    indices = indices[0]
    np_labels = np_labels[indices]

    if np.all(distances > 10000):
        context.bot.send_message(chat_id=chatid, text=f"Distance from the first microcontroller greater than 10 km!")

    for d, i, c, in zip(distances, indices, np_labels):
        if d < 10000 and c == True:
            context.bot.send_message(chat_id=chatid, text=f"Microcontrollers in the area detected infestations!")

        elif d < 10000 and c == True:
            context.bot.send_message(chat_id=chatid, text=f"Microcontrollers in the area do not detect infestations!")


def add_id(update, context):
    chatid = update.effective_chat.id
    receivedmessage = str(update.message.text).split()
    user_name = str(receivedmessage[1])
    user_email = str(receivedmessage[2])
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    context.bot.send_message(chat_id=chatid, text=response.status_code)
    id_user = None
    bandiera = False
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if user_name == str(dic["name"]) and user_email == str(dic["email"]):
                id_user = int(dic["id"])
                bandiera = True
                break

    if bandiera:
        pillolone = {
            "chat_id": chatid
        }
        response = requests.patch(f"https://insects_api-1-q3217764.deta.app/user/update/{id_user}", json=pillolone)
        if response.status_code == 404:
            context.bot.send_message(chat_id=chatid, text=response.status_code)
            context.bot.send_message(chat_id=chatid, text="chatid già associato ad un altro utente")
        elif response.status_code == 200:
            context.bot.send_message(chat_id=chatid, text=response.status_code)
            context.bot.send_message(chat_id=chatid, text="inserimento effettuato correttamente")
    else:
        context.bot.send_message(chat_id=chatid, text="nessun utente associato alle credenziali")


def add_micro(update, context):
    receivedmessage = str(update.message.text).split()
    chatid = update.effective_chat.id
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    updater.bot.send_message(chat_id=chatid, text=response.status_code)
    id_user = None
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if str(chatid) == str(dic["chat_id"]):
                id_user = str(dic["id"])
                break
    else:
        updater.bot.send_message(chat_id=chatid, text=response.status_code)
        updater.bot.send_message(chat_id=chatid, text="no account assiciated to this chatID")

    pillolone = {
        "lat": receivedmessage[1],
        "long": receivedmessage[2],
        "status": True,
        "user_id": int(id_user)
    }
    response = requests.post(f"https://insects_api-1-q3217764.deta.app/microcontroller/add/", json=pillolone)
    if response.status_code == 200:
        updater.bot.send_message(chat_id=chatid, text=response.status_code)
        updater.bot.send_message(chat_id=chatid, text="Inserimento microcontrollore effettuato correttamente")
    else:
        updater.bot.send_message(chat_id=chatid, text=response.status_code)
        updater.bot.send_message(chat_id=chatid, text="qualcosa è andato storto")


def status_update(update, context):
    hacker = True
    chatid = update.effective_chat.id
    receivedmessage = str(update.message.text).split()
    id_micro = int(receivedmessage[1])
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    updater.bot.send_message(chat_id=chatid, text=response.status_code)
    utente = None
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if str(chatid) == str(dic["chat_id"]):
                utente = str(dic["id"])
                break
        response = requests.get(f"https://insects_api-1-q3217764.deta.app/microcontrollers/user/{utente}")
        updater.bot.send_message(chat_id=chatid, text=response.status_code)
        if response.status_code == 200:
            data = response.json()
            for dic in data:
                if str(dic["id"]) == receivedmessage[1]:
                    hacker = False

    if hacker:
        updater.bot.send_message(chat_id=chatid, text="Questo non è il tuo microcontrollore "
                                                      "o il microcontrollore richiesto non esiste")
    else:
        pillolone = {
            "status": str(receivedmessage[2])
        }
        response = requests.patch(f"https://insects_api-1-q3217764.deta.app/microcontroller/update_status/{id_micro}",
                                  json=pillolone)
        update.message.reply_text(response.status_code)
        update.message.reply_text("stato microcontrollore aggiornato")


def ciataidi(update, context):
    chatid = update.effective_chat.id
    updater.bot.send_message(chat_id=chatid, text=chatid)


def crea(update, context):
    chatid = update.effective_chat.id
    receivedmessage = str(update.message.text).split()
    pillolone = {
        "name": receivedmessage[1],
        "email": receivedmessage[2],
        "chat_id": str(chatid)
    }
    # pillolone_di_jasone = json.dumps(pillolone)
    print(pillolone)
    response = requests.post(f"https://insects_api-1-q3217764.deta.app/user/add/", json=pillolone)
    if response.status_code == 200:
        update.message.reply_text(response.status_code)
        update.message.reply_text("Utente creato correttamente")
    elif response.status_code == 500:
        update.message.reply_text(response.status_code)
        update.message.reply_text("Username occupato")



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
            update.message.reply_text('No MC associated to your account')


def pics(update, context):
    hacker = True
    receivedmessage = str(update.message.text).split()
    chatid = update.effective_chat.id
    response = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    updater.bot.send_message(chat_id=chatid, text=response.status_code)
    utente = None
    if response.status_code == 200:
        data = response.json()
        for dic in data:
            if str(chatid) == str(dic["chat_id"]):
                utente = str(dic["id"])
                break
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
    dp.add_handler(CommandHandler('chatid', add_id))
    dp.add_handler(CommandHandler("addmicro", add_micro))
    dp.add_handler(CommandHandler("create", crea))
    dp.add_handler(CommandHandler("statup", status_update))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ciataidi))
    dp.add_handler(MessageHandler(Filters.location, location))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
