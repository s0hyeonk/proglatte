
import tkinter as tk
import tkinter.messagebox
import cal
import order
import api
import admin
order.connect_db()

caffee = {
    "아메리카노": 4500,
    "에스프레소": 4000,
    "카페라떼": 5000,
    "카푸치노": 5200,
}

ade = {
    "레몬에이드": 5000,
    "자몽에이드": 5000,
    "청포도에이드": 5000,
    "유자에이드": 5000,
}

juce = {
    "딸기주스": 6000,
    "사과주스": 6000,
    "오렌지주스": 6000,
    "포도주스": 6000
}

tea = {
    "얼그레이": 5000,
    "페퍼민트": 5000,
    "루이보스": 5000,
    "캐모마일": 5000
}

usd_rate = api.get_exchange_rate('USD')
if not usd_rate:
    print("환율 정보를 가져올 수 없었습니다.")

def add_item(name, price):
    cal.add_to_cart(name, price)
    qty = cal.cart[name][0] 
    
window = tk.Tk()
window.title("카페 키오스크")
window.geometry("1920x1080")

tk.Label(window, text="M e n u", font=("Arial", 80)).pack(pady=20)

top = tk.Frame(window)
top.pack(pady=10)

left = tk.Frame(top)
left.grid(row=0, column=0, padx=(0, 30))

tk.Label(left, text="caffee", font=("Arial", 40)).pack(anchor="w")

tk.Frame(left, height=1, bg="black").pack(fill="x")

for name, price in caffee.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = int(price * usd_rate)
        text = f"{name}                                         {price}원 (${usd_price})"
    else:
        text = f"{name}                                                        {price}원"
    
    btn = tk.Button(left, text=text, font=20, anchor="w", command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

right = tk.Frame(top)
right.grid(row=0, column=1, padx=(70, 0))

tk.Label(right, text="ade", font=("Arial", 40)).pack(anchor="w")
tk.Frame(right, width=340, height=1, bg="black").pack(fill="x", pady=5)

for name, price in ade.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = int(price * usd_rate)
        text = f"{name}                                         {price}원 (${usd_price})"
    else:
        text = f"{name}                                                        {price}원"
    
    btn = tk.Button(right, text=text, font=20, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

bottom = tk.Frame(window)
bottom.pack(pady=10)

left2 = tk.Frame(bottom)
left2.grid(row=0, column=0, padx=(0, 50))

tk.Label(left2, text="juice", font=("Arial", 40)).pack(anchor="w")
tk.Frame(left2, height=1, bg="black").pack(fill="x")

for name, price in juce.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = int(price * usd_rate)
        text = f"{name}                                          {price}원 (${usd_price})"
    else:
        text = f"{name}                                                         {price}원"
    
    btn = tk.Button(left2, text=text, font=20, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

def show_cart():
    if not cal.cart:
        tk.messagebox.showinfo("장바구니", "장바구니가 비어 있습니다!")
        return

    cart_text = "장바구니 내역:\n"
    for menu, (qty, price) in cal.cart.items():
        cart_text += f"{menu} x{qty} - {qty * price}원\n"
    
    total = cal.get_total_price()
    cart_text += f"\n총 금액: {total}원"

    def clear_order():
       cal.clear_cart()
       showcart.destroy()

    showcart = tk.Toplevel(left2)
    showcart.title("장바구니 내역") 
    showcart.geometry("350x350")
    tk.Label(showcart, text=cart_text, font="50", justify="left", fg="black").pack(pady=10)
    tk.Button(showcart, text="장바구니 비우기", font="40", command=clear_order).pack(pady=10)
    tk.Button(showcart, text="닫기", font="40", command=showcart.destroy).pack(pady=10)
    
tk.Button(left2, text="장바구니", font=(100), command=show_cart).pack(pady=50, padx=(500, 0))

right2 = tk.Frame(bottom)
right2.grid(row=0, column=1, padx=(50, 0))

tk.Label(right2, text="tea", anchor="w", font=("Arial", 40)).pack(anchor="w")
tk.Frame(right2, height=1, bg="black").pack(fill="x")

for name, price in tea.items():
    if not usd_rate:
        usd_rate = api.get_exchange_rate('USD')  

    if usd_rate:
        usd_price = int(price * usd_rate)
        text = f"{name}                                            {price}원 (${usd_price})"
    else:
        text = f"{name}                                                          {price}원"
    
    btn = tk.Button(right2, text=text, font=40, command=lambda n=name, p=price: add_item(n, p))
    btn.pack(pady=5)

def order_popup():
    if not cal.cart:
        tk.messagebox.showwarning("알림", "장바구니가 비었습니다!")
        return

    total = cal.get_total_price()
    summary_text = ""
    for menu, (qty, price) in cal.cart.items():
        summary_text += f" {menu} x{qty}\n"
        
        order.insert_order(menu, qty, qty * price)

    summary_text += f"\n총 금액: {total}원"


    popup = tk.Toplevel(window)
    popup.title("주문 완료")
    popup.geometry("350x350") 
    tk.Label(popup, text="주문이 완료되었습니다!", font=("Arial", 15)).pack(pady=5)
    tk.Label(popup, text=summary_text, justify="left", font=("Arial", 15), fg="black").pack(pady=5)

    def close_all():
        cal.clear_cart()
        window.quit()

    def restart_order():
        cal.clear_cart()
        popup.destroy()
    
    tk.Button(popup, text="재주문", font="40", command=restart_order).pack(pady=5)
    tk.Button(popup, text="종료", font="40", command=close_all).pack(pady=5)

def clear_order():
    cal.clear_cart()

tk.Button(right2, text="주문하기", font=(100), command=order_popup).pack(pady=50, padx=(0, 500))
tk.Button(window, text="관리자 화면", command=lambda: admin.open_admin_window(window)).pack(pady=50)

window.mainloop()
