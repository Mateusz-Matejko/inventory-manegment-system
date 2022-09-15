import sys
from manager import man_obj


def main(file_name):
    man_obj.get_history(file_name)
    return man_obj.account


if __name__ == '__main__':
    main()