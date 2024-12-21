# code for the situation in which the buffer is full and the producer has to 
# wait for at least one consumer takes action 
# There are 1 producer and 5 consumers



import threading
import time
import random

buffer_size = 30
buffer = [random.randint(1, 150) for i in range (buffer_size)]


empty = threading.Semaphore(0)
full = threading.Semaphore(buffer_size)
mutex = threading.Semaphore(1)

def producer():
    while len(buffer) <= buffer_size:
        print('Producer is waiting')
        
        item = random.randint(1, 150)
        empty.acquire()  
        mutex.acquire()
        
        print(f"Producer produced: {item}")
        
        mutex.release()
        full.release()  
        
        time.sleep(2)  

def consumer(consumer_id):
    while len(buffer) > 0:
        print(f"Consumer {consumer_id} is waiting")
        
        full.acquire()  
        mutex.acquire()
        
        # if buffer:        
        item = buffer.pop(0)
        print(f"Consumer {consumer_id} consumed: {item}")
        mutex.release()
        empty.release()  
        time.sleep(1)  

producer_thread = threading.Thread(target=producer)
consumer_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(5)]

producer_thread.start()
for thread in consumer_threads:
    thread.start()

producer_thread.join()
for thread in consumer_threads:
    thread.join()
    
    
print('Program terminated')
