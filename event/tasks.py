from celery import shared_task
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

load_dotenv()

def handle_name(name:str) -> str:
        words = name.split()
        first_name = ''
        last_name = ''
        acronym = ''
        for i, word in enumerate(words):
            if i == 0:
                first_name = word
                continue
        
            if i == len(words) - 1:
                last_name = word
                continue
            
            acronym += f'{word[0].upper()}. '
        
        return f'{first_name} {acronym}{last_name}'
    
def generate_invitation(name: str) -> bytes:
    img = Image.open("static/imgs/convite.png")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 60)

    name = handle_name(name)
    draw.text((930, 1025), name, fill="white", font=font)
    
    img = img.resize((500, 400), Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.read()
    

@shared_task
def send_email(name: str, recipient: str):
    server_smtp = 'smtp.gmail.com'
    port = 587
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    server = smtplib.SMTP(server_smtp, port)
    server.starttls()
    server.login(user, password)
    
    image_bytes = generate_invitation(name)

    msg = MIMEMultipart("related")
    msg["Subject"] = "Convite para o Maior Evento"
    msg["From"] = user
    msg["To"] = recipient

    html = """
    <html>
        <body>
            <h2>Parabéns por tomar essa decisão!</h2>
            <p>Você está convidado para o maior evento.</p>
            <img src="cid:convite">
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    image = MIMEImage(image_bytes, "png")
    image.add_header("Content-ID", "<convite>")
    image.add_header("Content-Disposition", "inline", filename="convite.png")

    msg.attach(image)

    server.send_message(msg)
    server.quit()