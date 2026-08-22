from multiprocessing import Process

num = 100
names = []
arg = []


def test1(args):
    global num, names
    num += 1
    names.append(num)
    args.append(num)
    print(f"test1:{num}, names:{names},arg:{args}")


def test2(args):
    global num, names
    num -= 1
    names.append(num)
    args.append(num)
    print(f"test2:{num}, names:{names},arg:{args}")


if __name__ == "__main__":
    p1 = Process(target=test1, args=(arg,))
    p2 = Process(target=test2, args=(arg,))
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # 进程之间的变量操作互不影响（有些变量可以跨进程，比如lock锁）
    print(f"end:{num}, names:{names},args:{arg}")
