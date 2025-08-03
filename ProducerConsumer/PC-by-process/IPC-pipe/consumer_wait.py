import multiprocessing
import time
import random

BUFFER_CAPACITY = 10


class Producer(multiprocessing.Process):
    def __init__(self, pipe, buffer_items, producer_id):
        super().__init__()
        self.pipe = pipe
        self.buffer_items = buffer_items
        self.producer_id = producer_id

    def run(self):
        _, sender = self.pipe
        while True:
            with self.buffer_items.get_lock():  # lock to ensure atomic updates
                if self.buffer_items.value < BUFFER_CAPACITY:
                    item = random.randint(1, 100)
                    print(f"Producer {self.producer_id} produced: {item}. Buffer items count: {self.buffer_items.value}")
                    sender.send(item)
                    self.buffer_items.value += 1
                    time.sleep(1)  
                else:
                    print(f"Buffer is full, producer {self.producer_id} is waiting. Buffer items count: {self.buffer_items.value}")
            time.sleep(4) 


class Consumer(multiprocessing.Process):
    def __init__(self, pipe, buffer_items, consumer_id):
        super().__init__()
        self.pipe = pipe
        self.buffer_items = buffer_items
        self.consumer_id = consumer_id

    def run(self):
        receiver, _ = self.pipe
        while True:
            with self.buffer_items.get_lock():  # lock to ensure atomic updates
                if self.buffer_items.value > 0:
                    item = receiver.recv()
                    self.buffer_items.value -= 1
                    print(f"Consumer {self.consumer_id} consumed: {item}. Buffer items count: {self.buffer_items.value}")
                    time.sleep(1)  
                else:
                    print(f"Buffer is empty, consumer {self.consumer_id} is waiting.")
            time.sleep(1)  


if __name__ == "__main__":
    pipe = multiprocessing.Pipe()
    buffer_items = multiprocessing.Value('i', 0)

    producers = [Producer(pipe, buffer_items, i) for i in range(3)]
    consumers = [Consumer(pipe, buffer_items, i) for i in range(5)]

    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.start()

    for producer in producers:
        producer.join()

    for consumer in consumers:
        consumer.join()

    pipe[0].close()
    pipe[1].close()
