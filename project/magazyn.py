import sys
from manager import man_obj


def main():
    products = sys.argv[2:]
    if len(sys.argv) < 3:
        raise KeyError("at least 3 arguments should be passed <file_name> <file_history> <product_id> ")
    for product in products:
        try:
            print(f"{product}: {man_obj.stock[product]}")
        except KeyError:
            print(f"{product}: not in stock")


if __name__ == '__main__':
    main()