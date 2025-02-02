import multiprocessing
import time
import random

BUFFER_CAPACITY = 10


class Producer(multiprocessing.Process):
    def __init__(self, queue, producer_id):
        super().__init__()
        self.queue = queue
        self.producer_id = producer_id

    def run(self):
        while True:
            if self.queue.qsize() < BUFFER_CAPACITY:
                item = random.randint(1, 100)
                print(f"Producer {self.producer_id} produced: {item}. Queue items count: {self.queue.qsize()}")
                self.queue.put(item)
                time.sleep(1)  
            else:
                print(f"Queue is full, producer {self.producer_id} is waiting. Queue items count: {self.queue.qsize()}")
            time.sleep(1) 


class Consumer(multiprocessing.Process):
    def __init__(self, queue, consumer_id):
        super().__init__()
        self.queue = queue
        self.consumer_id = consumer_id

    def run(self):
        while True:
            if (self.queue.empty()):
                print(f"Queue is empty, consumer {self.consumer_id} is waiting.")
                break
            else:
                item = self.queue.get()
                print(f"Consumer {self.consumer_id} consumed: {item}. Queue items count: {self.queue.qsize()}")
                time.sleep(1)  
            time.sleep(4)  


if __name__ == "__main__":
    queue = multiprocessing.Queue()

    producers = [Producer(queue, i) for i in range(3)]
    consumers = [Consumer(queue, i) for i in range(5)]

    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.start()

    for producer in producers:
        producer.join()

    for consumer in consumers:
        consumer.join()
