cart = []

def add_to_cart(menu, price):
    cart.append((menu, price))

def get_total_price():    
    return sum(price for _, price in cart)

def clear_cart():
    cart.clear()


