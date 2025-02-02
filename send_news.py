import smtplib
import schedule
import time
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Настройки Gmail SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "erichbchk@gmail.com"
app_password = "mqea aabg dgtl ankb"  # Замените на ваш App Password

# OpenAI API Key (замените на ваш ключ)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Данные получателя
receiver_email = "habibulline3@gmail.com"

# Функция генерации пяти важных новостей мира через OpenAI
def generate_world_news():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system", 
                "content": (
                    "Сгенерируй список из 5 самых важных новостей мира за последние 5 часов на английском языке. "
                    "Каждая новость должна быть краткой и оформлена как отдельный пункт списка. "
                    "Новостей должно быть ровно 5."
                )
            }]
        )
        news = response["choices"][0]["message"]["content"]
        return news.strip()
    except Exception as e:
        return f"Ошибка генерации новостей: {e}"

# Функция отправки письма с новостями
def send_email():
    subject = "Самые важные новости мира 🌍"
    body = generate_world_news()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Новости отправлены:\n", body)
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
    finally:
        server.quit()

# Запуск рассылки каждые 5 часов
schedule.every(5).hours.do(send_email)

print("📩 Рассылка запущена! Каждые 5 часов будет отправляться письмо с 5 важными новостями.")

# Бесконечный цикл для работы расписания
while True:
    schedule.run_pending()
    time.sleep(60)  # Проверяем расписание каждую минуту
