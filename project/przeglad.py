import sys
from manager import man_obj


def main(file):
    # if len(sys.argv) != 2:
    #     raise KeyError("2 arguments should be passed <file_name> <file_history>")
    man_obj.get_history(file)
    man_obj.write_history(file)
    print(man_obj.history)
    return man_obj.history



if __name__ == '__main__':
    main()