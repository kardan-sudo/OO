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
    jpg_path = Path(f'/home/radmir/OO/back/static/events/{event_id}.jpg')
    if jpg_path.exists():
        return jpg_path
    
    # Затем проверяем jpeg
    jpeg_path = Path(f'/home/radmir/OO/back/static/events/{event_id}.jpeg')
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

    elif message.text == 'Маршруты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        two_hour = types.KeyboardButton("до 2 часов")
        three_hour = types.KeyboardButton("до 3 часов")
        greate_three = types.KeyboardButton("до 6 часов")
        allin = types.KeyboardButton('Неважно')
        menu = types.KeyboardButton("Главное меню")
        markup.add(two_hour,three_hour, greate_three, allin, menu)
        safe_send_message(message.from_user.id, 'Выберите продолжительность маршрута', reply_markup=markup)

    elif message.text in ["до 2 часов", "до 3 часов", "до 6 часов", 'Неважно']:
        time_dict = {"до 2 часов": 120,
                     "до 3 часов": 180,
                     "до 6 часов": 300,
                     "Неважно": 0
                     }
        

        user_id = message.from_user.id
        if user_id not in user_states:
            user_states[user_id] = {}
        
        user_states[user_id]['route_time'] = time_dict[message.text]
        user_states[user_id]['waiting_for_difficulty'] = True

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        two_hour = types.KeyboardButton("Легкий")
        three_hour = types.KeyboardButton("Средний")
        greate_three = types.KeyboardButton("Тяжелый")
        allin = types.KeyboardButton('Неважно')
        menu = types.KeyboardButton("Главное меню")
        markup.add(two_hour,three_hour, greate_three, allin, menu)
        safe_send_message(message.from_user.id, 'Выберите сложность маршрута', reply_markup=markup)

    elif message.text in ["Легкий", "Средний", "Тяжелый", 'Неважно']:
        difficulty_dict = {
            "Легкий": "easy",
            "Средний": "medium", 
            "Тяжелый": "hard",
            "Неважно": "NULL"
        }
        
        user_id = message.from_user.id

        if (user_id in user_states and 
            'route_time' in user_states[user_id] and 
            user_states[user_id].get('waiting_for_difficulty')):
            
            selected_time = user_states[user_id]['route_time']
            selected_difficulty = difficulty_dict[message.text]
            
            # Выполняем поиск по двум параметрам
            routes = get_routes(selected_time, selected_difficulty)
            
            # Сохраняем в состояние
            user_states[user_id] = {
                'routes': routes,
                'current_index': 0,
                'message_id': None,
                'has_photo': False,
                'content_type': 'route'  # Тип контента - маршрут
            }
            
            # Показываем результаты
            show_event_and_route(user_id, routes, 'route', first_time=True)
            
            # Очищаем временное состояние
            user_states[user_id].pop('route_time', None)
            user_states[user_id].pop('waiting_for_difficulty', None)

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
        show_event_and_route(user_id, filtered_events, 'event', first_time=True)

def format_event_message(data):
    """Форматирует сообщение для мероприятия"""
    if data['event_type'] == 'Выставки':
        date_start = data['start_date']
        date_end = data['end_date']
        return f'''
*{data['title']}*

Время проведения: {date_start.strftime("%d.%m %H:%M")} - {date_end.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание (Сгенерировано ИИ):
{data['description_summ']}

[Купить билет]({data['website']})
'''
    else:
        date = data['start_date']
        return f'''
*{data['title']}*

Начало: {date.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание (Сгенерировано ИИ): 
{data['description_summ']}

[Купить билет]({data['website']})
'''

def format_route_message(data):
    """Форматирует сообщение для маршрута"""
    difficulty_emoji = {
        'easy': '🟢',
        'medium': '🟡', 
        'hard': '🔴'
    }
    
    emoji = difficulty_emoji.get(data['difficulty'], '⚪')
    
    return f'''
*{data['title']}*

{emoji} Сложность: {data['difficulty'].capitalize() if data['difficulty'] else 'Не указана'}
⏱ Продолжительность: {data['duration_minutes']} минут

{data['description']}

[В путь!]({data['url']})
'''


# Функция для получения изображения маршрута (аналогично мероприятиям)
def get_route_image_path(route_id):
    """Получает путь к изображению маршрута"""
    jpg_path = Path(f'/home/radmir/OO/back/static/routes/{route_id}.png')
    if jpg_path.exists():
        return jpg_path
    
    jpeg_path = Path(f'/home/radmir/OO/back/static/routes/{route_id}.png')
    if jpeg_path.exists():
        return jpeg_path
    
    return None


def send_item_message(user_id, caption, markup, data, item_type, first_time, state):
    """Отправляет сообщение с предметом (мероприятие/маршрут)"""
    # Получаем путь к изображению
    if item_type == 'event':
        data_image = get_event_image_path(data['id'])
    else:  # route
        data_image = get_route_image_path(data['id'])  # Нужно создать эту функцию
    
    # Для первого показа
    if first_time:
        if data_image and data_image.exists():
            with open(data_image, 'rb') as photo:
                sent_message = safe_send_photo(user_id, photo, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                state['message_id'] = sent_message.message_id
                state['has_photo'] = True
            else:
                sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
                if sent_message:
                    state['message_id'] = sent_message.message_id
                    state['has_photo'] = False
        else:
            sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                state['message_id'] = sent_message.message_id
                state['has_photo'] = False
    else:
        # Для последующих показов
        old_message_id = state.get('message_id')
        
        if data_image and data_image.exists():
            with open(data_image, 'rb') as photo:
                sent_message = safe_send_photo(user_id, photo, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                if old_message_id:
                    safe_delete_message(user_id, old_message_id)
                state['message_id'] = sent_message.message_id
                state['has_photo'] = True
            else:
                sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
                if sent_message:
                    if old_message_id:
                        safe_delete_message(user_id, old_message_id)
                    state['message_id'] = sent_message.message_id
                    state['has_photo'] = False
        else:
            sent_message = safe_send_message(user_id, caption, parse_mode='Markdown', reply_markup=markup)
            if sent_message:
                if old_message_id:
                    safe_delete_message(user_id, old_message_id)
                state['message_id'] = sent_message.message_id
                state['has_photo'] = False


def show_event_and_route(user_id, items, item_type='event', first_time=False):
    """
    Универсальная функция для отображения мероприятий и маршрутов
    
    Args:
        user_id: ID пользователя
        items: список мероприятий/маршрутов
        item_type: 'event' или 'route'
        first_time: первый ли показ
    """
    if user_id not in user_states:
        return

    state = user_states[user_id]
    current_index = state['current_index']
    
    if not items:
        safe_send_message(user_id, 'К сожалению, ничего не найдено.')
        return
    
    data = items[current_index]

    # Для мероприятий генерируем описание если нужно
    if item_type == 'event':
        if (data['description_summ'] is None) or (data['description_summ'] == ''):
            description_summ = generate_text_with_model(AI_prompt + data['description'])
            data['description_summ'] = description_summ
            update_event_data_safe(data['id'], description_summ=description_summ)

    # Создаем клавиатуру для навигации
    markup = types.InlineKeyboardMarkup()
    
    # Добавляем кнопки навигации
    nav_buttons = []
    if current_index > 0:
        nav_buttons.append(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'prev_{item_type}'))
    
    nav_buttons.append(types.InlineKeyboardButton(f'{current_index + 1}/{len(items)}', callback_data='page'))
    
    if current_index < len(items) - 1:
        nav_buttons.append(types.InlineKeyboardButton('Вперёд ➡️', callback_data=f'next_{item_type}'))
    
    markup.row(*nav_buttons)
    
    # Формируем сообщение в зависимости от типа
    if item_type == 'event':
        caption = format_event_message(data)
    else:  # route
        caption = format_route_message(data)
    
    # Отправка сообщения
    send_item_message(user_id, caption, markup, data, item_type, first_time, state)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = call.data
    
    if user_id not in user_states:
        bot.answer_callback_query(call.id, "Сессия устарела. Выберите заново.")
        return
    
    state = user_states[user_id]
    
    # Автоматически определяем тип контента по наличию данных
    if 'events' in state:
        items = state['events']
        content_type = 'event'
    elif 'routes' in state:
        items = state['routes']
        content_type = 'route'
    else:
        bot.answer_callback_query(call.id, "Данные не найдены")
        return
    
    if data.startswith('prev_'):
        if state['current_index'] > 0:
            state['current_index'] -= 1
            show_event_and_route(user_id, items, content_type, first_time=False)
        bot.answer_callback_query(call.id)
    
    elif data.startswith('next_'):
        if state['current_index'] < len(items) - 1:
            state['current_index'] += 1
            show_event_and_route(user_id, items, content_type, first_time=False)
        bot.answer_callback_query(call.id)
    
    elif data == 'page':
        bot.answer_callback_query(call.id, f"Страница {state['current_index'] + 1} из {len(items)}")

# Убедитесь, что запущен только один экземпляр бота
if __name__ == '__main__':
    try:
        print("Бот запущен...")
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        print("Убедитесь, что не запущено других экземпляров бота")
        time.sleep(5)