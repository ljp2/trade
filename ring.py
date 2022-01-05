import numpy as np

class Ring:
    def __init__(self, n: int):
        self.N = n
        self.buf = np.zeros(n, dtype="int8")
        self.index: int = 0
        self.last_val: int = None

    def push(self, pred: int):
        val = 1 if pred == 1 else -1
        self.last_val = val
        self.buf[self.index] = val
        self.index = (self.index + 1) % 2

    def last_pred(self):
        return self.last_val

    def sum(self):
        return self.buf.sum()

    def __repr__(self) -> str:
        return "{}:{}".format(self.last_val, self.buf)


ring = Ring(2)
