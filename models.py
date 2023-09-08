from dataclasses import dataclass

@dataclass
class spread:
    prev_ask: float
    prev_bid: float
    prev_avg: float
    prev_time: str
    ask: float
    bid: float
    avg: float
    time: str
    change: float

    def print_info(self):
        print(self.prev_time, "a:", round(self.prev_ask, 5), "b:", round(self.prev_bid, 5), "m:", round(self.prev_avg, 5), "==> {:.5f} ==>".format(self.change), self.time, "a:", round(self.ask, 5), "b:", round(self.bid, 5), "m:", round(self.avg, 5))

    def set_prev(self):
        self.prev_ask = self.ask
        self.prev_bid = self.bid
        self.prev_avg = self.avg
        self.prev_time = self.time