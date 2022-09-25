import sys
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accountant.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

alembic = Alembic()
alembic.init_app(app)


# class handling database
class HistoryOfOperations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return self.action

    def __str__(self):
        return self.action


def main():
    ...


# defining manager class
class Manager:
    def __init__(self):
        self.history_class = HistoryOfOperations
        self.account = 0
        self.history = []
        self.stock = {}
        self.actions = {}

    # method witch gets history of operations from database
    def get_history(self):
        result = db.session.query(HistoryOfOperations).all()
        self.history = result

    # methods that change history into current company stock and values
    def get_current_company(self):
        self.account = 0
        self.stock = {}
        for row in self.history:
            row = str(row)
            action = row.split(",")[0]
            if action == "saldo":
                action, change, comment = row.split(",")
                self.change_company_state(change=int(change), balance_o=True)
            elif action == "zakup":
                action, product_id, buy_price, buy_qty = row.split(",")
                self.change_company_state(product_id=product_id, price=int(buy_price), qty=int(buy_qty), buy_o=True)
            elif action == "sprzedaz":
                action, product_id, sell_price, sell_qty = row.split(",")
                self.change_company_state(product_id=product_id, price=int(sell_price), qty=int(sell_qty), sell_o=True)
            else:
                raise StopIteration("Failed get_current_company in Manager class.")

    # method used within getting current company
    def change_company_state(self, change=None, product_id=None, price=None, qty=None,
                             balance_o=False, sell_o=False, buy_o=False):
        if balance_o:
            self.account += change
        elif buy_o:
            if product_id not in self.stock:
                self.stock[product_id] = qty
            else:
                self.stock[product_id] += qty
            self.account -= (int(price) * int(qty))
        elif sell_o:
            self.stock[product_id] -= qty
            self.account += (int(price) * int(qty))

    # method used to add new transactions to database
    def add_to_database(self, data):
        history_object = self.history_class(action=data)
        db.session.add(history_object)
        db.session.commit()

    # creator of dictionary with possible actions
    def assign(self, action):
        def wrapper(func):
            self.actions[action] = func
        return wrapper

    # executor of actions dictionary
    def execute(self, action, **kwargs):
        self.actions[action](self, **kwargs)


man_obj = Manager()


# handler of new "saldo" operations
@man_obj.assign("saldo")
def saldo(manager, change, comment):
    if manager.account + change < 0:
        raise ValueError(f"Balance after transaction can't fall under 0.")
    manager.account += change
    man_obj.add_to_database(f"saldo,{str(change)},{str(comment)}")


# handler for new "zakup" operations
@man_obj.assign("zakup")
def buy(manager, product_id, buy_price, buy_qty):
    transaction_amount = buy_price * buy_qty
    if manager.account < transaction_amount:
        raise ValueError(f"Not enough money to buy {buy_qty} of \"{product_id}\", "
                         f"needed: {transaction_amount}, got: {manager.account}.")
    if product_id not in manager.stock:
        manager.stock[product_id] = buy_qty
    else:
        manager.stock[product_id] += buy_qty
    manager.account -= transaction_amount
    man_obj.add_to_database(f"zakup,{str(product_id)},{str(buy_price)},{str(buy_qty)}")


# handler fro new "sprzedaz" operations
@man_obj.assign("sprzedaz")
def sell(manager, product_id, sell_price, sell_qty, ):
    if product_id not in manager.stock:
        raise ValueError(f"You dont have \"{product_id}\" in stock, perhaps you ment other product.")
    if manager.stock[product_id] < sell_qty:
        raise ValueError(f"Not enough \"{product_id}\" in stock. Needed:{sell_qty}, got:{man_obj.stock[product_id]}.")
    manager.stock[product_id] -= sell_qty
    manager.account += sell_price * sell_qty
    man_obj.add_to_database(f"sprzedaz,{str(product_id)},{str(sell_price)},{str(sell_qty)}")


if __name__ == '__main__':
    main()

"""
saldo / kwota/ komentarz - (zmiana $ koncie, dodatnia lub ujemna)
zakup / produkt/ cena za szt / ilość szt (odejmuje $ z konta, dodaje do magazynu szt)
sprzedaz / produkt/ cena za szt / ilość szt (dodaje $ do konta, odejmuje z magazynu szt)
"""