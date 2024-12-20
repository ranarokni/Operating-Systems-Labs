# This is a program in which the producer will produce items till the
# bounded buffer is full. Initialization is empty.
# There are 3 producers and 5 consumers


import threading
import time
import random

# buffer = [random.randint(1, 100) for i in range(10)] # uncomment this to see producer will
                                                      # stop produceing cause the buffer is full.

buffer = []
buffer_size = 10

# initialization with empty buffer at the begigning
empty = threading.Semaphore(buffer_size)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)


def producer():
    while len(buffer) <= buffer_size:
        item = random.randint(1, 100)
        empty.acquire()  
        mutex.acquire()
        buffer.append(item)
        print(f"Producer produced: {item}")
        mutex.release()
        full.release()  
        time.sleep(1)  
        
        
def consumer(consumer_id):
    print(f'Consumer {consumer_id} is waiting')
    
    while len(buffer) <= buffer_size:
        full.acquire()  
        if buffer:
            item = buffer.pop(0)
            print(f"Consumer {consumer_id} consumed: {item}")
        mutex.release()
        empty.release()  
        time.sleep(5)         
        
        
producer_thread = [threading.Thread(target=producer, args=(i,)) for i in range(3)]
consumer_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(5)]

producer_thread.start()
for thread in consumer_threads:
    thread.start()

producer_thread.join()
for thread in consumer_threads:
    thread.join()

print('Program terminated')
