def calculate_bill(*prices, **tax):
    total = sum(prices)
    perct = tax.get("tax")

    tax_amount = (total * perct) / 100
    final = total + tax_amount

    return total, perct, final


print(calculate_bill(100, 250, 300, tax=18))
