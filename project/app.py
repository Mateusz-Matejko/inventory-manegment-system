from flask import Flask, render_template, request, redirect
from konto import main as konto_main
from magazyn import main as magazyn_main
from saldo import main as saldo_main
from zakup import main as zakup_main
from sprzedaz import main as sprzedaz_main

app = Flask(__name__)

stock = magazyn_main("history.txt")
account = konto_main("history.txt")
file = "history.txt"


@app.route("/")
def home():
    return render_template("home.html", account=account, stock=stock)


@app.route("/action", methods=["GET", "POST"])
def check():
    if request.form.get("method") == "saldo":
        action = request.form.get("method")
        change = request.form.get("change")
        change = int(change)
        comment = request.form.get("comment")
        result = saldo_main(action=action, change=change, comment=comment, file=file)
        if result:
            return render_template("error.html", msg=result)
        saldo_main(action=action, change=change, comment=comment, file=file)
        return redirect("/")
    elif request.form.get("method") == "zakup":
        action = request.form.get("method")
        product_id = request.form.get("product_id")
        buy_price = request.form.get("buy_price")
        buy_qty = request.form.get("buy_qty")
        buy_price, buy_qty = int(buy_price), int(buy_qty)
        result = zakup_main(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty, file=file)
        if result:
            return render_template("error.html", msg=result)
        zakup_main(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty, file=file)
        return redirect("/")
    elif request.form.get("method") == "sprzedaz":
        action = request.form.get("method")
        product_id = request.form.get("product_id")
        sell_price = request.form.get("buy_price")
        sell_qty = request.form.get("buy_qty")
        sell_price, sell_qty = int(sell_price), int(sell_qty)
        result = sprzedaz_main(action=action, product_id=product_id, sell_price=sell_price, sell_qty=sell_qty, file=file)
        if result:
            return render_template("error.html", msg=result)
        sprzedaz_main(action=action, product_id=product_id, sell_price=sell_price, sell_qty=sell_qty, file=file)
        return redirect("/")
    return render_template("error.html", msg="check function error")


# @app.route("/status/", methods=["POST", "GET"])
# def status():
#     r = ba()
#     if not r:
#         r = buy_status()
#         if not r:
#             r = sell_status()
#             if not r:
#                 return render_template("error.html")
#     return render_template("success.html")




