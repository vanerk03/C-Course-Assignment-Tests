from generate import DataFlag


def solve(path, flag: DataFlag, is_reversed: bool):
    fl = open(path, "r")
    if flag == DataFlag.INT:
        ot = [int(x.rstrip("\n")) for x in fl.readlines()]
    elif flag == DataFlag.FLOAT:
        ot = [float(x.rstrip("\n")) for x in fl.readlines()]
    elif flag == DataFlag.PHONEBOOK:
        ot = [x.rstrip("\n") for x in fl.readlines()]
        if ot[-1] == '\n':
            ot = ot[:-1]
        tmp = []
        for x in ot:
            a, b, c, num = x.split()
            num = int(num)
            tmp.append((a, b, c, num))
        ot = tmp
    else:
        raise ValueError("this flag doesn't exits") 

    return ot 