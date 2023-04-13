import sys
from manager import man_obj


def main(action, change, comment):
    man_obj.get_history()
    man_obj.execute(action=action, change=change, comment=comment)
    # return "Balance successfully changed. Current balance:"


if __name__ == '__main__':
    main()