import sys
from manager import man_obj


def main():
    if len(sys.argv) != 2:
        raise KeyError("1 arguments should be passed <file>")
    man_obj.get_history(file_name=sys.argv[1])
    print(man_obj.account)


if __name__ == '__main__':
    main()