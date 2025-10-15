import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot

# -----------------------
# 사용자 설정
# -----------------------
BOT_TOKEN = "8258926638:AAEYxFGOYyx-fY2BepvTKYhrR8tAlpuV7-4"  # ← 본인 봇 토큰
CHAT_ID = 5489253375        # ← 아까 확인한 Chat ID
CHECK_INTERVAL = 30  # 초 단위 (30초마다 확인)

# 감시할 자리별 URL 리스트 (10월 24일로 변경)
URLS = [
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489708?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489708?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489636?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489703?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489628?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489623?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489617?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489606?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489664?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489654?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489646?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489639?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489597?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489586?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489582?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489574?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489569?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489555?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489546?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489541?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489534?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489527?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489518?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489512?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5489488?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
    "https://m.booking.naver.com/booking/12/bizes/1033312/items/5487627?area=ple&lang=ko&startDateTime=2025-10-24T00%3A00%3A00%2B09%3A00&theme=place",
]

# -----------------------
# 텔레그램 봇 초기화
# -----------------------
bot = Bot(token=BOT_TOKEN)

# -----------------------
# 자리 활성화 확인 함수
# -----------------------
def is_slot_available(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"사이트 요청 실패 ({url}): {e}")
        return False

    soup = BeautifulSoup(res.text, "html.parser")
    button = soup.find("button", string="오후 6:00")
    if button and "disabled" not in button.attrs:
        return True
    return False

# -----------------------
# 텔레그램 알림 함수
# -----------------------
def send_telegram(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

# -----------------------
# 메인 루프
# -----------------------
print("예약 감시 시작 (10월 24일)...")
while True:
    for url in URLS:
        if is_slot_available(url):
            send_telegram(f"🎉 예약 가능! {url}")
            print(f"알림 전송 완료: {url}")
        else:
            print(f"예약 불가: {url}")
    time.sleep(CHECK_INTERVAL)
