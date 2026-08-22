from multiprocessing import Pipe, Process


def producer(send_conn):
    send_conn.send({"name": "张三", "score": 95})
    send_conn.close()  # 关闭后续不能再send


def consumer(recv_conn):
    data = recv_conn.recv()
    print(data)
    recv_conn.close()  # 关闭后续不能再recv


def test1(con1):
    data = con1.recv()
    print(f"test1:{data}")
    con1.send(1)


def test2(con2):
    con2.send(2)
    data = con2.recv()
    print(f"test2:{data}")


if __name__ == "__main__":
    # 单向管道，第一个只能读，第二个只能发
    recv_conn, send_conn = Pipe(duplex=False)

    p1 = Process(target=producer, args=(send_conn,))
    p2 = Process(target=consumer, args=(recv_conn,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # 双向管道，既能读也能发，但一个发送的消息，只能另一个读
    con1, con2 = Pipe()
    t1 = Process(target=test1, args=(con1,))
    t2 = Process(target=test2, args=(con2,))
    t1.start()
    t2.start()
