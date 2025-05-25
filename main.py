import tkinter as tk
import calculate
import api

menu_items = {
    "아메리카노": 4000,
    "카페라떼": 4500,
    "카푸치노": 4800
}

# 환율 미리 불러오기
usd_rate = api.get_exchange_rate('USD')

def add_item(name, price):
    sum.add_to_cart(name, price)
    status_label.config(text=f"{name} 추가됨!")

def show_total():
    total = calculate.get_total_price()
    if usd_rate:
        usd_total = round(total * usd_rate, 2)
        status_label.config(text=f"총 금액: {total}원 (약 ${usd_total})")
    else:
        status_label.config(text=f"총 금액: {total}원 (환율 정보 없음)")

# tkinter UI 설정
window = tk.Tk()
window.title("카페 키오스크")
window.geometry("320x400")

tk.Label(window, text="📋 메뉴판", font=("Arial", 16)).pack(pady=10)

# 메뉴 버튼 만들기
for name, price in menu_items.items():
    if usd_rate:
        usd_price = round(price * usd_rate, 2)
        text = f"{name} - {price}원 (약 ${usd_price})"
    else:
        text = f"{name} - {price}원"
    
    btn = tk.Button(window, text=text, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

# 총 금액 보기 버튼
tk.Button(window, text="총 금액 보기", command=show_total).pack(pady=10)

# 상태 메시지 표시 라벨
status_label = tk.Label(window, text="", fg="blue")
status_label.pack(pady=20)

# 환율 안내 문구
if usd_rate:
    tk.Label(window, text=f"※ 환율: 1원 ≈ ${usd_rate:.5f}", fg="gray").pack()
else:
    tk.Label(window, text="※ 환율 정보를 불러올 수 없습니다.", fg="red").pack()

window.mainloop()
