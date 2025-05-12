
from flask import Flask, request, render_template
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_FOLDER = 'audios'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return 'No audio file', 400

    audio = request.files['audio']
    existing = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.webm')]
    num = len(existing) + 1
    filename = f"audio-{num:03}.webm"
    path = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(path)

    send_email_with_attachment(path, filename)
    return 'OK', 200

def send_email_with_attachment(filepath, filename):
    EMAIL_FROM = os.getenv('EMAIL_FROM')
    EMAIL_TO = os.getenv('EMAIL_TO')
    EMAIL_PASS = os.getenv('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'Novo áudio anónimo'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content(f'Foi enviado um novo áudio: {filename}')

    with open(filepath, 'rb') as f:
        msg.add_attachment(f.read(), maintype='audio', subtype='webm', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASS)
        smtp.send_message(msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
