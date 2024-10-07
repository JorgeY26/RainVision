# Importar las librerías necesarias
from flask import Flask, request, jsonify
from twilio.rest import Client
from pyngrok import ngrok
import threading

# Configurar Twilio con tu account_sid y auth_token
account_sid = 'ACf556fbcd861665a5c9860e45ddd1019a'
auth_token = '8998b8c91e49a0150a645be8903ddad2'
client = Client(account_sid, auth_token)

app = Flask(__name__)  # Aquí corregí el error de _name_

# Función para enviar el mensaje de WhatsApp con imagen
def send_text_message_with_image(sender, message, media_url=None):
    try:
        msg = client.messages.create(
            from_="whatsapp:+14155238886",  # El número de Twilio
            body=message,
            media_url=media_url,  # URL de la imagen (opcional)
            to=f"whatsapp:+{sender}"  # Número de WhatsApp del destinatario
        )
        print(f"Mensaje enviado correctamente, SID: {msg.sid}")
        return True
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        return False

# Ruta para manejar la solicitud POST de Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_message = request.form['Body']  # Obtener el mensaje recibido
    sender_number = request.form['From']  # Obtener el número del remitente

    print(f"Mensaje recibido de {sender_number}: {incoming_message}")

    # Aquí puedes decidir qué respuesta enviar
    response_message = f"Recibí tu mensaje: '{incoming_message}'"
    print(f"Enviando respuesta: {response_message}")  # Imprimir el mensaje de respuesta en el terminal
    send_text_message_with_image(sender_number.split(":")[1], response_message, None)  # Responder al remitente

    return jsonify({"ok": True}), 200

# Lista de zonas en la provincia del Carchi
zonas = [
    "1. Zona de Tulcán",
    "2. Zona de Bolívar",
    "3. Zona de Mira",
    "4. Zona de San Pedro de Huaca",
    "5. Zona de El Chical",
    "6. Zona de La Paz",
    "7. Zona de Huaca",
    "8. Zona de Montúfar",
    "9. Zona de Cumbal",
    "10. Zona de Espejo",
    "11. Zona de La Libertad",
    "12. Zona de El Ángel"
]

# Mensaje inicial que se enviará al comenzar
initial_message = "Buen día, se mostrará un listado de zonas en la provincia del Carchi que están en la zona de predicción de lluvias para mejorar el cultivo de papa:\n" + "\n".join(zonas)

# URL de la imagen a enviar
media_url = 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'

# Función para iniciar el servidor Flask
def run_app():
    app.run(port=3000)

# Ejecutar el envío de mensaje directamente en el script
if __name__ == "__main__":  # Aquí corregí el error de _name_
    to_whatsapp_number = '593980093156'  # Cambia esto por tu número de WhatsApp

    # Enviar el mensaje inicial con la imagen
    send_text_message_with_image(to_whatsapp_number, initial_message, media_url)

    # Exponer el puerto de Flask a través de ngrok
    public_url = ngrok.connect(3000)
    print(f"Ngrok URL: {public_url}")

    # Iniciar el servidor Flask en un hilo
    threading.Thread(target=run_app).start()
