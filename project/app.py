from flask import Flask, render_template, request, redirect
from konto import main as konto_main
from magazyn import main as magazyn_main
from saldo import main as saldo_main
from zakup import main as zakup_main
from sprzedaz import main as sprzedaz_main
from przeglad import main as przeglad_main
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///buildings.db"
db = SQLAlchemy(app)
# file with history
file = "history.txt"


# function that speeds up the functionality of returning to homepage with information :)
def return_render_template_home(msg):
    return render_template("home.html", account=konto_main(file), stock=magazyn_main(file), msg=msg)


# defining route for main site
@app.route("/")
def home():
    return return_render_template_home("No information")


# operations on the form in html, making transaction
@app.route("/action", methods=["GET", "POST"])
def check():
    # operations connected with balance
    if request.form.get("method") == "saldo":
        # getting arguments via post method
        action = request.form.get("method")
        comment = request.form.get("comment")
        change = request.form.get("change")
        # predicting wrong value passed in change key
        try:
            change = int(change)
        except ValueError:
            return return_render_template_home("Error: wrong value")
        # predict ValueError passed from manager function.
        try:
            saldo_main(action=action, change=change, comment=comment, file=file)
        except ValueError as error:
            return return_render_template_home(f"Error: {error}")
        return return_render_template_home(f"Balance successfully changed by: {change}")
    elif request.form.get("method") == "zakup":
        # getting arguments via post method
        action = request.form.get("method")
        product_id = request.form.get("product_id")
        buy_price = request.form.get("buy_price")
        buy_qty = request.form.get("buy_qty")
        # predicting wrong value passed in buy_price or buy_qty keys
        try:
            buy_price = int(buy_price)
            buy_qty = int(buy_qty)
        except ValueError:
            return return_render_template_home("Error: wrong value")
        # predict ValueError passed from manager function.
        try:
            zakup_main(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty, file=file)
        except ValueError as error:
            return return_render_template_home(f"Error: {error}")
        return return_render_template_home(f"{buy_qty}pcs of \"{product_id}\" bought successfully")
    elif request.form.get("method") == "sprzedaz":
        # getting arguments via post method
        action = request.form.get("method")
        product_id = request.form.get("product_id")
        sell_price = request.form.get("sell_price")
        sell_qty = request.form.get("sell_qty")
        # predicting wrong value passed in sell_price or sell_qty keys
        try:
            sell_price = int(sell_price)
            sell_qty = int(sell_qty)
        except ValueError:
            return return_render_template_home(msg="Error: wrong value")
        # predict ValueError passed from manager function.
        try:
            sprzedaz_main(action=action, product_id=product_id, sell_price=sell_price, sell_qty=sell_qty, file=file)
        except ValueError as error:
            return return_render_template_home(msg=f"Error: {error}")
        return return_render_template_home(f"{sell_qty}pcs of \"{product_id}\" sold successfully")
    # unexpected nothing happened return error.html
    return render_template("error.html", msg="check function error")


# function that returns history
def get_history(current_history, start=None, finish=None):
    history_list = []
    for action in current_history:
        for details in action:
            history_list.append(details)
    history_list.append("stop")
    # values type of start and finish are string to pass this step
    if start and finish:
        # values type changed to return selected by user slice of list
        return history_list[int(start):int(finish)]
    return history_list


# route witch returns specific slice of program history
@app.route("/history/<start>/<finish>")
def history_start_finish(start=None, finish=None):
    # predicting the passed be not number
    if int(start) < 0 or int(finish) < 0:
        return render_template("error.html", msg="negative argument passed")
    if start and finish:
        history_list_index = get_history(przeglad_main(file), start=start, finish=finish)
        return render_template("history.html", history=history_list_index)
    # unexpected nothing happened return error.html
    return render_template("error.html", msg="wrong arguments")


# route witch returns whole history
@app.route("/history/")
def history():
    return render_template("history.html", history=get_history(przeglad_main(file)))

