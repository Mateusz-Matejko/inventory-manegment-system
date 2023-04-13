import sys
from manager import man_obj


def main():
    man_obj.get_history()
    man_obj.get_current_company()
    return man_obj.stock


if __name__ == '__main__':
    main()