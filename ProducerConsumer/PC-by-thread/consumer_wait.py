# This is a program in which the producer will produce items till the
# bounded buffer is full. Initialization is empty.
# if time sleep of producer set to be more than consumer, the program
# would continue only when the producer produces sth as all the consumers 
# are waiting for it (and the number of consumers is more than the number of producers)
# There are 1 producer and 5 consumers


# todo: write the document


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
        print('Producer is waiting')
        item = random.randint(1, 100)
        
        empty.acquire()  
        mutex.acquire()
        
        buffer.append(item)
        print(f"Producer produced: {item}")
        
        mutex.release()
        full.release()  
        time.sleep(1)  # change this to see the effect of consumers waiting for priducer, best time is 

def consumer(consumer_id):
    print(f'Consumer {consumer_id} is waiting')
    
    while len(buffer) <= buffer_size and len(buffer) >= 0:
        full.acquire()  
        mutex.acquire()
        
        if buffer:
            item = buffer.pop(0)
            print(f"Consumer {consumer_id} consumed: {item}")
            
        mutex.release()
        empty.release()  
        time.sleep(5)         # with empty buffer initialization, this should be larger than producer sleep time. 
                                # Perfectly more than 5 times larger as the number of consumers = 5*producers 
        
        
producer_thread = threading.Thread(target=producer)
consumer_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(5)]

producer_thread.start()
for thread in consumer_threads:
    thread.start()

producer_thread.join()
for thread in consumer_threads:
    thread.join()

print('Program terminated')
