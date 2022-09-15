from flask import Flask, render_template, request
from konto import main as ballance_konto
from magazyn import main as stock_magazyn
app = Flask(__name__)


@app.route("/")
def home():
    stock = stock_magazyn("history.txt")
    balance = ballance_konto("history.txt")
    return render_template("home.html", balance=balance, stock=stock)


@app.route("/action")
def action():
    # validate action
    action = request.args.get("action")
    if action == "sprzedaz":
        return render_template("sprzedaz.html")
    elif action == "zakup":
        return render_template("zakup.html")
    elif action == "saldo":
        return render_template("saldo.html")
    else:
        render_template("Error.html")

@app.route("/check")
def ballance_status():
    if str(request.form.get("change")).isalpha() or str(request.form.get("comment")).isnumeric():
        return None
    action = "saldo"
    change = request.form.get("change")
    comment = request.form.get("comment")
    return render_template("success.html")


def buy_status():
    if str(request.form.get("buy_price")).isalpha() or str(request.form.get("buy_qty")).isalpha()\
            or str(request.form.get("id")).isnumeric():
        return None
    action = "zakup"
    id = request.form.get("id")
    price = request.form.get("buy_price")
    amount = request.form.get("buy_qty")
    return render_template("success.html")


def sell_status():
    if str(request.form.get("sell_price")).isalpha() or str(request.form.get("sell_qty")).isalpha()\
            or str(request.form.get("id")).isnumeric():
        return None
    action = "sprzedaz"
    id = request.form.get("id")
    price = request.form.get("sell_price")
    amount = request.form.get("sell_qty")
    return render_template("success.html")


@app.route("/status/", methods=["POST", "GET"])
def status():
    r = ballance_status()
    print(r)
    if not r:
        r = buy_status()
        if not r:
            r = sell_status()
            if not r:
                return render_template("error.html")
    return render_template("success.html")




