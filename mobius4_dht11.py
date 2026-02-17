import requests, json, time, uuid
import board, adafruit_dht

# =========================================================
# Mobius 설정 정보
# =========================================================
MOBIUS_BASE = "http://localhost:7599/Mobius"
AE_NAME = "DHT_AE"
CNT_NAME = "DATA"
ORIGINATOR = "SM"

# =========================================================
# DHT11 센서 설정 (BCM D8 핀)
# =========================================================
dht = adafruit_dht.DHT11(board.D8)

# CIN 업로드 URL 구성
cin_url = f"{MOBIUS_BASE}/{AE_NAME}/{CNT_NAME}"

# HTTP 세션 재사용 (연결 효율 향상)
session = requests.Session()

def headers():
    """
    oneM2M CIN 생성 요청용 HTTP 헤더
    ty=4 → CIN 생성
    """
    return {
        "Accept": "application/json",
        "X-M2M-RI": str(uuid.uuid4()),   # 요청 고유 ID
        "X-M2M-Origin": ORIGINATOR,     # originator
        "X-M2M-RVI": "4",               # oneM2M 버전
        "Content-Type": "application/json;ty=4"
    }

print("[*] DHT11 -> Mobius CIN uploader")
print("    URL:", cin_url)

# =========================================================
# 메인 루프 : 5초마다 온습도 값을 Mobius에 업로드
# =========================================================
try:
    while True:
        try:
            # 센서 값 읽기
            t = dht.temperature
            h = dht.humidity

            # 센서 오류 또는 None 값이면 재시도
            if t is None or h is None:
                time.sleep(0.2)
                continue

            # Mobius에 업로드할 payload 구성
            payload = {
                "m2m:cin": {
                    "con": json.dumps({
                        "temp": float(t),
                        "hum": float(h)
                    })
                }
            }

            # CIN 생성 요청
            r = session.post(cin_url, headers=headers(), json=payload, timeout=5)

            # 결과 출력
            if r.status_code == 201:
                print(f"[OK] Temp:{t}C  Hum:{h}%")
            else:
                print(f"[WARN] {r.status_code} - {r.text[:200]}")

        except RuntimeError:
            pass

        time.sleep(5)

# =========================================================
# 프로그램 종료 시 센서 정리
# =========================================================
finally:
    try:
        dht.exit()
    except Exception:
        pass

