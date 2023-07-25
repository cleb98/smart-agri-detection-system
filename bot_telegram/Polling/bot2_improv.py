from telegram import Bot
from config import BOTKEY, CHAT_ID
import requests

testo1 = "Il micro con identificativo "
testo2 = " ha rilevato una minaccia per la coltivazione"

dict_utenti = {}
poppatore = {}

def inizializzazione_dict_utenti():
    risposta = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
    if risposta.status_code == 200:
        dati = risposta.json()
    for usatore in dati:
        dict_utenti[str(usatore["id"])] = None

    for utente in dict_utenti:
        risposta = requests.get(f"https://insects_api-1-q3217764.deta.app/microcontrollers/user/{utente}")
        if risposta.status_code == 200:
            dati1 = risposta.json()
            lista_micro = []
            for microcontrollore in dati1:
                if bool(microcontrollore["status"]) == True:          #c'è da capire se i micro sono attivi quando False o True
                    lista_micro.append(int(microcontrollore["id"]))
            dict_utenti[utente] = lista_micro
    for key in dict_utenti:
        poppatore[str(key)] = False


def pollo():
    bot = Bot(token=BOTKEY)
    while True:
        print("°°°°° FROM THE TOP °°°°°")
        risposta = requests.get(f"https://insects_api-1-q3217764.deta.app/users/")
        if risposta.status_code == 200:
            dati = risposta.json()
            for utente in dati:
                id_utente = str(utente["id"])
                chat_utente = str(utente["chat_id"])
                poppatore[id_utente] = True
                risposta = requests.get(f"https://insects_api-1-q3217764.deta.app/microcontrollers/user/{id_utente}")

                # if tizio è nel dict controlla i micro
                # se i micro in allarme sono nella lista non fare nulla
                # se dei micro mancano alla lista avvisa utente e cacciali nella lista
                # se un micro che è nella lista non è in allarme toglilo dalla lista


                if (id_utente in dict_utenti):
                    print(f"utente {id_utente} già presente")
                    if risposta.status_code == 200:
                        dati1 = risposta.json()
                        lista_micro = dict_utenti[id_utente]
                        for microcontrollore in dati1:
                            if (bool(microcontrollore["status"]) == True and int(microcontrollore["id"]) not in dict_utenti[id_utente]):
                                bot.send_message(chat_id=chat_utente, text=testo1 + str(microcontrollore["id"]) + testo2)
                                print(str(testo1 + str(microcontrollore["id"]) + testo2))
                                lista_micro.append(int(microcontrollore["id"]))

                            if (bool(microcontrollore["status"]) == False and int(microcontrollore["id"]) in dict_utenti[id_utente]):
                                lista_micro.remove(int(microcontrollore["id"]))




                else:
                    print("nuovo utente")
                    dict_utenti[id_utente] = None
                    #risposta = requests.get(f"https://djdkdw.deta.dev/microcontrollers/user/{id_utente}")
                    if risposta.status_code == 200:
                        dati1 = risposta.json()
                        lista_micro = []
                        for microcontrollore in dati1:
                            if (bool(microcontrollore["status"]) == True):                                                     # c'è da capire se i micro sono attivi quando False o True
                                lista_micro.append(int(microcontrollore["id"]))
                                bot.send_message(chat_id=chat_utente, text=testo1 + str((microcontrollore["id"])) + testo2)
                        dict_utenti[id_utente] = lista_micro

        for key in poppatore:
            if(poppatore[key] == False):
                dict_utenti.pop(key)
                poppatore.pop(key)
            poppatore[key] =False



            #if tizio è nel dict controlla i micro || se non c'è aggiungilo (copia codice da primo metodo)
            #se i micro in allarme sono nella lista non fare nulla
            #se dei micro mancano alla lista avvisa utente e cacciali nella lista
            #se un micro che è nella lista non è in allarme toglilo dalla lista
            # ^.^ se un utente presente nella lista non viene menzionato dal database droppalo   --> se key ha falso droppa da entrambe. quando poi un nome viene letto deve essere riaggiunto anche a poppatore

if __name__ == '__main__':
    inizializzazione_dict_utenti()
    pollo()







'''
def pollo_rinforzante():
    bot = Bot(token=BOTKEY)
    while True:
        bot.send_message(chat_id=CHAT_ID, text="mammata")
        risposta = requests.get(f"https://djdkdw.deta.dev/users/")
        if risposta.status_code == 200:
            dati = risposta.json()
        for usatore in dati:
            usatore = str(usatore)
            poppatore[usatore] = True #mi annota la presenza di un utente nel database così se questo manca droppo l'utente dal dizionario

            if (usatore in dict_utenti):
                print("utente in lista")

            else:                                                                  #se la chiave non c'è la creo e la riempio
                risposta = requests.get(f"https://djdkdw.deta.dev/microcontrollers/user/{usatore}")
                dati1 = risposta.json()
                lista_micro = []
                for microcontrollore in dati1:
                    if (bool(microcontrollore["status"]) == False):             # c'è da capire se i micro sono attivi quando False o True
                        lista_micro.append(str(microcontrollore["id"]))
                        bot.send_message(chat_id=CHAT_ID, text= testo1 + str((microcontrollore["id"])) + testo2)
                dict_utenti[usatore] = lista_micro





        for key in poppatore:
            if(poppatore[key] == False):
                dict_utenti.pop(key)
                poppatore.pop(key)
            poppatore[key] =False
'''