import logging, telegram
from config import TOKEN
from index import logger, run
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
import processFlow.processFunctions as processFunctions
import handlersFiles.conversationHandlers as CH

logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,")

def loggerInfo(userName, ChatId, messageId, text):
    logger.info(f'El Usuario {userName} Id:{ChatId} ah solicitado {text} Id mensaje: {messageId}.')

def echo(update,context):
    bot = context.bot
    updatemsg = getattr(update, 'message', None)

    #Obtener Id del mensaje
    messageId = updatemsg.message_id
    ChatId = update.message.chat_id
    userName = update.effective_user["first_name"]

    #Obtener texto que ingreso el usuario
    text = update.message.text
    lowerText = text.lower()
    
    loggerInfo(userName, ChatId, messageId, text)

    menu = 'menu'
    saludos = ('hola', 'buenas', 'buenos dias', 'buenas tardes', 'buenas noches')
    informacionbot = 'informacion sobre el bot'
    historial = 'ver historial'
    cancelar = 'cancelar'

    # Make flow with save data
    if informacionbot in lowerText:
        processFunctions.getBotInfo(update, context)
    elif menu in lowerText:
        processFunctions.Menu(update, context)
    elif any(saludo in lowerText for saludo in saludos):
        processFunctions.welcome(update, context)
    #elif historial in lowerText:
    #    processFunctions.seeHistorial(update, context)
    else:
        update.message.reply_text(f'Lo siento pero no entendi. 😔')
        logger.info(f'El usuario {userName} introdujo un comando no valido.')

if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    
updater = Updater(myBot.token, use_context=True)

dp = updater.dispatcher

dp.add_handler(processFunctions.conv_handler)
# Process location
location_handler = MessageHandler(Filters.location, CH.BotHandler().locationUser)
dp.add_handler(location_handler)
# Process callbacks
dp.add_handler(CallbackQueryHandler(processFunctions.User_Handler))

# The bot listen the commands or chat
dp.add_handler(MessageHandler(Filters.text, echo))
run(updater)