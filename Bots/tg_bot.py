import telebot
from telebot import types
import psycopg2
from get_db import *
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
from message import *
from AI_sum_request import generate_text_with_model

bot = telebot.TeleBot('8286621737:AAHEZDZvZo-wG-hhpOpbFIx7TDDtPENHk7c')

# Словарь для хранения состояния пользователей
user_states = {}

def get_event_image_path(event_id):
    """Получает путь к изображению мероприятия"""
    # Сначала проверяем jpg
    jpg_path = Path(f'/home/radmir/OO/back/static/image/{event_id}.jpg')
    if jpg_path.exists():
        return jpg_path
    
    # Затем проверяем jpeg
    jpeg_path = Path(f'/home/radmir/OO/back/static/image/{event_id}.jpeg')
    if jpeg_path.exists():
        return jpeg_path
    
    # Если изображение не найдено, возвращаем None
    return None

def safe_send_message(chat_id, text, **kwargs):
    """Безопасная отправка сообщения с обработкой ошибок"""
    try:
        return bot.send_message(chat_id, text, **kwargs)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return None

def safe_send_photo(chat_id, photo, caption, **kwargs):
    """Безопасная отправка фото с обработкой ошибок"""
    try:
        return bot.send_photo(chat_id, photo, caption=caption, **kwargs)
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")
        return None

def safe_delete_message(chat_id, message_id):
    """Безопасное удаление сообщения"""
    try:
        bot.delete_message(chat_id, message_id)
        return True
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")
        return False

def safe_edit_message_text(chat_id, message_id, text, **kwargs):
    """Безопасное редактирование текстового сообщения"""
    try:
        bot.edit_message_text(text, chat_id, message_id, **kwargs)
        return True
    except Exception as e:
        print(f"Ошибка при редактировании текста: {e}")
        return False

def safe_edit_message_caption(chat_id, message_id, caption, **kwargs):
    """Безопасное редактирование подписи к фото"""
    try:
        bot.edit_message_caption(caption, chat_id, message_id, **kwargs)
        return True
    except Exception as e:
        print(f"Ошибка при редактировании подписи: {e}")
        return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton('Вперёд!')
    markup.add(start)
    safe_send_message(message.from_user.id, hello_mes, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Вперёд!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        event = types.KeyboardButton("Мероприятия")
        route = types.KeyboardButton("Маршруты")
        pict_places = types.KeyboardButton("Живописные места")
        markup.add(event, route, pict_places)
        safe_send_message(message.from_user.id, type_event_mes, reply_markup=markup)

    elif message.text == 'Мероприятия':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        event_list = [types.KeyboardButton(event) for event in get_event_list()]
        event_list.append(types.KeyboardButton("Главное меню"))
        markup.add(*event_list)
        safe_send_message(message.from_user.id, '**Выберите тип мероприятия:**', parse_mode='Markdown', reply_markup=markup)

    elif message.text == 'Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        event = types.KeyboardButton("Мероприятия")
        route = types.KeyboardButton("Маршруты")
        pict_places = types.KeyboardButton("Живописные места")
        markup.add(event, route, pict_places)
        safe_send_message(message.from_user.id, type_event_mes, reply_markup=markup)

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
            'message_id': None,
            'has_photo': False
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
        safe_send_message(user_id, 'К сожалению, на ближайшие 30 дней мероприятий не найдено.')
        return
    
    data = events[current_index]

    if (data['description_summ'] == None) or (data['description_summ'] == ''):
        description_summ = generate_text_with_model(AI_prompt+data['description'])
        data['description_summ'] = description_summ
        update_event_data_safe(data['id'],description_summ=description_summ)

    event_type = state['event_type']
    
    # Получаем путь к изображению
    data_image = get_event_image_path(data['id'])
    
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
    
    # Формируем сообщение
    if event_type == 'Выставки':
        date_start = data['start_date']
        date_end = data['end_date']
        caption = f'''
*{data['title']}*

Время проведения: {date_start.strftime("%d.%m %H:%M")} - {date_end.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание (Сгенерировано ИИ):
{data['description_summ']}

[Купить билет]({data['website']})
'''
    else:
        date = data['start_date']
        caption = f'''
*{data['title']}*

Начало: {date.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание (Сгенерировано ИИ): 
{data['description_summ']}

[Купить билет]({data['website']})
'''
    
    # Для первого показа
    if first_time:
        if data_image and data_image.exists():
            # Пытаемся отправить фото
            with open(data_image, 'rb') as photo:
                sent_message = safe_send_photo(user_id, photo, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                state['message_id'] = sent_message.message_id
                state['has_photo'] = True
            else:
                # Если фото не отправилось, отправляем текст
                sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
                if sent_message:
                    state['message_id'] = sent_message.message_id
                    state['has_photo'] = False
        else:
            # Если фото нет, отправляем текст
            sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                state['message_id'] = sent_message.message_id
                state['has_photo'] = False
    else:
        # Для последующих показов (навигация)
        old_message_id = state.get('message_id')
        old_has_photo = state.get('has_photo', False)
        
        # Всегда отправляем новое сообщение и удаляем старое
        if data_image and data_image.exists():
            # Отправляем новое фото
            with open(data_image, 'rb') as photo:
                sent_message = safe_send_photo(user_id, open(data_image, 'rb'), caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                # Удаляем старое сообщение, если оно есть
                if old_message_id:
                    safe_delete_message(user_id, old_message_id)
                
                state['message_id'] = sent_message.message_id
                state['has_photo'] = True
            else:
                # Если фото не отправилось, отправляем текст
                sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
                if sent_message:
                    if old_message_id:
                        safe_delete_message(user_id, old_message_id)
                    state['message_id'] = sent_message.message_id
                    state['has_photo'] = False
        else:
            # Отправляем новый текст
            sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                # Удаляем старое сообщение, если оно есть
                if old_message_id:
                    safe_delete_message(user_id, old_message_id)
                
                state['message_id'] = sent_message.message_id
                state['has_photo'] = False

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

# Убедитесь, что запущен только один экземпляр бота
if __name__ == '__main__':
    try:
        print("Бот запущен...")
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        print("Убедитесь, что не запущено других экземпляров бота")
        time.sleep(5)