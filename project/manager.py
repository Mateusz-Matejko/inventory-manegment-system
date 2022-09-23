import sys
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accountant.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class HistoryOfOperations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return self.action

    def __str__(self):
        return self.action


# db.create_all()

history_list = []
with open("history.txt", "r") as f:
    result = f.readlines()
    for line in result:
        line = str(line.strip())
        history_list.append(line)


print(history_list)

# for line in history_list:
#     print(line)
#     something = HistoryOfOperations(action=line)
#     db.session.add(something)
# db.session.commit()


def main():
    print(man_obj.history)
    man_obj.get_current_company()


# defining manager class


class Manager:
    def __init__(self):
        self.account = 0
        self.history = []
        self.stock = {}
        self.actions = {}

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, other):
        other = db.session.query(HistoryOfOperations).all()
        self._history = other

    def get_current_company(self):
        self.account = 0
        self.stock = {}
        for row in self.history:
            row = str(row)
            action = row.split(",")[0]
            if action == "saldo":
                action, change, comment = row.split(",")
                self.account += int(change)
            elif action == "zakup":
                action, product_id, buy_price, buy_qty = row.split(",")
                sell_buy_operation(product_id, buy_price, buy_qty, buy=True)

            elif action == "sprzedaz":
                action, product_id, sell_price, sell_qty = row.split(",")
            else:
                raise StopIteration("Failed get_current_company in Manager class.")

            # else:
            #     raise StopIteration("Failed iteration")
            #     self.account += change
            #     self.history.append([line, change, comment])
            # elif action == "zakup":
            #     product_id, buy_price, buy_qty, full_amount = sell_buy_operation(file)
            #     if product_id not in self.stock:
            #         self.stock[product_id] = buy_qty
            #     else:
            #         self.stock[product_id] += buy_qty
            #     self.account -= full_amount
            #     self.history.append([line, product_id, str(buy_price), str(buy_qty)])
            # elif action == "sprzedaz":
            #     product_id, sell_price, sell_qty, full_amount = sell_buy_operation(file)
            #     self.stock[product_id] -= sell_qty
            #     self.account += full_amount
            #     self.history.append([line, product_id, str(buy_price), str(buy_qty)])
            # elif line == "stop":
            #     break

    # def write_history(self, file):
    #     with open(file, "w") as file:
    #         for transaction in self.history:
    #             for details in transaction:
    #                 details = str(details)
    #                 try:
    #                     details = details.strip()
    #                 except AttributeError:
    #                     pass
    #                 file.write(str(details))
    #                 file.write("\n")
    #         file.write("stop")
    #
    # def assign(self, action):
    #     def wrapper(func):
    #         self.actions[action] = func
    #     return wrapper
    #
    # def execute(self, action, **kwargs):
    #     self.actions[action](self, **kwargs)


man_obj = Manager()


# @man_obj.assign("saldo")
# def saldo(manager, change, comment):
#     if manager.account + change < 0:
#         raise ValueError(f"Balance after transaction can't fall under 0.")
#     manager.account += change
#     man_obj.history.append(["saldo", str(change), comment])
#
#
# @man_obj.assign("zakup")
# def buy(manager, product_id, buy_price, buy_qty):
#     transaction_amount = buy_price * buy_qty
#     if manager.account < transaction_amount:
#         raise ValueError(f"Not enough money to buy {buy_qty} of \"{product_id}\", "
#                          f"needed: {transaction_amount}, got: {manager.account}.")
#     if product_id not in manager.stock:
#         manager.stock[product_id] = buy_qty
#     else:
#         manager.stock[product_id] += buy_qty
#     manager.account -= transaction_amount
#     man_obj.history.append(["zakup", product_id, str(buy_price), str(buy_qty)])
#
#
# @man_obj.assign("sprzedaz")
# def sell(manager, product_id, sell_price, sell_qty):
#     transaction_amount = sell_price * sell_qty
#     if product_id not in manager.stock:
#         raise ValueError(f"You dont have \"{product_id}\" in stock, perhaps you ment other product.")
#     if manager.stock[product_id] < sell_qty:
#         raise ValueError(f"Not enough \"{product_id}\" in stock. Needed:{sell_qty}, got:{man_obj.stock[product_id]}.")
#     manager.stock[product_id] -= sell_qty
#     manager.account += transaction_amount
#     man_obj.history.append(["sprzedaz", product_id, str(sell_price), str(sell_qty)])
#
#
def sell_buy_operation(id, price, qty, sell=False, buy=False):
    price = int(price)
    qty = int(qty)
    transaction_amount = price*qty
    if buy:
        if id not in man_obj.stock:
            man_obj.stock[id] = qty
        else:
            man_obj.stock[id] += qty
        man_obj.account -= transaction_amount
    elif sell:
        man_obj[id] -= qty
        man_obj.account += transaction_amount




if __name__ == '__main__':
    main()

"""
saldo / kwota/ komentarz - (zmiana $ koncie, dodatnia lub ujemna)
zakup / produkt/ cena za szt / ilość szt (odejmuje $ z konta, dodaje do magazynu szt)
sprzedaz / produkt/ cena za szt / ilość szt (dodaje $ do konta, odejmuje z magazynu szt)
"""