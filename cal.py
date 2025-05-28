cart = {}

def add_to_cart(menu, price):
    if menu in cart:
        cart[menu][0] += 1  
    else:
        cart[menu] = [1, price]

def get_total_price():    
    return sum(qty * price for qty, price in cart.values())

def clear_cart():
    cart.clear()


