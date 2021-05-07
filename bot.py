import logging
from flask import Flask, request
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext,Dispatcher
from telegram import Bot
 #Enable logging
from telegram import Update,Bot
 #logging: any kind of error happen or warning is raised, so this is used to parse it in a systematic manner
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 	                level=logging.INFO)
#logger object can create logs for your program
logger=logging.getLogger(__name__)

TOKEN ="1784143113:AAHslDSQ7LqEK-ljjERrK4tRvvy_tiQIQI0"

app=Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods=['GET','POST'])
def webhook():
    # webhook view which receives updates from telegram#
    # create update object from json-format request data
    update=Update.de_json(request.get_json(), bot)
    # process update
    dispatcher.process_update(update)
    return "ok"


#https://python-telegram-bot.readthedocs.io/en/stable/ go to this link for referring the func usage

def _help(update: Update,context: CallbackContext):
    help_txt="This is help text"
    first_name = update.to_dict()['message']['chat']['first_name']
    update.message.reply_text("hi {}\n {}".format(first_name,help_txt))
    #bot.send_message(chat_id=update.message.chat_id,text=help_txt)
'''def echo_text(Bot, update: Update,context: CallbackContext):
    reply=update.message.text#contains the text of msg
    bot.send_message(chat_id=update.message.chat_id, text=reply)'''

def echo_sticker(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)


def error(bot,update):
    logger.error("Update '%s' has caused error '%s", update, update.error)#update.error contains error if caused due to update.

def greeting(update: Update,context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']
##    print(update.to_dict().keys(),first_name)
    update.message.reply_text("hi {}".format(first_name))

def message_handler(update: Update,context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)

def main():
    bot=Bot(TOKEN)
    bot.set_webhook("https://4201824f98ef.ngrok.io/"+TOKEN)
    #updater=Updater(TOKEN,use_context=True)#updator will keep polling and receive the updates from telegram and move it to the dispatcher
    #dispatcher handles those updates
    dp=Dispatcher(bot,NONE) #all the response will be handled

    #Add handlers
    #dispatcher needs multiple handlers
    #former start is for: if the user writes / with start then it will call the start(latter) function
    dp.add_handler(CommandHandler("start" , greeting))
    dp.add_handler(CommandHandler("help" , _help))
    #messageHandler class is for handling stickers and other text and if the msg is in text form user .text
    dp.add_handler(MessageHandler(Filters.text , message_handler))
    dp.add_handler(MessageHandler(Filters.sticker ,echo_sticker))
    dp.add_error_handler(error)

    #updater.start_polling()
    #logger.info("Started polling...")
    #updater.idle()#waits until the user presses ctrl+c or anything to stop the program

if __name__=="__main__":
    main()
    app.run(port=8443)
