import smtplib
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Отладочная функция для проверки переменных окружения
def debug_env():
    print("DEBUG: Проверка переменных окружения:")
    print("EMAIL:", "SET" if os.getenv("EMAIL") else "NOT SET")
    print("SMTP_PASSWORD:", "SET" if os.getenv("SMTP_PASSWORD") else "NOT SET")
    print("OPENAI_API_KEY:", "SET" if os.getenv("OPENAI_API_KEY") else "NOT SET")
    print("RECEIVER_EMAIL:", "SET" if os.getenv("RECEIVER_EMAIL") else "NOT SET")

# Выводим отладочную информацию
debug_env()

# Настройки Gmail SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = os.getenv("EMAIL")             # Из GitHub Secrets: EMAIL = erichbchk@gmail.com
app_password = os.getenv("SMTP_PASSWORD")       # Из GitHub Secrets: SMTP_PASSWORD = mqea aabg dgtl ankb

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")      # Из GitHub Secrets: OPENAI_API_KEY = sk-proj-...

# Данные получателя
receiver_email = os.getenv("RECEIVER_EMAIL")      # Из GitHub Secrets: RECEIVER_EMAIL = habibulline3@gmail.com

# Проверяем, что все переменные заданы
if not sender_email or not app_password or not receiver_email or not openai.api_key:
    print("❌ Ошибка: Не заданы все необходимые переменные окружения!")
    exit(1)

# Функция генерации новостей
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

# Функция отправки письма
def send_email():
    print(f"📨 Отправка письма от {sender_email} к {receiver_email}...")
    subject = "Самые важные новости мира 🌍"
    body = generate_world_news()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Новости успешно отправлены!")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
    finally:
        server.quit()

# Запуск скрипта
if __name__ == "__main__":
    print("🚀 Запуск send_news.py")
    send_email()
    print("🏁 Скрипт завершён!")
