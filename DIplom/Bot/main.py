import sqlite3
from telebot import types, TeleBot

bot = TeleBot('6372943040:AAF8tK6O331qBpMZiDF-8eDFZ7775f4DFhA')

# Добавьте переменную для отслеживания текущего ID вопроса
current_question_id = 1

def send_question(message, question_id):
    with sqlite3.connect('test_questions.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM questions WHERE id == {question_id}')
        questions = cur.fetchall()
        info = '\n'.join(f'Номер вопроса {el[0]} из 1024 \nВопрос: {el[1]}' for el in questions)
        bot.send_message(message.chat.id, info)
        
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('A', callback_data='A')
        btn2 = types.InlineKeyboardButton('B', callback_data='B')
        btn3 = types.InlineKeyboardButton('C', callback_data='C')
        btn4 = types.InlineKeyboardButton('D', callback_data='D')
        btn5 = types.InlineKeyboardButton('Вернуться на главную', callback_data='back')
        markup.row(btn1, btn2, btn3, btn4)
        markup.row(btn5)
        bot.send_message(message.chat.id, 'Выберите ответ\n', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Начать', callback_data='start')
    btn2 = types.InlineKeyboardButton('Информация об экзамене', callback_data='about')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 
                     f'Добро пожаловать, есть такие команды: \n    start \n    или просто пришли фото', reply_markup=markup)
    global current_question_id
    current_question_id = 1  # Сбросить ID вопроса при начале новой сессии

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_question_id
    if call.data =='start':
        #bot.delete_message(call.message.chat.id, call.message.message_id)
        send_question(call.message, current_question_id)
    elif call.data in ['A', 'B', 'C', 'D']:
        with sqlite3.connect('test_questions.db') as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM questions WHERE id == {current_question_id}')
            question = cur.fetchone()
            correct_answer = question[2]
            if correct_answer == call.data[-1]:
                current_question_id += 1  # Увеличить ID вопроса при правильном ответе
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('Следующий вопрос', callback_data='next')
                btn2 = types.InlineKeyboardButton('На главную', callback_data='back')
                markup.row(btn1, btn2)
                bot.send_message(call.message.chat.id, 'Ответ правильный', reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, 'Ответ неправильный')
    elif call.data == 'next':
        send_question(call.message, current_question_id)
    elif call.data == 'about':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Назад', callback_data='back' )
        markup.add(btn1)
        bot.send_message(call.message.chat.id, 
                         'Информация об экзамене: fhgffdgjdsj gfdjgf djgfd\ngfgfdg fdhgfdh dshfds hfdshf dshfds', reply_markup=markup)
    elif call.data == 'back':
        #bot.delete_message(call.message.chat.id, call.message.message_id-1)
        #bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
bot.polling(none_stop=True)