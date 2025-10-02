from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Настройки базы данных
    database_url: str = "postgresql://user:password@localhost:5432/sbp"  # Значение по умолчанию

    # Настройки SMTP (для email_sender)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "mannanovr70@gmail.com"
    SMTP_PASSWORD: str = "oafd mldn jpqj lgxk"
    FROM_EMAIL: str = "noreply@example.com"

    class Config:
        env_file = ".env"  # Загружает из .env файла


settings = Settings()
