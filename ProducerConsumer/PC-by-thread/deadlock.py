#  In this program, the number of consumed items is not shared among the 
#  threads of consumer. So the code is traped in a deadlock when the consumers waits for
# the producer to produce but it wont cause it already produced as the number of buffer size.


import threading
import time
import random


buffer = [-1 for i in range(5)]
buffer_size = 5


empty = threading.Semaphore(buffer_size)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)


in_index = 0
out_index = 0

def producer():
    global in_index, out_index
    
    items_produced = 0
    counter = 0
    
    while(items_produced < buffer_size):
        counter += 1
        empty.acquire()
        mutex.acquire() # handling race condition
        
        buffer[in_index] = counter
        in_index = (in_index + 1) % buffer_size
        print(f"Producer produced {counter}. Items produced: {items_produced}")
        
        mutex.release()
        full.release()
        time.sleep(1)
        
        items_produced += 1
    
    
def consumer(consumer_id):
    global in_index, out_index
    
    items_consumed = 0
    couter = 0
    while(items_consumed < buffer_size):
        print(f'Consumer {consumer_id} is waiting. Items cosumed: {items_consumed}')
        full.acquire()
        mutex.acquire()
        
        item = buffer[out_index]
        items_consumed += 1
        out_index = (out_index + 1) % buffer_size
        print(f"Consumer {consumer_id} consumed: {item}.")
        
        mutex.release()
        empty.release()
        time.sleep(3)
        
        
        
# producer_thread = threading.Thread(target=producer)
# consumer_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(5)]

# producer_thread.start()
# for thread in consumer_threads:
#     thread.start()

# producer_thread.join()
# for thread in consumer_threads:
#     thread.join()

# print('Program terminated')



# anoter way:


sequence_semaphore = threading.Semaphore(0)

def p1(p1_id):
    sequence_semaphore.acquire()
    print(f"P1 {p1_id} is running")
    time.sleep(1)
    sequence_semaphore.release()  

def p2(p2_id):
    sequence_semaphore.acquire()  
    print(f"P2 {p2_id} is running")


p1_threads = [threading.Thread(target=p1, args=(i,)) for i in range(1)]     
p2_threads = [threading.Thread(target=p2, args=(i,)) for i in range(1)]

for thread in p1_threads:
    thread.start()
    
for thread in p2_threads:
    thread.start()

for thread in p1_threads:
    thread.join()
for thread in p2_threads:
    thread.join()

print('Program terminated')
