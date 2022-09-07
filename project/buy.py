import sys
from manager import man_obj
from manager import write_history


def main():
    action = "zakup"
    file = sys.argv[1]
    product_id = sys.argv[2]
    buy_price = int(sys.argv[3])
    buy_qty = int(sys.argv[4])
    man_obj.execute(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty)
    print(man_obj.stock)
    write_history(history=man_obj.history, file=file)


if __name__ == '__main__':
    main()
