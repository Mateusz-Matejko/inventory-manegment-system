import sys
from manager import man_obj


def main():
    if len(sys.argv) != 5:
        raise KeyError("5 arguments should be passed <file_name> <file_history> <product_id> <price> <qty>")
    action = "zakup"
    file = sys.argv[1]
    product_id = sys.argv[2]
    buy_price = int(sys.argv[3])
    buy_qty = int(sys.argv[4])
    man_obj.get_history(file)
    man_obj.execute(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty)
    man_obj.write_history(file=file)
    print(f"{buy_qty}pcs of \"{product_id}\" successfully bought. Current stock:")
    print(man_obj.stock)


if __name__ == '__main__':
    main()
