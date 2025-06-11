import telebot
from telebot import types

bot = telebot.TeleBot("8183868011:AAE1ejQUW2OYZ-zms4S0uepGwK6E6iZYBQI")

questions = {
    1: {
        "question": "Сколько будет 2 + 2?",
        "options": ["3", "6", "5", "4"],
        "answer": "4"
    },
    2: {
        "question": "Как называется столица Франции?",
        "options": ["Мадрид", "Париж", "Рим", "Лондон"],
        "answer": "Париж"
    },
    3: {
        "question": "Где нашли броню полностью из золота?",
        "options": ["Монголия", "Айзербайджан", "Казахстан", "Китай"],
        "answer": "Казахстан"
    },
    4: {
        "question": "Сколько дней в феврале в високосном году?",
        "options": ["28", "29", "30", "31"],
        "answer": "29"
    },
    5: {
        "question": "Какое насекомое вызвало короткое замыкание в ранней версии вычислительной машины, тем самым породив термин «компьютерный баг»?",
        "options": ["Мотылек", "Таракан", "Муха", "Японский хрущик"],
        "answer": "Мотылек"
    }
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в игру 'Кто хочет стать миллионером'! Я буду показывать вам вопросы, а вы должны выбрать правильный ответ. У вас есть возможность использовать подсказку '50/50'. Поехали!")
    user_data[message.chat.id] = {"question_num": 1, "money": 0}
    send_question(message)

def send_question(message):
    question_num = user_data[message.chat.id]["question_num"]
    question = questions[question_num]["question"]
    options = questions[question_num]["options"]

    markup = types.ReplyKeyboardMarkup(row_width=2)
    for option in options:
        button = types.KeyboardButton(option)
        markup.add(button)

    bot.send_message(message.chat.id, question, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    question_num = user_data[message.chat.id]["question_num"]
    answer = questions[question_num]["answer"]

    if message.text == answer:
        user_data[message.chat.id]["money"] += 200000
        if question_num == 5:
            bot.send_message(message.chat.id, f"Поздравляем! Вы победили и выиграли 1000000 рублей!")
            bot.send_message(message.chat.id, f"Ваш выигрыш: {user_data[message.chat.id]['money']} рублей")
            return
        user_data[message.chat.id]["question_num"] += 1
        send_question(message)
    else:
        bot.send_message(message.chat.id, f"Ответ неверный! Ваш выигрыш: {user_data[message.chat.id]['money']} рублей")

bot.polling()