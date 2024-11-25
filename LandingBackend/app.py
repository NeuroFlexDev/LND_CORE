from flask import Flask, request, jsonify
from flask_cors import CORS  # для разрешения CORS-запросов с фронтенда
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


app = Flask(__name__)
CORS(app, origins=["https://neuroflex.ru"])
# Настройки почты (заполните данными)
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 587

# Обработчик POST-запроса для отправки почты
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'message': 'Имя и почта обязательны!'}), 400

    # Формируем сообщение
    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = MAIL_USERNAME  # Получатель — это ваша почта
    msg['Subject'] = 'Новая заявка с контактной формы'

    body = f'Имя: {name}\nПочта: {email}'
    msg.attach(MIMEText(body, 'plain'))

    print(msg)

    try:
        # Отправка почты
        server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, MAIL_USERNAME, msg.as_string())
        server.close()
        return jsonify({'message': 'Заявка отправлена успешно!'}), 200
    except Exception as e:
        return jsonify({'message': f'Ошибка при отправке заявки: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
