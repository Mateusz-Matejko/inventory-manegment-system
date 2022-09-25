import sys
from manager import man_obj


def main(action, product_id, buy_price, buy_qty):
    man_obj.get_current_company()
    man_obj.execute(action=action, product_id=product_id, buy_price=buy_price, buy_qty=buy_qty)
    man_obj.get_current_company()


if __name__ == '__main__':
    main()
