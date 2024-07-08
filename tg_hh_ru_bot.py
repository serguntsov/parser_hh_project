import telebot
from telebot import types
from values import TELEGRAM_BOT_TOKEN
from database import cursor, conn
from parcer_hh import find_vacancies_by_name

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

user_states = {}

name = None
salary_min = None
salary_max = None
value = None
location = None

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS filter(user_id BIGINT, name TEXT, salary_min TEXT, salary_max TEXT, value TEXT, location TEXT)""")
        cursor.execute("""
                INSERT INTO filter (user_id, name, salary_min, salary_max, value, location)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, 0, 0, 0, 0, 0))
        conn.commit()
    except Exception as e:
        print(f"Error creating filter table or inserting data: {e}")
    
    question(message.chat.id, f'Здравствуй, {message.from_user.first_name}!\n'
                     f'Бот создан для поиска вакансий, напишите вакансию для поиска', salary_min_def )

def get_start_markup_2(): 
    markup = types.InlineKeyboardMarkup(row_width=True) 
    start_button = types.InlineKeyboardButton(text="Старт", callback_data="start") 
    markup.add(start_button) 
    return markup

def get_next_markup_1():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next1 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next1")
    markup.add(next1)
    return markup

def get_next_markup_2():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next2 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next2")
    markup.add(next2)
    return markup

def get_next_markup_3():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next3 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next3")
    markup.add(next3)
    return markup

def get_next_markup_4():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next4 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next4")
    markup.add(next4)
    return markup

def get_next_markup_5():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next5 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next5")
    markup.add(next5)
    return markup

def get_next_markup_6():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next6 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next6")
    markup.add(next6)
    return markup

def get_next_markup_7():
    markup = types.InlineKeyboardMarkup(row_width=True)
    next7 = types.InlineKeyboardButton(text="Пропустить вопрос", callback_data="next7")
    markup.add(next7)
    return markup

def question(chat_id, question, next_step_handler, markup=None):
    msg = bot.send_message(chat_id, question, reply_markup=markup)
    user_states[chat_id] = next_step_handler
    bot.register_next_step_handler(msg, handle_response)

def handle_response(message):
    chat_id = message.chat.id
    if chat_id in user_states:
        next_step_handler = user_states.pop(chat_id)
        next_step_handler(message)

def salary_min_def(message):
    if message.text:
        bot.send_message(message.chat.id, "Подождите, идет поиск актуальных вакансий")
        find_vacancies_by_name(message.text, message.chat.id)
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = %s", ('vacancies',))
        if cursor.fetchone():
            user_id = message.chat.id
            cursor.execute("UPDATE filter SET name = %s WHERE user_id = %s;", (message.text, user_id))
            conn.commit()
            question(message.chat.id, "Установите параметр минимальной заработной платы\nВведите число.", salary_max_def, get_next_markup_1())
        else:
            msg = bot.send_message(message.chat.id, f"Такой вакансии не существует\nПопробуйте снова")
            bot.register_next_step_handler(msg, salary_min_def)
        
def salary_max_def(message):
    if message.text:
        user_id = message.chat.id
        cursor.execute("UPDATE filter SET salary_min = %s WHERE user_id = %s;", (message.text, user_id))
        conn.commit()
        question(message.chat.id, "Установите параметр максимальной заработной платы\nВведите число.", value_def, get_next_markup_2())

def value_def(message):
    if message.text == "RUR" or "KZT" or "EUR" or "USD":
        user_id = message.chat.id
        cursor.execute("UPDATE filter SET salary_max = %s WHERE user_id = %s;", (message.text, user_id))
        conn.commit()
        question(message.chat.id, f"Выберите валюту заработной платы.\nОтветить можно только RUR, KZT, EUR или USD", location_def, get_next_markup_3())
    else:
        msg = bot.send_message(message.chat.id, f"Такой валюты не существует\nОтветить можно только RUR, KZT, EUR или USD\nПопробуйте снова")
        bot.register_next_step_handler(msg, value_def)
        

def location_def(message):
    if message.text in ["RUR", "KZT", "EUR", "USD"]:
        user_id = message.chat.id
        cursor.execute("UPDATE filter SET value = %s WHERE user_id = %s;", (message.text, user_id))
        conn.commit()
        print("location")
        question(message.chat.id, "Укажите город поиска работы.", finish_def, get_next_markup_4())
    else:
        question(message.chat.id, f"В какой валюте мне искать?\nОтветить можно только RUR, KZT, EUR или USD", value_def, get_next_markup_3())
        

def finish_def(message): 
    if message.text: 
        user_id = message.chat.id 
        cursor.execute("UPDATE filter SET location = %s WHERE user_id = %s;", (message.text, user_id)) 
        conn.commit() 
        handle_finish(message)


def handle_finish(message):
        user_id = message.chat.id
        cursor.execute("SELECT user_id, name, salary_min, salary_max, value, location FROM filter WHERE user_id = %s;", (user_id,))
        row = cursor.fetchone()

        if row:
            user_id = row[0]
            name = row[1]
            salary_min = row[2]
            salary_max = row[3]
            value = row[4]
            location = row[5]

            try:
                salary_min = int(salary_min)
            except ValueError:
                salary_min = 0

            try:
                salary_max = int(salary_max)
            except ValueError:
                salary_max = 0

            sql_query = """
                SELECT v.name, v.salary_min, v.salary_max, v.value, v.location, v.id
                FROM vacancies v
                INNER JOIN filter u ON v.id_user = u.user_id
                WHERE 1=1
                """
                
            conditions = []
            params = []

            if salary_min > 0:
                conditions.append("v.salary_min >= %s")
                params.append(salary_min)
            if salary_max > 0:
                conditions.append("v.salary_max <= %s")
                params.append(salary_max)
            if value != "0":
                conditions.append("v.value = %s")
                params.append(value)
            if location != "0":
                conditions.append("v.location = %s")
                params.append(location)

            # Append conditions to SQL query
            if conditions:
                sql_query += " AND " + " AND ".join(conditions)

            sql_query += " ORDER BY v.id;"  # Order by vacancy ID for consistent pagination

            # Execute query and fetch results
            cursor.execute(sql_query, params)
            rows = cursor.fetchall()
            print(rows)

            if rows:
                # Store the vacancies in user's session data for pagination
                user_states[user_id] = {
                    'vacancies': rows,
                    'index': 0  # Start index for pagination
                }

                # Send the first batch of vacancies (up to 10)
                send_vacancies(user_id)
            else:
                bot.send_message(user_id, "Подходящих вакансий не найдено.")
        else:
            bot.send_message(user_id, "Данные в таблице filter не найдены.")
def send_vacancies(user_id): 
    session_data = user_states.get(user_id) 
    if session_data: 
        vacancies = session_data['vacancies'] 
        current_index = session_data['index'] 
 
        num_vacancies = len(vacancies) 
        batch_size = 10 
 
        if current_index < num_vacancies: 
            batch = vacancies[current_index:current_index + batch_size] 
            for index, vacancy in enumerate(batch, start=current_index + 1): 
                print(vacancy)
                vacancy_message = (
                    f"Вакансия: {vacancy[0]}\n"
                    f"Зарплата от: {vacancy[1]} до: {vacancy[2]} {vacancy[3]}\n"
                    f"Город: {vacancy[4]}\n"
                    f"<a href='{vacancy[5]}'>Ссылка на вакансию</a>"
                )
                bot.send_message(user_id, vacancy_message, parse_mode='HTML') 
 
            current_index += batch_size 

            session_data['index'] = current_index 
            user_states[user_id] = session_data 

            inline_markup = types.InlineKeyboardMarkup(row_width=2) 
            buttons = [] 
 
            if current_index < num_vacancies: 
                buttons.append(types.InlineKeyboardButton(text="Далее", callback_data="next_vacancies")) 
 
            buttons.append(types.InlineKeyboardButton(text="Завершить поиск", callback_data="finish_search"))
            inline_markup.add(*buttons) 
            bot.send_message(user_id, "Выберите действие:", reply_markup=inline_markup)




@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'next1':
        cursor.execute("UPDATE filter SET salary_min = %s WHERE user_id = %s;", (0, call.message.chat.id))
        conn.commit()
        question(call.message.chat.id, "При пропуске ответа, будут выдаваться все возможные варианты поиска\nДо какой зарплаты мне искать вакансию?", value_def, get_next_markup_2())
    
    elif call.data == 'next2':
        cursor.execute("UPDATE filter SET salary_max = %s WHERE user_id = %s;", (0, call.message.chat.id))
        conn.commit()
        question(call.message.chat.id, "При пропуске ответа, будут выдаваться все возможные варианты поиска\nВ какой валюте мне искать?\nОтветить можно только RUR, KZT, EUR или USD", value_def, get_next_markup_3())
    
    elif call.data == 'next3':
        cursor.execute("UPDATE filter SET value = %s WHERE user_id = %s;", (0, call.message.chat.id))
        conn.commit()
        question(call.message.chat.id, "При пропуске ответа, будут выдаваться все возможные варианты поиска\nВ каком городе мне искать вакансию?", finish_def, get_next_markup_4())
        
    elif call.data == 'next4':
        cursor.execute("UPDATE filter SET location = %s WHERE user_id = %s;", (0, call.message.chat.id))
        conn.commit()
        handle_finish(call.message)
    
    elif call.data == 'next5':
        question(call.message.chat.id, "До какой зарплаты мне искать вакансию?(бэк)", value_def, get_next_markup_2())
        
    elif call.data == 'next6':
            question(call.message.chat.id, f"В какой валюте мне искать?\nОтветить можно только RUR, KZT, EUR или USD", location_def, get_next_markup_3())
        
    elif call.data == 'next7':
        print("next7")
        question(call.message.chat.id, "В каком городе искать вакансию?", finish_def, get_next_markup_4())
        
    elif call.data == 'next_vacancies':
        send_vacancies(call.message.chat.id)
    
    elif call.data == 'finish_search': 
        user_id = call.message.chat.id 
        column_name1 = "id_user" 
        column_name2 = "user_id" 
        value_to_delete = user_id 
        delete_query = f"DELETE FROM vacancies WHERE {column_name1} = %s;" 
        cursor.execute(delete_query, (value_to_delete,)) 
        delete_query2 = f"DELETE FROM filter WHERE {column_name2} = %s;" 
        cursor.execute(delete_query2, (value_to_delete,)) 
        conn.commit() 
        question(call.message.chat.id, f"Поиск завершен\n" 
                    "Чтобы начать новый поиск, просто нажми кнопку старт", start, get_start_markup_2())
    
    elif call.data == 'start': 
        start(call.message)

bot.polling(none_stop=True)