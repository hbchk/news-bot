import smtplib
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Настройки Gmail SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "erichbchk@gmail.com"
app_password = os.getenv("SMTP_PASSWORD")  # Берем пароль из переменных окружения!

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Берем ключ API из переменных окружения!

# Данные получателя
receiver_email = "habibulline3@gmail.com"

# Функция генерации пяти важных новостей мира через OpenAI
def generate_world_news():
    print("📡 Генерация новостей...")
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
            }],
            timeout=10  # Таймаут 10 секунд
        )
        news = response["choices"][0]["message"]["content"]
        print("✅ Новости успешно сгенерированы!")
        return news.strip()
    except Exception as e:
        print(f"❌ Ошибка генерации новостей: {e}")
        return f"Ошибка генерации новостей: {e}"

# Функция отправки письма с новостями
def send_email():
    print("📨 Отправка письма...")
    subject = "Самые важные новости мира 🌍"
    body = generate_world_news()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)  # Таймаут на SMTP соединение
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Новости отправлены:\n", body)
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
    finally:
        server.quit()

# Запуск скрипта (ОДИН раз!)
if __name__ == "__main__":
    print("🚀 Старт send_news.py")
    send_email()
    print("🏁 Скрипт завершён!")
