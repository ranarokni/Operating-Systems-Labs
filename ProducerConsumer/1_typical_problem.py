# This is a program in which the producer will produce items till the
# bounded buffer is full. 
# There are 1 producer and 5 consumers


import threading
import time
import random

buffer = [random.randint(1, 150) for i in range(10)] # uncomment this to see producer will
                                                      # stop produceing cause the buffer is full.

buffer = []
buffer_size = 10


# initialization with nonempty buffer at the begining
empty = threading.Semaphore(buffer_size - 5)
full = threading.Semaphore(5)
mutex = threading.Semaphore(1)



def producer():
    while len(buffer) <= buffer_size:
        print('Producer is waiting')
        item = random.randint(1, 150)
        
        empty.acquire()  
        mutex.acquire()
        
        buffer.append(item)
        print(f"Producer produced: {item}")
        
        mutex.release()
        full.release()  
        time.sleep(1)  

def consumer(consumer_id):
    
    while len(buffer) <= buffer_size and len(buffer) >= 0:
        print(f"Consumer {consumer_id} is waiting")

        full.acquire()  
        mutex.acquire()
        
        if buffer:
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
