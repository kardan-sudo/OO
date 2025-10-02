import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import psycopg2
from get_db import *
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
import random
import json
from message import *
from AI_sum_request import generate_text_with_model

TOKEN = "vk1.a.qW_YVau62neDdXBg1aw4lHM2-ZsCd9L1ioQj29whg3YnVy51-9mryuW6LpDb-qbEHV0JT4LSJylheCuU5QNriqSgHjUEHxsH3Q_tZX8-DZw9tsukboNj6Uen9PK4Lh9-anRDGZFzIlRiuOZ4VtRFW8RwzUmLBPd0PpfDg8cSlTX22qc0kH09B608udpaKFUbdhqeDxx8JwlPEFYLzoHPfg"
GROUP_ID = '233031631'


# Инициализация VK API
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

# Словарь для хранения состояния пользователей
user_states = {}

def get_event_image_path(event_id):
    """Получает путь к изображению мероприятия"""
    jpg_path = Path(f'/home/radmir/OO/back/static/events/{event_id}.jpg')
    if jpg_path.exists():
        return jpg_path
    
    jpeg_path = Path(f'/home/radmir/OO/back/static/events/{event_id}.jpeg')
    if jpeg_path.exists():
        return jpeg_path
    
    return None

def get_route_image_path(route_id):
    """Получает путь к изображению маршрута"""
    png_path = Path(f'/home/radmir/OO/back/static/routes/{route_id}.png')
    if png_path.exists():
        return png_path
    return None

def get_scenic_spot_image_path(spot_id):
    """Получает путь к изображению живописного места"""
    jpg_path = Path(f'/home/radmir/OO/back/static/scenic/{spot_id}.jpg')
    if jpg_path.exists():
        return jpg_path
    
    jpeg_path = Path(f'/home/radmir/OO/back/static/scenic/{spot_id}.jpeg')
    if jpeg_path.exists():
        return jpeg_path
    
    return None

def safe_send_message(user_id, text, keyboard=None, attachment=None):
    """Безопасная отправка сообщения"""
    try:
        params = {
            'user_id': user_id,
            'message': text,
            'random_id': random.randint(0, 2**63)
        }
        
        if keyboard:
            params['keyboard'] = keyboard
        if attachment:
            params['attachment'] = attachment
            
        return vk.messages.send(**params)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return None

def upload_photo(user_id, image_path):
    """Загружает фото на сервер VK и возвращает attachment"""
    try:
        # Получаем адрес сервера для загрузки
        upload_url = vk.photos.getMessagesUploadServer(peer_id=user_id)['upload_url']
        
        # Загружаем фото
        with open(image_path, 'rb') as photo_file:
            files = {'photo': photo_file}
            response = vk_session.http.post(upload_url, files=files)
        
        upload_result = response.json()
        
        # Сохраняем фото
        photo_data = vk.photos.saveMessagesPhoto(
            server=upload_result['server'],
            photo=upload_result['photo'],
            hash=upload_result['hash']
        )[0]
        
        return f"photo{photo_data['owner_id']}_{photo_data['id']}"
    except Exception as e:
        print(f"Ошибка при загрузке фото: {e}")
        return None

def create_main_keyboard():
    """Создает основную клавиатуру"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Мероприятия', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Маршруты', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Живописные места', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

def create_events_keyboard():
    """Создает клавиатуру для выбора типа мероприятий"""
    keyboard = VkKeyboard(one_time=False)
    events = get_event_list()
    for i, event in enumerate(events):
        if i > 0 and i % 2 == 0:
            keyboard.add_line()
        keyboard.add_button(event, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def create_routes_time_keyboard():
    """Создает клавиатуру для выбора времени маршрута"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('до 2 часов', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('до 3 часов', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('до 6 часов', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Неважно', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def create_routes_difficulty_keyboard():
    """Создает клавиатуру для выбора сложности маршрута"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Легкий', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Средний', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Тяжелый', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Любой', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def create_navigation_keyboard(current_index, total_count, content_type):
    """Создает инлайн-клавиатуру для навигации"""
    keyboard = VkKeyboard(inline=True)
    
    if current_index > 0:
        keyboard.add_callback_button('⬅️ Назад', color=VkKeyboardColor.SECONDARY, payload={'command': f'prev_{content_type}'})
    
    keyboard.add_callback_button(f'{current_index + 1}/{total_count}', color=VkKeyboardColor.PRIMARY, payload={'command': 'page'})
    
    if current_index < total_count - 1:
        keyboard.add_callback_button('Вперёд ➡️', color=VkKeyboardColor.SECONDARY, payload={'command': f'next_{content_type}'})
    
    return keyboard.get_keyboard()

def format_event_message(data):
    """Форматирует сообщение для мероприятия"""
    if data['event_type'] == 'Выставки':
        date_start = data['start_date']
        date_end = data['end_date']
        return f'''{data['title']}

Время проведения: {date_start.strftime("%d.%m %H:%M")} - {date_end.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание (Сгенерировано ИИ):
{data['description_summ']}

Ссылка на билеты: {data['website']}'''
    else:
        date = data['start_date']
        return f'''{data['title']}

Начало: {date.strftime("%d.%m %H:%M")}
Адрес: {data['address']}

Описание (Сгенерировано ИИ): 
{data['description_summ']}

Ссылка на билеты: {data['website']}'''

def format_route_message(data):
    """Форматирует сообщение для маршрута"""
    difficulty_emoji = {
        'easy': '🟢',
        'medium': '🟡', 
        'hard': '🔴'
    }
    
    emoji = difficulty_emoji.get(data['difficulty'], '⚪')
    
    return f'''{data['title']}

{emoji} Сложность: {data['difficulty'].capitalize() if data['difficulty'] else 'Не указана'}
⏱ Продолжительность: {data['duration_minutes']} минут

{data['description']}

Ссылка на маршрут: {data['url']}'''

def format_scenic_spot_message(data):
    """Форматирует сообщение для живописного места"""
    return f'''{data['title']}

{data['description']}
Время работы: {data['opening_hours']}

Стоимость: {data['entrance_fee']}

📍 Местоположение: {data['address']}'''

def send_item_message(user_id, caption, keyboard, data, item_type, first_time, state):
    """Отправляет сообщение с предметом"""
    # Получаем путь к изображению
    if item_type == 'event':
        image_path = get_event_image_path(data['id'])
    elif item_type == 'route':
        image_path = get_route_image_path(data['id'])
    else:  # scenic_spot
        image_path = get_scenic_spot_image_path(data['id'])
    
    attachment = None
    if image_path and image_path.exists():
        attachment = upload_photo(user_id, image_path)
    
    # Отправляем сообщение
    safe_send_message(user_id, caption, keyboard=keyboard, attachment=attachment)

def show_event_and_route(user_id, items, item_type='event', first_time=False):
    """Универсальная функция для отображения мероприятий, маршрутов и живописных мест"""
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
    keyboard = create_navigation_keyboard(current_index, len(items), item_type)
    
    # Формируем сообщение в зависимости от типа
    if item_type == 'event':
        caption = format_event_message(data)
    elif item_type == 'route':
        caption = format_route_message(data)
    else:  # scenic_spot
        caption = format_scenic_spot_message(data)
    
    # Отправка сообщения
    send_item_message(user_id, caption, keyboard, data, item_type, first_time, state)

def handle_message(user_id, text):
    """Обработчик текстовых сообщений"""
    text_lower = text.lower()
    
    if text_lower == 'старт' or text_lower == 'начать' or text_lower == 'вперёд!':
        safe_send_message(user_id, hello_mes, keyboard=create_main_keyboard())

    elif text_lower == 'мероприятия':
        safe_send_message(user_id, '**Выберите тип мероприятия:**', keyboard=create_events_keyboard())

    elif text_lower == 'главное меню':
        safe_send_message(user_id, type_event_mes, keyboard=create_main_keyboard())

    elif text_lower == 'маршруты':
        safe_send_message(user_id, 'Выберите продолжительность маршрута', keyboard=create_routes_time_keyboard())

    elif text_lower in ["до 2 часов", "до 3 часов", "до 6 часов", 'неважно']:
        time_dict = {
            "до 2 часов": 120,
            "до 3 часов": 180, 
            "до 6 часов": 300,
            "неважно": 0
        }
        
        if user_id not in user_states:
            user_states[user_id] = {}
        
        user_states[user_id]['route_time'] = time_dict[text_lower]
        user_states[user_id]['waiting_for_difficulty'] = True

        safe_send_message(user_id, 'Выберите сложность маршрута', keyboard=create_routes_difficulty_keyboard())

    elif text_lower == 'живописные места':
        scenic_spots = get_scenic_spots()
        
        user_states[user_id] = {
            'scenic_spots': scenic_spots,
            'current_index': 0,
            'content_type': 'scenic_spot'
        }
        
        show_event_and_route(user_id, scenic_spots, 'scenic_spot', first_time=True)

    elif text_lower in ["легкий", "средний", "тяжелый", 'любой']:
        difficulty_dict = {
            "легкий": "easy",
            "средний": "medium", 
            "тяжелый": "hard",
            "любой": "NULL"
        }
        
        if (user_id in user_states and 
            'route_time' in user_states[user_id] and 
            user_states[user_id].get('waiting_for_difficulty')):
            
            selected_time = user_states[user_id]['route_time']
            selected_difficulty = difficulty_dict[text_lower]
            
            routes = get_routes(selected_time, selected_difficulty)
            
            user_states[user_id] = {
                'routes': routes,
                'current_index': 0,
                'content_type': 'route'
            }
            
            show_event_and_route(user_id, routes, 'route', first_time=True)
            
            # Очищаем временные данные
            if 'route_time' in user_states[user_id]:
                del user_states[user_id]['route_time']
            if 'waiting_for_difficulty' in user_states[user_id]:
                del user_states[user_id]['waiting_for_difficulty']

    elif text_lower in ['концерты', 'спектакли', 'выставки']:
        data_events = get_event_data(text)
        filtered_events = []
        
        for data in data_events:
            if text_lower == 'выставки':
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
        
        user_states[user_id] = {
            'event_type': text_lower,
            'events': filtered_events,
            'current_index': 0,
            'content_type': 'event'
        }
        
        show_event_and_route(user_id, filtered_events, 'event', first_time=True)

    else:
        # Проверяем, есть ли у пользователя активное состояние с данными
        if user_id in user_states:
            # Если есть активное состояние, игнорируем неизвестные команды
            # чтобы не мешать навигации
            return
        else:
            safe_send_message(user_id, "Не понимаю команду. Используйте кнопки меню или напишите 'Старт'.")

def handle_callback(user_id, payload,event_id):
    """Обработчик callback-событий"""
    try:
        if user_id not in user_states:
            print(f"Пользователь {user_id} не найден в user_states")
            return
        
        state = user_states[user_id]
        command = payload.get('command', '')
        
        print(f"Обработка callback: {command} для пользователя {user_id}")
        
        # Определяем тип контента и данные
        if 'events' in state:
            items = state['events']
            content_type = 'event'
        elif 'routes' in state:
            items = state['routes']
            content_type = 'route'
        elif 'scenic_spots' in state:
            items = state['scenic_spots']
            content_type = 'scenic_spot'
        else:
            print(f"Нет данных для пользователя {user_id}")
            return
        
        if command.startswith('prev_'):
            if state['current_index'] > 0:
                state['current_index'] -= 1
                show_event_and_route(user_id, items, content_type, first_time=False)
                # Отправляем уведомление об успешном действии
                vk.messages.sendMessageEventAnswer(
                    event_id=event_id,
                    user_id=user_id,
                    peer_id=user_id,
                    event_data=json.dumps({'type': 'show_snackbar', 'text': '⬅️ Переход к предыдущему'})
                )
        
        elif command.startswith('next_'):
            if state['current_index'] < len(items) - 1:
                state['current_index'] += 1
                show_event_and_route(user_id, items, content_type, first_time=False)
                # Отправляем уведомление об успешном действии
                vk.messages.sendMessageEventAnswer(
                    event_id=event_id,
                    user_id=user_id,
                    peer_id=user_id,
                    event_data=json.dumps({'type': 'show_snackbar', 'text': '➡️ Переход к следующему'})
                )
        
        elif command == 'page':
            # Просто подтверждаем нажатие
            vk.messages.sendMessageEventAnswer(
                event_id=event_id,
                user_id=user_id,
                peer_id=user_id,
                event_data=json.dumps({'type': 'show_snackbar', 'text': f'Страница {state["current_index"] + 1} из {len(items)}'})
            )
            
    except Exception as e:
        print(f"Ошибка в handle_callback: {e}")

def main():
    """Основная функция бота"""
    print("Бот VK запущен...")
    
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message
                user_id = message['from_id']
                text = message['text']
                
                print(f"Сообщение от {user_id}: {text}")
                handle_message(user_id, text)
                
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                user_id = event.object.user_id
                payload = event.object.payload
                event_id = event.object.event_id
                
                print(f"Callback от {user_id}: {payload}")
                handle_callback(user_id, payload, event_id)
                
        except Exception as e:
            print(f"Ошибка при обработке события: {e}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        time.sleep(5)