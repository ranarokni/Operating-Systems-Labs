import multiprocessing
import time
import random

def producer(pipe):
    # producer writes data to the pipe.
    sender = pipe[1]
    for i in range(5):
        item = random.randint(1, 100)
        print(f"Producer produced: {item}")
        sender.send(item)
        time.sleep(1) 
    sender.send(None)  # signal termination

def consumer(pipe):
    # consumer reads data from the pipe.
    receiver = pipe[0]
    while True:
        item = receiver.recv()
        if item is None:  # termination signal
            print("Consumer received termination signal.")
            break
        print(f"Consumer consumed: {item}")
        time.sleep(2) 

if __name__ == "__main__":
    pipe = multiprocessing.Pipe()
    
    producer_process = multiprocessing.Process(target=producer, args=(pipe,))
    consumer_process = multiprocessing.Process(target=consumer, args=(pipe,))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()
    
    pipe[0].close()
    pipe[1].close()
