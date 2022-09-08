import sys
from manager import man_obj
from manager import write_history


def main():
    action = "sprzedaz"
    file = sys.argv[1]
    product_id = sys.argv[2]
    sell_price = int(sys.argv[3])
    sell_qty = int(sys.argv[4])
    man_obj.execute(action=action, product_id=product_id, sell_price=sell_price, sell_qty=sell_qty)
    print(man_obj.stock)
    write_history(history=man_obj.history, file=file)


if __name__ == '__main__':
    main()