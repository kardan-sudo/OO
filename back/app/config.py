from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Настройки базы данных
    database_url: str = "postgresql://user:password@localhost:5432/sbp"  # Значение по умолчанию

    # Настройки SMTP (для email_sender)
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your_username"
    SMTP_PASSWORD: str = "your_password"
    FROM_EMAIL: str = "noreply@example.com"

    class Config:
        env_file = ".env"  # Загружает из .env файла


settings = Settings()
