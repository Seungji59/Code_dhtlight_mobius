import requests, json, time, uuid
from gpiozero import LED
from gpiozero.pins.lgpio import LGPIOFactory

# =========================================================
# GPIO 설정 (BCM 18번 핀)
# =========================================================
factory = LGPIOFactory()
led = LED(18, pin_factory=factory)

led.off()
print("초기 상태: LED OFF (기존 la 무시)")

# =========================================================
# Mobius 설정 정보
# =========================================================
MOBIUS_BASE = "http://localhost:7599/Mobius"
AE_NAME = "FAN_AE"
CNT_NAME = "CMD"
ORIGINATOR = "SM2"

def headers():
    """oneM2M 요청용 공통 HTTP 헤더 생성"""
    return {
        "Accept": "application/json",
        "X-M2M-RI": str(uuid.uuid4()),   # 요청 고유 ID
        "X-M2M-Origin": ORIGINATOR,     # originator
        "X-M2M-RVI": "4",               # oneM2M 버전
    }

def get_latest_cin():
    """
    CMD 컨테이너의 최신 CIN(/la) 조회
    성공 시 m2m:cin 반환, 실패 시 None 반환
    """
    url = f"{MOBIUS_BASE}/{AE_NAME}/{CNT_NAME}/la"
    r = requests.get(url, headers=headers(), timeout=3)

    if r.status_code != 200:
        print(f"[Mobius] GET la failed: {r.status_code}")
        return None

    return r.json().get("m2m:cin", {})

# =========================================================
# 시작 시 기존 최신 CIN은 기준값으로만 저장 (실행 안 함)
# =========================================================
last_ri = None
try:
    cin0 = get_latest_cin()
    if cin0:
        last_ri = cin0.get("ri")
        print("시작 기준 ri 저장:", last_ri)
except Exception as e:
    print("초기 la 조회 실패:", e)

print("[*] Fan -> LED control started (새 CIN만 반응)")

# =========================================================
# 메인 루프 : 새로운 CIN이 생성될 때만 LED 제어
# =========================================================
while True:
    try:
        cin = get_latest_cin()
        if not cin:
            time.sleep(0.5)
            continue

        ri = cin.get("ri")

        # 이전과 동일한 CIN이면 무시
        if not ri or ri == last_ri:
            time.sleep(0.5)
            continue

        # 새로운 CIN 도착
        last_ri = ri

        con = cin.get("con")

        # con은 문자열(JSON) 형태이므로 파싱
        if isinstance(con, str):
            try:
                con = json.loads(con)
            except json.JSONDecodeError:
                print("con JSON 파싱 실패:", con)
                time.sleep(0.5)
                continue

        if not isinstance(con, dict):
            print("con 형식 오류:", con)
            time.sleep(0.5)
            continue

        fan = con.get("fan")

        # fan 값에 따라 LED 제어
        if fan in ["on", 1, "1", True]:
            led.on()
            print("NEW fan=on  -> LED ON")

        elif fan in ["off", 0, "0", False]:
            led.off()
            print("NEW fan=off -> LED OFF")

        else:
            print("알 수 없는 fan 값:", fan)

    except Exception as e:
        print("runtime error:", e)

    time.sleep(0.5)
