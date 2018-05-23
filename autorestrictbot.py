import os
import logging

from dotenv import load_dotenv, find_dotenv

from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram.ext.filters import Filters

logger = logging.getLogger(__name__)

class AutoRestrictBot(object):
    def __init__(self, dispatcher, chat_id):
        self.chat_id = chat_id
        if self.chat_id != None:
            dispatcher.add_handler(MessageHandler(Filters.chat(self.chat_id) &
                Filters.status_update.new_chat_members, self.new_member))
        else:
            dispatcher.add_handler(CommandHandler('get_chat_id',
                                                  self.get_chat_id))
        dispatcher.add_error_handler(self.error)
    def new_member(self, bot, update):
        new_members = update.message.new_chat_members
        for member in new_members:
            bot.restrict_chat_member(self.chat_id, member.id,
                                     can_send_messages=False,
                                     can_send_media_messages=False,
                                     can_send_other_messages=False)
    def get_chat_id(self, bot, update):
        update.message.reply_text('{}'.format(update.message.chat.id),
                                  quote=True)
    def error(self, bot, update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    load_dotenv(find_dotenv())
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s - %(levelname)-8s %(message)s')
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', None)
    if chat_id is not None:
        chat_id = int(chat_id)
    updater = Updater(token)
    auto_restrict_bot = AutoRestrictBot(updater.dispatcher, chat_id)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
