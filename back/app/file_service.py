import aiofiles
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
from typing import Optional

class FileService:
    def __init__(self):
        self.events_photos_dir = Path('/home/flymalysh/Рабочий стол/sbp/OO/back/static/events/')
    
    async def save_event_photo(self, event_id: int, photo: UploadFile) -> bool:
        """Сохраняет фото мероприятия"""
        try:
            # Проверяем тип файла
            if not photo.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File must be an image"
                )
            
            # Формируем путь к файлу
            filename = f"{event_id}.jpeg"  # Исправлено: .jpg
            file_path = self.events_photos_dir + filename
            
            # Читаем и сохраняем файл
            contents = await photo.read()
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(contents)
            
            return True
            
        except Exception as e:
            print(f"Error saving photo: {e}")
            return False
    
    def get_event_photo_path(self, event_id: int) -> Optional[Path]:
        """Возвращает путь к фото мероприятия если оно существует"""
        filename = f"{event_id}.jpeg"  # Исправлено: .jpg
        file_path = self.events_photos_dir / filename
        return file_path if file_path.exists() else None

file_service = FileService()
