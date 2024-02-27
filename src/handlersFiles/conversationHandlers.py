import time, logging, config
import dataBaseFiles.databaseQuery as databaseQuerys
from telegram.ext import ConversationHandler
import apiServices.mapsCountry as mapsCountry
import dataBaseFiles.databaseQuery as databaseQuerys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)

table = config.table_Name_Users

class BotHandler:
    def __init__(self):
        self.START, self.LOCATIONUSER, self.PLATFORMS = range(3)

    def start(self, update, context):
        first_name = update.effective_user["first_name"]
        userName = update.effective_user["username"]
        iduser = update.effective_user["id"]
        date = update.message.date
        dateDatabase = date.strftime("%Y-%m-%d %H:%M:%S")

        dbuser = databaseQuerys.selectUser(table, iduser)
        dbcountry = databaseQuerys.selectCountry(table, iduser)
        dbplatforms = databaseQuerys.selectPlatforms(table, iduser)
        
        if dbuser == False:
            opcion1 = 'Por supuesto, preguntame!'
            opcion2 = 'No, esta bien, gracias.'

            keyboard = [
                [InlineKeyboardButton(opcion1, callback_data=opcion1)],
                [InlineKeyboardButton(opcion2, callback_data=opcion2)]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Woooow! ¡Hola ' + first_name + ' encantado de atenderte!')
            time.sleep(3)
            update.message.reply_text('Soy de los creadores de BotRex un chatbot para whatsapp!\n\nFui creado en Telegram para avisar sobre los precios de los juegos de las principales plataformas. 📈')
            time.sleep(4)
            update.message.reply_text(f'Antes de comenzar debo realizar un par de preguntas\n\n¿Estas listo?',reply_markup=reply_markup)
            
            country = None
            country_code = None
            platforms = None
            start_question = [True]

            # Save info in database if user is not registered
            databaseQuerys.saveData(table, userName, iduser, country, country_code, dateDatabase, platforms, start_question)

            return self.START
        elif dbuser == True and dbcountry == False:
            opcion1 = 'Por supuesto, preguntame!'
            opcion2 = 'No, esta bien, gracias.'

            keyboard = [
                [InlineKeyboardButton(opcion1, callback_data=opcion1)],
                [InlineKeyboardButton(opcion2, callback_data=opcion2)]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Bien ' + first_name + ' retomemos donde estabamos!')
            time.sleep(1)
            update.message.reply_text(f'Te debo realizar un par de preguntas\n\n¿Estas listo?',reply_markup=reply_markup)

            return self.START
        elif dbuser == True and dbcountry == True and dbplatforms == False:
            opcion1 = 'Claro!, dime...'

            keyboard = [
                [InlineKeyboardButton(opcion1, callback_data=opcion1)]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Bien ' + first_name + ' retomemos donde estabamos!')
            time.sleep(1)
            update.message.reply_text(f'Te debo realizar una pregunta mas\n\n¿Estas listo?',reply_markup=reply_markup)

            return self.PLATFORMS
        else:
            update.message.reply_text(text="Hey! ya estas registrado.")
            return ConversationHandler.END
    
    def locationUser(self, update, context):
        try:
            user_location = update.message.location
            iduser = update.effective_user["id"]
            all_platforms = ['Steam', 'Epic Games', 'Ubisoft', 'Origin', 'Battle net', 'GOG', 'Itchio', 'Xbox game pass']

            keyboard = [
                [InlineKeyboardButton("1- "+all_platforms[0], callback_data=all_platforms[0]),
                InlineKeyboardButton("2- "+all_platforms[1], callback_data=all_platforms[1]),
                InlineKeyboardButton("3- "+all_platforms[2], callback_data=all_platforms[2])],
                [InlineKeyboardButton("4- "+all_platforms[3], callback_data=all_platforms[3]),
                InlineKeyboardButton("5- "+all_platforms[4], callback_data=all_platforms[4]),
                InlineKeyboardButton("6- "+all_platforms[5], callback_data=all_platforms[5])],
                [InlineKeyboardButton("7- "+all_platforms[6], callback_data=all_platforms[6]),
                InlineKeyboardButton("8- "+all_platforms[7], callback_data=all_platforms[7])],
                [InlineKeyboardButton("9- Todas las plataformas", callback_data='all_platforms')],
                [InlineKeyboardButton("Listo!", callback_data='done')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Generic location
            if user_location is None:
                country = "United States"
                country_code = "us"

                databaseQuerys.saveCountry(table, iduser, country, country_code)

                update.message.reply_text('No hay problema!\n\nTe brindare la informacion generica al momento de darte un aviso.\n\nBien, ahora necesito saber que plataformas te interesan para avisarte siempre que haya una promocion o juego gratuito!')

            else:
                latitude = user_location.latitude
                longitude = user_location.longitude
                country, country_code = mapsCountry.obtain_country(latitude, longitude)
                
                databaseQuerys.saveCountry(table, iduser, country, country_code)
                
                update.message.reply_text('Mega Fantastico, muchas gracias!!!\n\nTe brindare la informacion mas acertada a tu ubicacion al momento de darte un aviso.\n\nBien, ahora necesito saber que plataformas te interesan para avisarte siempre que haya una promocion o juego gratuito!')

            update.message.reply_text('Por favor, selecciona tus plataformas:', reply_markup = reply_markup)

            return self.PLATFORMS
        except Exception as e:
            logging.info(f"Info: Error to obtain location user.",e)
    
    def unrecognized_message(self, update, context):
        update.message.reply_text('No he entendido, escribe nuevamente o selecciona las opciones correspondientes.')
        return
    
    # Otros métodos para diferentes estados
    def cancel(self, update, context):
        bot = context.bot
        ChatId = update.message.chat_id
        bot.sendMessage(chat_id = ChatId, parse_mode = "HTML", text = f'Operacion cancelada.')
        return ConversationHandler.END