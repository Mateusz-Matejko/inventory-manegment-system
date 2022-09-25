from flask import Flask, render_template, request, redirect
from konto import main as konto_main
from magazyn import main as magazyn_main
from saldo import main as saldo_main
from zakup import main as zakup_main
from sprzedaz import main as sprzedaz_main
from przeglad import main as przeglad_main
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from manager import man_obj

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accountant.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
alembic = Alembic()
alembic.init_app(app)

class HistoryOfOperations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return self.action

    def __str__(self):
        return self.action


# function that speeds up the functionality of returning to homepage with information :)
def return_render_template_home(msg):
    return render_template("home.html", account=konto_main(), stock=magazyn_main(), msg=msg)


# checking if coma is in any of values passed
def check_for_coma(arguments_list):
    for argument in arguments_list:
        if "," in argument:
            raise ValueError


# defining route for main site
@app.route("/")
def home():
    return return_render_template_home(msg="No information")


# operations on the form in html, making transaction
@app.route("/action", methods=["GET", "POST"])
def check():
    # operations connected with balance
    if request.form.get("method") == "saldo":
        # getting arguments via post method
        action = request.form.get("method")
        comment = request.form.get("comment")
        change = request.form.get("change")
        # checking for coma and predicting wrong value passed in change key
        try:
            check_for_coma([action, comment, change])
            change = int(change)
        except ValueError:
            return return_render_template_home(msg="Error: wrong value passed or \",\"(coma) used.")
        # predict ValueError passed from manager function.
        try:
            saldo_main(action=action, change=change, comment=comment)
        except ValueError as error:
            return return_render_template_home(msg=f"Error: {error}")
        return return_render_template_home(msg=f"Balance successfully changed by: {change}")
    elif request.form.get("method") == "zakup":
        # getting arguments via post method
        action = request.form.get("method")
        product_id = request.form.get("product_id")
        buy_price = request.form.get("buy_price")
        buy_qty = request.form.get("buy_qty")
        # checking for coma and predicting wrong value passed in buy_price or buy_qty keys
        try:
            check_for_coma([action, product_id, buy_price, buy_qty])
            buy_price = int(buy_price)
            buy_qty = int(buy_qty)
        except ValueError:
            return return_render_template_home(msg="Error: wrong value passed or \",\"(coma) used.")
        # predict ValueError passed from manager function.
        try:
            zakup_main(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty)
        except ValueError as error:
            return return_render_template_home(msg=f"Error: {error}")
        return return_render_template_home(msg=f"{buy_qty}pcs of \"{product_id}\" bought successfully")
    elif request.form.get("method") == "sprzedaz":
        # getting arguments via post method
        action = request.form.get("method")
        product_id = request.form.get("product_id")
        sell_price = request.form.get("sell_price")
        sell_qty = request.form.get("sell_qty")
        # checking for coma and predicting wrong value passed in sell_price or sell_qty keys
        try:
            check_for_coma([action, product_id, sell_price, sell_qty])
            sell_price = int(sell_price)
            sell_qty = int(sell_qty)
        except ValueError:
            return return_render_template_home(msg="Error: wrong value passed or \",\"(coma) used.")
        # predict ValueError passed from manager function.
        try:
            sprzedaz_main(action=action, product_id=product_id, sell_price=sell_price, sell_qty=sell_qty)
        except ValueError as error:
            return return_render_template_home(msg=f"Error: {error}")
        return return_render_template_home(msg=f"{sell_qty}pcs of \"{product_id}\" sold successfully")
    # unexpected nothing happened return error.html
    return render_template("error.html", msg="check function error")


# function that returns history
def get_history(current_history, start=None, finish=None):
    # values type of start and finish are string to pass this step
    if start and finish:
        # values type changed to return selected by user slice of list
        return current_history[int(start):int(finish)]
    return current_history


# route witch returns specific slice of program history
@app.route("/history/<start>/<finish>")
def history_start_finish(start=None, finish=None):
    # predicting the passed be not number
    if int(start) < 0 or int(finish) < 0:
        return render_template("error.html", msg="negative argument passed")
    if start and finish:
        history_list_index = get_history(przeglad_main(), start=start, finish=finish)
        return render_template("history.html", history=history_list_index)
    # unexpected nothing happened return error.html
    return render_template("error.html", msg="wrong arguments")


# route witch returns whole history
@app.route("/history/")
def history():
    return render_template("history.html", history=get_history(przeglad_main()))

