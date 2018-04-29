import telebot, json


def start_telegram(manager):
    bot = telebot.TeleBot(manager.settings["token"])

    def send(chat_id, tosend):
        if not tosend:
            return

        for stype, sdata in tosend:
            if stype == "text":
                bot.send_message(chat_id, sdata)

            elif stype == "image":
                bot.send_photo(chat_id, sdata)

            elif stype == "video":
                bot.send_photo(chat_id, sdata)

            elif stype == "location":
                bot.send_location(chat_id, sdata["lat"], sdata["long"])

    @bot.message_handler(commands=["start"])
    def start(message):
        send(message.chat.id, manager.create_chat(message.chat.id))

    @bot.message_handler(commands=["reset"])
    def start(message):
        send(message.chat.id, manager.reset_chat(message.chat.id))

    @bot.message_handler(content_types=['text'])
    def get_message(message):
        send(message.chat.id, manager.process_message(message.chat.id, message.text))

    @bot.message_handler(content_types=['location'])
    def get_location(message):
        send(message.chat.id, manager.update_step(message.chat.id, location=(
            message.location.latitude,
            message.location.longitude
        )))

    @bot.edited_message_handler(content_types=['location'])
    def update_location(message):
        send(message.chat.id, manager.update_step(message.chat.id, location=(
            message.location.latitude,
            message.location.longitude
        )))

    meta = [None,]

    print("] Start polling.")

    bot.polling(none_stop=True)

    print("\n] Stop polling.")
