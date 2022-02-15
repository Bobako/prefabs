"""Нужен для работы с модными кнопками в тг.
По сути, хранит в ОЗУ, какую функцию нужно вызвать по нажатию за тебя.
Закоменченное - удаление старых сообщений с кнопками"""


class Callback:
    callback_funcs = {}

    # inline_messages = {}

    def __init__(self):
        pass

    def register_callback(self, message, func, *args):
        # self.delete_old_inline(message.chat.id)
        key = str(message.chat.id) + str(message.id)
        self.callback_funcs[key] = [func, args]
        # self.inline_messages[message.chat.id] = message.id

    def run_callback(self, call, data):
        bot.answer_callback_query(call.id)
        # bot.delete_message(call.message.chat.id, call.message.id)
        key = str(call.message.chat.id) + str(call.message.id)
        try:
            func, args = self.callback_funcs[key]
        except KeyError:
            return
        func(call, data, *args)


"""Применение:"""

cb = Callback()

msg = bot.send_message(..., reply_markup=some_keyboard())  # какое то сообщение с инлайн кнопками

cb.register_callback(msg, some_func, some_arg1,
                     some_arg2)  # по нажатию вызовет some_func с аргументами call, data, some_arg1, some_arg2


def some_arg(call, data, some_arg1, some_arg2):
    pass
"""В call и data придет инфа о нажатии - кто, когда, зачем, какой жсон положили в кнопку"""


def currencies_keyboard(currencies):  # пример собственно клавиатуры с инлайн кнопками
    k = types.InlineKeyboardMarkup()
    for currency in currencies:
        k.add(types.InlineKeyboardButton(text=currency, callback_data=json.dumps({"currency": currency})))
    return k
