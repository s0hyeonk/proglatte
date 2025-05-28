
import tkinter as tk
import importlib
import cal
importlib.reload(cal)

import api

menu_items = {
    "아메리카노": 4500,
    "카페라떼": 5000,
    "카푸치노": 5200
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
window.geometry("320x400")

tk.Label(window, text="메뉴판", font=("Arial", 16)).pack(pady=10)

for name, price in menu_items.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = round(price * usd_rate, 2)
        text = f"{name} - {price}원 (약 ${usd_price})"
    else:
        text = f"{name} - {price}원"
    
    btn = tk.Button(window, text=text, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

tk.Button(window, text="총 금액 보기", command=show_total).pack(pady=10)

status_label = tk.Label(window, text="", fg="blue")
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
    summary_text += f"\n총 금액: {total}원"

    tk.Label(popup, text="주문이 완료되었습니다!", font=("Arial", 12)).pack(pady=5)
    tk.Label(popup, text=summary_text, justify="left", fg="black").pack(pady=5)

    def close_all():
        cal.clear_cart()
        window.quit()

    def restart_order():
        cal.clear_cart()
        popup.destroy()
        status_label.config(text="주문을 시작하세요")

    tk.Button(popup, text="재주문", command=restart_order).pack(pady=5)
    tk.Button(popup, text="종료", command=close_all).pack(pady=5)

def clear_order():
    cal.clear_cart()
    status_label.config(text="🗑 장바구니 내역이 초기화되었습니다.")

tk.Button(window, text="주문하기", command=order_popup).pack(pady=5)

tk.Button(window, text="🗑 장바구니 비우기", command=clear_order).pack(pady=5)

if usd_rate:
    tk.Label(window, text=f"※ 환율: 1원 ≈ ${usd_rate:.5f}", fg="gray").pack()
else:
    tk.Label(window, text="※ 환율 정보를 불러올 수 없습니다.", fg="red").pack()

window.mainloop()
