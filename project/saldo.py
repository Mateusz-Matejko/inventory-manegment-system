import sys
from manager import man_obj


def main():
    if len(sys.argv) != 4:
        raise KeyError("4 arguments should be passed <file_name> <file_history> <change> <commentary>")
    action = "saldo"
    file = sys.argv[1]
    change = int(sys.argv[2])
    comment = sys.argv[3]
    man_obj.get_history(file)
    man_obj.execute(action=action, change=change, comment=comment)
    man_obj.write_history(file=file)
    print("Balance successfully changed. Current balance:")
    print(man_obj.account)


if __name__ == '__main__':
    main()