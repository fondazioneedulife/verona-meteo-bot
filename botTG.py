import sqlite3
from telegram.ext import Updater
updater = Updater(token='5264647805:AAGj67m7JD0WM3BDSixG4d3CH1Rq_XtS5SQ', use_context=True)
dispatcher = updater.dispatcher
from telegram import Update
from telegram.ext import CallbackContext, CallbackContext,CommandHandler

db = 'Meteo.db'
conn = sqlite3.connect(db)
cur = conn.cursor()
strt = "Benvenuto in Meteo Verona!\nIl bot che ti tiene aggiornato sul meteo della tua città!\nPer iniziare digita /data indicando la data che ti interessa, utilizzando il formato GG/MM/AA\nSe hai bisogno di aiuto digita /help"
hp = "Benvenuto nella sezione comandi!\nProva a digitare:\n- /locazione\nPer consocere la posizione della stazione da te selezionata\n- /temperatura\nPer sapere le temperature della tua città\n- /vento\nPer conoscere in che direzione si sta spostando il vento\n- /pioggia\nPer sapere quanti millimetri di pioggia sono caduti fin ora"
t = "1"
o = "1"
id = "1"


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=strt)


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=hp)


def data(update: Update, context: CallbackContext):
    dt = (" ").join(context.args)
    global t 
    global o
    global id
    t = dt
    
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT DATA, ORA FROM Locazione
                    WHERE DATA == "''' +str(dt)+ '''"
                ''')
    ldata = cur.fetchmany(10)
    c=0
    for x in ldata:
        update.message.reply_text("data e ora" + str(ldata[c]))
        c=c+1
    if(o=="1"):
        update.message.reply_text("seleziona un ora con /ora <orario>")
    else:#assegna id
        cur.execute('''SELECT IDStazione FROM Locazione
                    WHERE Data == "''' +str(t)+ '''" and Ora == "''' +str(o)+ '''"
                ''')
        rid = cur.fetchall()
        id = rid[1][0]

    update.message.reply_text('\ndata selezionata: '+ dt)


def ora(update: Update, context: CallbackContext):
    a = (" ").join(context.args)
    global o 
    global t
    global id
    o = a
    print(a)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT ORA, DATA FROM Locazione
                    WHERE ORA == "''' +str(a)+ '''"
                ''')
    ora = cur.fetchmany(10)
    c=0
    for x in ora:
        update.message.reply_text("data e ora" + str(ora[c]))
        c=c+1

    if(o=="1"):
        update.message.reply_text("seleziona una data con /data <data>")
    else:#assegna id
        cur.execute('''SELECT IDStazione FROM Locazione
                    WHERE Data == "''' +str(t)+ '''" and Ora == "''' +str(o)+ '''"
                ''')
        rid = cur.fetchall()
        id = rid[1][0]
    
    update.message.reply_text('\nora selezionata: '+ a)



def asd(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    context.bot.send_message(chat_id=update.effective_chat.id, text=o)
    context.bot.send_message(chat_id=update.effective_chat.id, text=id)


def vento(update: Update, context: CallbackContext):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT Vento.RAFF , Vento.WIND , Vento.WIND_DIR FROM Vento
                    INNER JOIN Locazione on Locazione.ID = Vento.ID_Locazione
                    WHERE Locazione.ID == ''' + str(id) + '''
            ''')
    wind = cur.fetchall()
    a = wind[0][0]
    b = wind [0][1]
    c = wind [0][2]
    print(a)
    print(b)
    print(c)
    update.message.reply_text("Vento in nodi: " + str(a) +"\nRaffiche: " + str(b)+ "\nDirezione del vento: " + str(c))



def locazione(update: Update, context: CallbackContext):
    global t
    global o
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT IDStazione FROM Locazione
                    WHERE ID == ''' + str(id) + '''
                ''')
    staz = cur.fetchall()
    a = staz[0][0]
    print(a)
    update.message.reply_text("ID stazione: " + str(a) +"\nData: " + str(t)+ "\nOra: " + str(o))


def pioggia(update: Update, context: CallbackContext):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT Pioggia.RAIN , Pioggia.DP  FROM Pioggia
                    INNER JOIN Locazione on Locazione.ID = Pioggia.ID_Locazione
                    WHERE Locazione.ID == ''' + str(id) + '''
            ''')
    rain = cur.fetchall()
    piog=rain[0][0]
    dew = rain [0][1]
    print(piog)
    print(dew)
    update.message.reply_text("Millimetri di pioggia: " + str(piog) +"\nPunto di rugiada: " + str(dew))


def temperatura(update: Update, context: CallbackContext):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT Temperatura.T , Temperatura.UR , Temperatura.PR FROM Temperatura
                INNER JOIN Locazione on Locazione.ID = Temperatura.ID_Locazione
                WHERE Locazione.ID == ''' + str(id) + '''
            ''')
    temp = cur.fetchall()
    a = temp[0][0]
    b = temp [0][1]
    c = temp [0][2]
    print(a)
    print(b)
    print(c)
    update.message.reply_text("Temperatura: " + str(a) +"\nUR: " + str(b)+ "\nPR: " + str(c))


temp_handler = CommandHandler('temperatura', temperatura)
dispatcher.add_handler(temp_handler)
updater.start_polling()
pioggia_handler = CommandHandler('pioggia', pioggia)
dispatcher.add_handler(pioggia_handler)
updater.start_polling()
locazione_handler = CommandHandler('locazione', locazione)
dispatcher.add_handler(locazione_handler)
updater.start_polling()
vento_handler = CommandHandler('vento', vento)
dispatcher.add_handler(vento_handler)
updater.start_polling()
data_handler = CommandHandler('asd', asd)
dispatcher.add_handler(data_handler)
updater.start_polling()
data_handler = CommandHandler('data', data)
dispatcher.add_handler(data_handler)
updater.start_polling()
ora_handler = CommandHandler('ora', ora)
dispatcher.add_handler(ora_handler)
updater.start_polling()
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)
updater.start_polling()
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

conn.close()
