
import requests

TOKEN = "6736689012:AAFd_XEkmHpAGrGZnKZjARuPMWE64Prq4Dw"
CHAT_ID = "824040117"

def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print("Erro ao enviar mensagem:", e)
