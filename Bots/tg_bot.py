import telebot
from telebot import types
import psycopg2
from get_db import get_event_list, get_event_data
from datetime import datetime, timedelta, timezone

bot = telebot.TeleBot('8286621737:AAHEZDZvZo-wG-hhpOpbFIx7TDDtPENHk7c')

# Словарь для хранения состояния пользователей
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton('Вперёд!')
    markup.add(start)
    bot.send_message(message.from_user.id, '''
Привет! 👋 Я — твой персональный бот-навигатор по культурным событиям Орла и Орловской области. 🎭🎨

Здесь ты найдёшь всё самое интересное: концерты 🎵, выставки 🖼️, театральные постановки 🎬 и многое другое! Просто выбери категорию, которая тебе по душе, и получи актуальную информацию о ближайших событиях. 📅✨

Если нужна помощь или советы — я всегда рядом! 🤖💬 Готов сделать твой досуг насыщенным и увлекательным! Поехали? 🚀
''', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Вперёд!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        event = types.KeyboardButton("Мероприятия")
        route = types.KeyboardButton("Маршруты")
        pict_places = types.KeyboardButton("Живописные места")
        markup.add(event, route, pict_places)
        bot.send_message(message.from_user.id, '''
Выбери, что тебя интересует:

🗓️ Мероприятия — самые свежие и интересные события в Орле и Орловской области
🗺️ Маршруты — лучшие культурные и туристические маршруты по региону
🌄 Живописные места — вдохновляющие уголки природы и красоты рядом с тобой''', reply_markup=markup)

    elif message.text == 'Мероприятия':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        event_list = [types.KeyboardButton(event) for event in get_event_list()]
        event_list.append(types.KeyboardButton("Главное меню"))
        markup.add(*event_list)
        bot.send_message(message.from_user.id, '**Выберите тип мероприятия:**', parse_mode='Markdown', reply_markup=markup)

    elif message.text == 'Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        event = types.KeyboardButton("Мероприятия")
        route = types.KeyboardButton("Маршруты")
        pict_places = types.KeyboardButton("Живописные места")
        markup.add(event, route, pict_places)
        bot.send_message(message.from_user.id, '''
Выбери, что тебя интересует:

🗓️ Мероприятия — самые свежие и интересные события в Орле и Орловской области
🗺️ Маршруты — лучшие культурные и туристические маршруты по региону
🌄 Живописные места — вдохновляющие уголки природы и красоты рядом с тобой''', reply_markup=markup)

    elif message.text in ['Концерты', 'Спектакли', 'Выставки']:
        # Получаем данные и фильтруем их
        data_events = get_event_data(message.text)
        filtered_events = []
        
        for data in data_events:
            if message.text == 'Выставки':
                date_start = data['start_date']
                date_end = data['end_date']
                now = datetime.now(timezone.utc)
                if now < date_end < now + timedelta(days=30):
                    filtered_events.append(data)
            else:
                date = data['start_date']
                now = datetime.now(timezone.utc)
                if now < date < now + timedelta(days=30):
                    filtered_events.append(data)
        
        # Сохраняем состояние пользователя
        user_id = message.from_user.id
        user_states[user_id] = {
            'event_type': message.text,
            'events': filtered_events,
            'current_index': 0,
            'message_id': None  # Будем хранить ID сообщения для редактирования
        }
        
        # Показываем первое мероприятие
        show_event(user_id, first_time=True)

def show_event(user_id, first_time=False):
    if user_id not in user_states:
        return
    
    state = user_states[user_id]
    events = state['events']
    current_index = state['current_index']
    
    if not events:
        bot.send_message(user_id, 'К сожалению, на ближайшие 30 дней мероприятий не найдено.')
        return
    
    data = events[current_index]
    event_type = state['event_type']
    
    # Создаем клавиатуру для навигации
    markup = types.InlineKeyboardMarkup()
    
    # Добавляем кнопки навигации
    nav_buttons = []
    if current_index > 0:
        nav_buttons.append(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'prev_{event_type}'))
    
    nav_buttons.append(types.InlineKeyboardButton(f'{current_index + 1}/{len(events)}', callback_data='page'))
    
    if current_index < len(events) - 1:
        nav_buttons.append(types.InlineKeyboardButton('Вперёд ➡️', callback_data=f'next_{event_type}'))
    
    markup.row(*nav_buttons)
    
    # Формируем сообщение в зависимости от типа мероприятия
    if event_type == 'Выставки':
        date_start = data['start_date']
        date_end = data['end_date']
        caption = f'''
*{data['title']}*

Время проведения: {date_start.strftime("%d.%m %H:%M")} - {date_end.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание: {data['description'][:500]}{'...' if len(data['description']) > 500 else ''}

[Купить билет]({data['website']})
'''
        if first_time:
            # Первый раз отправляем фото с подписью
            try:
                with open('/home/radmir/Bots/Telegram/images.jpeg', 'rb') as photo:
                    sent_message = bot.send_photo(user_id, photo, caption=caption, parse_mode='Markdown', reply_markup=markup)
                    state['message_id'] = sent_message.message_id
                    state['has_photo'] = True
            except:
                sent_message = bot.send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
                state['message_id'] = sent_message.message_id
                state['has_photo'] = False
        else:
            # Редактируем существующее сообщение
            if state.get('has_photo'):
                try:
                    bot.edit_message_caption(
                        chat_id=user_id,
                        message_id=state['message_id'],
                        caption=caption,
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                except Exception as e:
                    # Если не удалось отредактировать подпись, отправляем новое сообщение
                    with open('/home/radmir/Bots/Telegram/images.jpeg', 'rb') as photo:
                        sent_message = bot.send_photo(user_id, photo, caption=caption, parse_mode='Markdown', reply_markup=markup)
                        state['message_id'] = sent_message.message_id
            else:
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=state['message_id'],
                    text=caption,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
    else:
        date = data['start_date']
        message_text = f'''
*{data['title']}*

Начало: {date.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание: {data['description'][:500]}{'...' if len(data['description']) > 500 else ''}

[Купить билет]({data['website']})
'''
        if first_time:
            # Первый раз отправляем текстовое сообщение
            sent_message = bot.send_message(user_id, message_text, parse_mode='Markdown', reply_markup=markup)
            state['message_id'] = sent_message.message_id
            state['has_photo'] = False
        else:
            # Редактируем существующее сообщение
            bot.edit_message_text(
                chat_id=user_id,
                message_id=state['message_id'],
                text=message_text,
                parse_mode='Markdown',
                reply_markup=markup
            )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = call.data
    
    if user_id not in user_states:
        bot.answer_callback_query(call.id, "Сессия устарела. Выберите мероприятие заново.")
        return
    
    state = user_states[user_id]
    
    if data.startswith('prev_'):
        # Переход к предыдущему мероприятию
        if state['current_index'] > 0:
            state['current_index'] -= 1
            show_event(user_id, first_time=False)
        bot.answer_callback_query(call.id)
    
    elif data.startswith('next_'):
        # Переход к следующему мероприятию
        if state['current_index'] < len(state['events']) - 1:
            state['current_index'] += 1
            show_event(user_id, first_time=False)
        bot.answer_callback_query(call.id)
    
    elif data == 'page':
        bot.answer_callback_query(call.id, f"Страница {state['current_index'] + 1} из {len(state['events'])}")

bot.polling(none_stop=True, interval=0)