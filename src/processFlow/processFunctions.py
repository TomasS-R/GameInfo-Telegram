import logging, config
import dataBaseFiles.databaseQuery as db
import handlersFiles.conversationHandlers as CH
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

def User_Handler(update, context):
    query = update.callback_query

    user_choice = query.data

    user_id_tg = update.effective_user["id"]
    table_name = config.table_Name_Users

    result = db.selectCountry(table_name, user_id_tg)
    #dbplatforms = db.selectPlatforms(table_name, user_id_tg)

    if result == False:
        if user_choice == 'Por supuesto, preguntame!':

            accept_location_keyboard = KeyboardButton(text="Enviar ubicación", request_location=True)
            decline_location_keyboard = KeyboardButton(text="Prefiero no hacerlo", request_location=False)

            custom_keyboard = [[accept_location_keyboard],[decline_location_keyboard]]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            query.edit_message_text('Muy bien!')

            context.bot.send_message(chat_id=update.effective_chat.id, text='Necesito que brindes acceso a tu región para poder brindarte un mejor servicio.', reply_markup=reply_markup)
            
            return myFlowSaveData.LOCATIONUSER
        
        elif user_choice == 'No, esta bien, gracias.':

            query.edit_message_text(text="¡Entendido! Si cambias de opinión, solo házmelo saber con el comando /start.")
            
            return ConversationHandler.END
        else:
            # Maneja casos inesperados
            query.edit_message_text(text="No entendí tu elección. Intenta de nuevo.")
            return myFlowSaveData.START

def saveData(update, context):
    query = update.callback_query
    user_id_tg = update.effective_user["id"]
    table_name = config.table_Name_Users

    dbplatforms = db.selectPlatforms(table_name, user_id_tg)
    text = 'Claro!, dime...'
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

    if dbplatforms == False and query.data == text:
        query.edit_message_text('Genial, ahora necesito saber que plataformas te interesan para avisarte siempre que haya una promocion o juego gratuito!\n\nPor favor, selecciona tus plataformas:', reply_markup=reply_markup)
        return myFlowSaveData.PLATFORMS
    elif query.data == 'done':
        # When user press done button save the platforms in the database if not have any platform selected show a message
        selected_platforms = context.user_data.get('selected_platforms', [])
        if 'all_platforms' in context.user_data:
            db.savePlatforms(table_name, user_id_tg, all_platforms)
            query.edit_message_text(text="Has seleccionado: Todas las plataformas")
            return ConversationHandler.END
        else:
            #logging.info(f"Plataformas seleccionadas: {len(selected_platforms)}")
            if len(selected_platforms) == 0:
                query.edit_message_text(text="No has seleccionado ninguna plataforma.\n\nSelecciona minimo 1 opcion", reply_markup=reply_markup)
                return myFlowSaveData.PLATFORMS
            else:
                db.savePlatforms(table_name, user_id_tg, selected_platforms)
                formatted_platforms = "\n".join([f"{i+1}- {platform}" for i, platform in enumerate(selected_platforms)])
                query.edit_message_text(text=f"Has seleccionado:\n{formatted_platforms}")
                return ConversationHandler.END
    else:
        # Special case for all platforms
        if query.data == 'all_platforms':
            # If user deselects all platforms, remove the key from the user_data dict
            if query.data in context.user_data:
                del context.user_data['all_platforms']
                context.user_data['selected_platforms'] = []
                platforms_text = " "
            else:
                context.user_data['selected_platforms'] = []
                context.user_data['all_platforms'] = True
                platforms_text = "Todas las plataformas"
        else:
            # If user select platform add it to the list, else remove it finnaly format the text and show user the current selection
            if 'selected_platforms' not in context.user_data:
                context.user_data['selected_platforms'] = []
            if query.data in context.user_data['selected_platforms']:
                context.user_data['selected_platforms'].remove(query.data)
            else:
                context.user_data['selected_platforms'].append(query.data)
            platforms_text = "\n".join(context.user_data['selected_platforms'])
        
        query.edit_message_text(text=f"Plataforma seleccionada:\n{platforms_text}\nSelecciona otra plataforma o presiona 'Listo!'", reply_markup=reply_markup)

myFlowSaveData = CH.BotHandler() 

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', myFlowSaveData.start)],
    states={
        myFlowSaveData.START: [CallbackQueryHandler(User_Handler)],
        myFlowSaveData.LOCATIONUSER: [
            MessageHandler(Filters.location, myFlowSaveData.locationUser),
            MessageHandler(Filters.text, myFlowSaveData.locationUser)
        ],
        myFlowSaveData.PLATFORMS: [CallbackQueryHandler(saveData)]
    },
    fallbacks=[CommandHandler('cancel', myFlowSaveData.cancel), MessageHandler(Filters.text, myFlowSaveData.unrecognized_message)],
)

def welcome(update, context):
    userName = update.effective_user["first_name"]
    keyboard = []

    keyboard.append([KeyboardButton(f'/nuevo', callback_data='1'), KeyboardButton(f'Ver historial', callback_data='2')])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text('¡Hola ' + userName + ' gracias por llamarme!\nDime que deseas hacer?', reply_markup=reply_markup)

def getBotInfo(update, context):
    bot = context.bot
    ChatId = update.message.chat_id
    
    # Menu keyboard
    keyboard = []
    keyboard.append([KeyboardButton(f'🔙 Atras', callback_data='8'), KeyboardButton(f'📝 Menu', callback_data='7')])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    # Fin Menu
    bot.sendMessage(chat_id = ChatId, parse_mode = "HTML", text = f'Soy un bot creado para avisar sobre los precios de los productos/servicios que desees rastrear. 📈')
    update.message.reply_text('¿Deseas regresar al menu?', reply_markup=reply_markup)

def Menu(update, context):
    keyboard = []

    keyboard.append([KeyboardButton(f'Rastrear_Precio', callback_data='1'), KeyboardButton(f'🌐 Redes Sociales', callback_data='2')])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('📝 *Menu* \nElige una de las siguientes opciones:',  reply_markup=reply_markup)
