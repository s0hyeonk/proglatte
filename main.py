
import tkinter as tk
import importlib
import cal
importlib.reload(cal)

import order
order.connect_db()

import api

import admin

caffee_items = {
    "아메리카노": 4500,
    "에스프레소": 4000,
    "카페라떼": 5000,
    "카푸치노": 5200,
}

ade_items = {
    "레몬에이드": 4000,
    "자몽에이드": 5500,
    "청포도에이드": 5500,
    "유자에이드": 5000,
}

juce_items = {
    "딸기주스": 6000,
    "사과주스": 6000,
    "오렌지주스": 6000,
    "포도주스": 6000
}


usd_rate = api.get_exchange_rate('USD')
if not usd_rate:
    print("환율 정보를 가져올 수 없었습니다.")

def add_item(name, price):
    cal.add_to_cart(name, price)
    qty = cal.cart[name][0] 
    status_label.config(text=f"{name} 추가됨! (수량: {qty})")

def show_total():
    total = cal.get_total_price()
    usd_rate = api.get_exchange_rate("USD") 
    
    if usd_rate:
        usd_total = round(total * usd_rate, 2)
        status_label.config(text=f"총 금액: {total}원 (약 ${usd_total})")
    else:
        status_label.config(text=f"총 금액: {total}원 (환율 정보 없음)")

window = tk.Tk()
window.title("카페 키오스크")
window.geometry("1920x1080")

tk.Label(window, text="M e n u", font=("Arial", 80)).pack(pady=10)

tk.Label(window, text="caffee", anchor="w", font=("Arial", 40)).pack(pady=0, padx=100, fill="x")
tk.Frame(window, width=340, height=1, bg="black").pack(padx=10, pady=5)

for name, price in caffee_items.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = round(price * usd_rate, 2)
        text = f"{name}                                      {price}원 (약 ${usd_price})"
    else:
        text = f"{name}                                                        {price}원"
    
    btn = tk.Button(window, text=text, font=20, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

tk.Label(window, text="ade", anchor="w", font=("Arial", 40)).pack(pady=0, padx=100, fill="x")
tk.Frame(window, width=340, height=1, bg="black").pack(padx=10, pady=5)

for name, price in ade_items.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = round(price * usd_rate, 2)
        text = f"{name}                                      {price}원 (약 ${usd_price})"
    else:
        text = f"{name}                                                        {price}원"
    
    btn = tk.Button(window, text=text, font=20, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

tk.Label(window, text="juce", anchor="w", font=("Arial", 40)).pack(pady=0, padx=100, fill="x")
tk.Frame(window, width=340, height=1, bg="black").pack(padx=10, pady=5)
for name, price in juce_items.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = round(price * usd_rate, 2)
        text = f"{name}                                      {price}원 (약 ${usd_price})"
    else:
        text = f"{name}                                                        {price}원"
    
    btn = tk.Button(window, text=text, font=20, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)


tk.Button(window, text="총 금액 보기", command=show_total).pack(pady=10)

tk.Button(window, text="관리자 화면", command=lambda: admin.open_admin_window(window, status_label)).pack(pady=10)

status_label = tk.Label(window, text="메뉴를 선택해주세요!", fg="blue")
status_label.pack(pady=20)

def order_popup():
    if not cal.cart:
        status_label.config(text="장바구니가 비었습니다.")
        return

    total = cal.get_total_price()

    popup = tk.Toplevel(window)
    popup.title("주문 완료")
    popup.geometry("280x240")

    summary_text = ""
    for menu, (qty, price) in cal.cart.items():
        summary_text += f" {menu} x{qty}\n"
        
        order.insert_order(menu, qty, qty * price)
    summary_text += f"\n총 금액: {total}원"

    tk.Label(popup, text="주문이 완료되었습니다!", font=("Arial", 12)).pack(pady=5)
    tk.Label(popup, text=summary_text, justify="center", fg="black").pack(pady=5)

    def close_all():
        cal.clear_cart()
        window.quit()

    def restart_order():
        cal.clear_cart()
        popup.destroy()
        status_label.config(text="메뉴를 선택해주세요!")

    tk.Button(popup, text="메뉴로 돌아가기", command=restart_order).pack(pady=5)
    tk.Button(popup, text="종료", command=close_all).pack(pady=5)

def clear_order():
    cal.clear_cart()
    status_label.config(text="장바구니 내역이 초기화되었습니다!")

tk.Button(window, text="주문하기", font=(20), command=order_popup).pack(pady=5)

tk.Button(window, text="장바구니 비우기", command=clear_order).pack(pady=5)

window.mainloop()
