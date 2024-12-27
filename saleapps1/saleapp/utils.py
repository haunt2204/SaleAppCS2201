def count_cart(cart):
    total_quantity, total_amount = 0, 0

    for c in cart.values():
        total_quantity += c['quantity']
        total_amount += c['quantity']*c['price']

    print(cart)

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }