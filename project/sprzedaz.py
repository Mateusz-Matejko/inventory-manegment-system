import sys
from manager import man_obj


def main(action, product_id, sell_price, sell_qty):
    man_obj.get_history()
    man_obj.execute(action=action, product_id=product_id, sell_price=sell_price, sell_qty=sell_qty)


if __name__ == '__main__':
    main()