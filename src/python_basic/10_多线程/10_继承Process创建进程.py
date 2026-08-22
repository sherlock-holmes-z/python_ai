from multiprocessing import Process


class SpeakProcess(Process):
    def __init__(self, a, **kwargs):
        super().__init__(**kwargs)
        self.a = a

    def run(self):
        print(f"self.a is {self.a},process_name is {super().name}")


if __name__ == "__main__":
    p1 = SpeakProcess(a=1, name="SpeakProcess")
    p1.start()
