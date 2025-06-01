import tkinter as tk
import order

def open_admin_window(master_window, status_label=None):
    admin = tk.Toplevel(master_window)
    admin.title("관리자 화면 - 주문 내역")
    admin.geometry("400x400")

    orders = order.get_all_orders()

    if not orders:
        tk.Label(admin, text="주문 내역이 없습니다.").pack(pady=10)
    else:
        for row in orders:
            id, name, qty, price, time = row
            text = f"{id}. {name} x{qty} - {price}원 ({time})"
            tk.Label(admin, text=text, anchor="w", justify="left").pack(anchor="w")

    def reset_orders():
        order.clear_orders()
        admin.destroy()
        if status_label:
            status_label.config(text="주문 초기화 완료")

    tk.Button(admin, text="주문 내역 전체 초기화", command=reset_orders, fg="red").pack(pady=10)
