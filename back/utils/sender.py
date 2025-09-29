import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailSender:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL

    async def send_email(self, to_email: str, subject: str, body: str):
        message = MIMEMultipart()
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.username,
            password=self.password,
            use_tls=True,
        )

    async def send_memorial_date_notification(self, memorial_date, users):
        """Отправка уведомления о памятной дате"""
        subject = f"Памятная дата: {memorial_date.title}"
        
        for user in users:
            body = f"""
            <html>
                <body>
                    <h2>Сегодня памятная дата: {memorial_date.title}</h2>
                    <p>{memorial_date.description}</p>
                    <p>Подробнее на нашем сайте: <a href="https://www.example.com/memorial-dates">www.example.com</a></p>
                    <hr>
                    <p><small>Это автоматическое уведомление. Отписаться можно в настройках профиля.</small></p>
                </body>
            </html>
            """
            
            try:
                await self.send_email(user.email, subject, body)
                print(f"Email sent to {user.email}")
            except Exception as e:
                print(f"Failed to send email to {user.email}: {e}")

email_sender = EmailSender()