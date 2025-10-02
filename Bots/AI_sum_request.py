import requests
import json
import tkinter as tk
from tkinter import filedialog
import base64
import mimetypes
import os
from urllib.parse import quote_plus

# --- API URLs ---
TEXT_MODELS_URL = "https://text.pollinations.ai/models"
IMAGE_MODELS_URL = "https://image.pollinations.ai/models"
TEXT_GENERATION_OPENAI_URL = "https://text.pollinations.ai/openai" # OpenAI compatible endpoint
IMAGE_GENERATION_BASE_URL = "https://image.pollinations.ai/prompt/"

# --- Helper Functions ---

# def fetch_models(url):
#     """Получает список моделей с указанного URL."""
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Вызовет исключение для плохих ответов (4xx or 5xx)
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе моделей: {e}")
#         return None

# def select_model_from_list(models_data, model_type="text"):
#     """
#     Позволяет пользователю выбрать модель из списка.
#     Для текстовых моделей 'models_data' - это список словарей.
#     Для моделей изображений 'models_data' - это список строк.
#     """
#     if not models_data:
#         print("Список моделей пуст или не удалось загрузить.")
#         return None

#     print(f"\nДоступные модели для {model_type}:")
#     model_type == "text"

#     return models_data[8]


def encode_image_to_base64(image_path):
    """Кодирует изображение в base64 строку."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Ошибка при кодировании изображения: {e}")
        return None

# --- Generation Functions ---

def generate_text_with_model(prompt):
    """Генерация текста с использованием выбранной модели."""

    model_name = 'openai-fast'

    image_path = None
    image_base64 = None
    mime_type = None

    # Формируем запрос в формате OpenAI
    messages = []
    if image_base64 and mime_type:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}
                }
            ]
        })
    else:
        messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_name,
        "messages": messages
        # Можно добавить другие параметры OpenAI, если API их поддерживает (temperature, max_tokens и т.д.)
        # "temperature": 0.7,
        # "max_tokens": 150
    }

    print("\nОтправка запроса...")
    try:
        response = requests.post(TEXT_GENERATION_OPENAI_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        api_response = response.json()

        # Парсинг ответа (стандартный для OpenAI)
        if api_response.get("choices") and len(api_response["choices"]) > 0:
            generated_text = api_response["choices"][0].get("message", {}).get("content")
            return generated_text
        else:
            print("\nНе удалось получить сгенерированный текст из ответа API.")
            print("Ответ API:", api_response)

    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса на генерацию текста: {e}")
    except json.JSONDecodeError:
        print("Ошибка: Не удалось декодировать JSON ответ от сервера.")
        print("Текст ответа:", response.text)
    print("-" * 30)

# --- Main Script Logic ---

# def main(prompt):
#     text_models = fetch_models(TEXT_MODELS_URL)
#     if text_models:
#         text = generate_text_with_model(prompt)
#     else:
#         print("Не удалось загрузить текстовые модели.")

# if __name__ == "__main__":
#     main()