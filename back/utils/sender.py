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
                
    async def send_request_approved_notification(self, user_email: str, user_name: str, position: str, organization: str):
        """Отправка уведомления о подтверждении заявки"""
        subject = "Ваша заявка на представительство подтверждена"
        
        body = f"""
        <html>
            <body>
                <h2>Уважаемый(ая) {user_name}!</h2>
                <p>Ваша заявка на представительство была подтверждена.</p>
                <p><strong>Должность:</strong> {position}</p>
                <p><strong>Организация:</strong> {organization}</p>
                <p>Теперь вы имеете права представителя в нашей системе.</p>
                <hr>
                <p><small>Это автоматическое уведомление. Пожалуйста, не отвечайте на это письмо.</small></p>
            </body>
        </html>
        """
        
        try:
            await self.send_email(user_email, subject, body)
            print(f"Approval email sent to {user_email}")
        except Exception as e:
            print(f"Failed to send approval email to {user_email}: {e}")
    
    async def send_request_rejected_notification(self, user_email: str, user_name: str):
        """Отправка уведомления об отклонении заявки"""
        subject = "Ваша заявка на представительство отклонена"
        
        body = f"""
        <html>
            <body>
                <h2>Уважаемый(ая) {user_name}!</h2>
                <p>К сожалению, ваша заявка на представительство была отклонена.</p>
                <p>Если вы считаете, что это произошло по ошибке, пожалуйста, свяжитесь с администрацией.</p>
                <hr>
                <p><small>Это автоматическое уведомление. Пожалуйста, не отвечайте на это письмо.</small></p>
            </body>
        </html>
        """
        
        try:
            await self.send_email(user_email, subject, body)
            print(f"Rejection email sent to {user_email}")
        except Exception as e:
            print(f"Failed to send rejection email to {user_email}: {e}")

email_sender = EmailSender()