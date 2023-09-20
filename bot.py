import requests
import time
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()
def fetch_data():
    response = requests.get("https://blaze.com/api/roulette_games/recent")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar dados: {response.status_code}")
        return None

def send_telegram_message(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Erro ao enviar mensagem para o Telegram: {response.content}")

def check_colors(data, last_alert_count, last_alert_color, martigale_count):
    colors = [item['color'] for item in data]
    current_color = colors[0]
    count = 0

    for color in colors:
        if color == current_color:
            count += 1
        else:
            break

    if count >= 5 and (count != last_alert_count or current_color != last_alert_color):
        last_alert_count = count
        last_alert_color = current_color

        symbol, opposite_symbol = ("🟥", "⬛") if current_color == 1 else ("⬛", "🟥")
        martigale_stage = count - 5  # Calcula a etapa do Martigale

        message = f"⚠️ ===== Alerta! ===== ⚠️\n A cor {symbol} foi repetida {count} vezes seguidas.\n\n Entre com {opposite_symbol} na próxima rodada! \n\n {martigale_stage} Martigale 💥"
        print(message)
        send_telegram_message(message)
        martigale_count += 1
    elif current_color != last_alert_color and martigale_count > 0:
        message = f"==== ✅ {martigale_count}x1 WIN ✅ ===="
        print(message)
        send_telegram_message(message)
        martigale_count = 0  # Reset martigale_count

    return last_alert_count, last_alert_color, martigale_count

def main():
    last_checked_time = 0
    last_alert_count = 0
    last_alert_color = None
    martigale_count = 0

    while True:
        if time.time() - last_checked_time > 5:
            last_checked_time = time.time()
            data = fetch_data()
            if data:
                last_alert_count, last_alert_color, martigale_count = check_colors(data, last_alert_count, last_alert_color, martigale_count)

if __name__ == "__main__":
    main()

