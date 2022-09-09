import sys
from manager import man_obj
from manager import write_history


def main():
    if len(sys.argv) != 4:
        raise KeyError("4 arguments should be passed <file_name> <file_history> <change> <commentary>")
    action = "saldo"
    file = sys.argv[1]
    change = int(sys.argv[2])
    comment = sys.argv[3]
    man_obj.execute(action=action, change=change, comment=comment)
    write_history(man_obj.history, file=file)
    print("Balance successfully changed. Current balance:")
    print(man_obj.account)


if __name__ == '__main__':
    main()