import sys


def main():
    man_obj.get_history("history.txt")

# defining manager class


class Manager:
    def __init__(self):
        self.account = 0
        self.history = []
        self.stock = {}
        self.actions = {}
        self.file_name = None

    def get_history(self, file_name):
        self.history = []
        self.account = 0
        self.stock = {}
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line == "saldo":
                    change = int(file.readline().strip())
                    comment = file.readline().strip()
                    self.account += change
                    self.history.append([line, change, comment])
                elif line == "zakup":
                    product_id, buy_price, buy_qty, full_amount = sell_buy_operation(file)
                    if product_id not in self.stock:
                        self.stock[product_id] = buy_qty
                    else:
                        self.stock[product_id] += buy_qty
                    self.account -= full_amount
                    self.history.append([line, product_id, str(buy_price), str(buy_qty)])
                elif line == "sprzedaz":
                    product_id, sell_price, sell_qty, full_amount = sell_buy_operation(file)
                    self.stock[product_id] -= sell_qty
                    self.account += full_amount
                    self.history.append([line, product_id, str(buy_price), str(buy_qty)])
                elif line == "stop":
                    break

    def write_history(self, file):
        with open(file, "w") as file:
            for transaction in self.history:
                for details in transaction:
                    details = str(details)
                    try:
                        details = details.strip()
                    except AttributeError:
                        pass
                    file.write(str(details))
                    file.write("\n")
            file.write("stop")

    def assign(self, action):
        def wrapper(func):
            self.actions[action] = func
        return wrapper

    def execute(self, action, **kwargs):
        self.actions[action](self,**kwargs)


man_obj = Manager()


@man_obj.assign("saldo")
def saldo(manager, change, comment):
    manager.account += change
    man_obj.history.append(["saldo", str(change), comment])


@man_obj.assign("zakup")
def buy(manager, product_id, buy_price, buy_qty):
    transaction_amount = buy_price * buy_qty
    if manager.account < transaction_amount:
        raise ValueError(f"Not enough money to buy {buy_qty} of {product_id}")
    if product_id not in manager.stock:
        manager.stock[product_id] = buy_qty
    else:
        manager.stock[product_id] += buy_qty
    manager.account -= transaction_amount
    man_obj.history.append(["zakup", product_id, str(buy_price), str(buy_qty)])


@man_obj.assign("sprzedaz")
def sell(manager, product_id, sell_price, sell_qty):
    transaction_amount = sell_price * sell_qty
    if product_id not in manager.stock:
        raise KeyError(f"You dont have \"{product_id}\" in stock, perhaps you ment other product.")
    if manager.stock[product_id] < sell_qty:
        raise ValueError(f"Not enough {product_id} in stock. Needed:{sell_qty}, got:{man_obj.stock[product_id]}.")
    manager.stock[product_id] -= sell_qty
    manager.account += transaction_amount
    man_obj.history.append(["sprzedaz", product_id, str(sell_price), str(sell_qty)])


def sell_buy_operation(file):
    product_id = file.readline().rstrip()
    price = int(file.readline().rstrip())
    qty = int(file.readline().rstrip())
    transaction_amount = price*qty
    return product_id, price, qty, transaction_amount


if __name__ == '__main__':
    main()

"""
saldo / kwota/ komentarz - (zmiana $ koncie, dodatnia lub ujemna)
zakup / produkt/ cena za szt / ilość szt (odejmuje $ z konta, dodaje do magazynu szt)
sprzedaz / produkt/ cena za szt / ilość szt (dodaje $ do konta, odejmuje z magazynu szt)
"""