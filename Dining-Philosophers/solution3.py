# This code solves DP problem by defining a shared priority queue between the philosophers.


import heapq
import threading
import time
import random


class Philosopher(threading.Thread):
    def __init__(self, name, id, left, right, priority_queue, queue_lock, waiter):
        threading.Thread.__init__(self)
        self.name = name
        self.id = id
        self.left_fork = left
        self.right_fork = right
        self.priority_queue = priority_queue
        self.queue_lock = queue_lock
        self.waiter = waiter
        self.hungry_since = None
        
    def run(self):
        
        while True:
            self.think()
            self.hungry_since = time.time()  
            self.add_to_queue()  # everytime a philospher is hungry it's added to
                                # waiting queue list
            self.eat()
            
    def add_to_queue(self):   
        with self.queue_lock:
            heapq.heappush(self.priority_queue, (self.hungry_since, self))
            
            
    def think(self):
        think_time = random.randint(1, 5)
        print(f"{self.name} is thinking for {think_time} seconds")
        time.sleep(think_time)
        print(f"{self.name} stopped thinking")
        
    
    def eat(self):
        left_fork = self.left_fork
        right_fork = self.right_fork
        
        while True:
            with self.queue_lock:
                if self.priority_queue[0][1] == self:  # A philosopher can start eating 
                                                        # if and only if it is the first one
                                                        # waiting in the pririty queue
                    heapq.heappop(self.priority_queue)
                    break
            
            time.sleep(0.1)  

        with self.waiter:  
            left_fork.acquire()
            right_fork.acquire()
        
        print(f"{self.name} is eating.")
        time.sleep(2)  

        left_fork.release()
        right_fork.release()
        
        print(f"{self.name} stopped eating.")
            
        


forks = [threading.Semaphore(1) for i in range(5)]

priority_queue = []    # define a shared priority queue
queue_lock = threading.Lock()   # lock on the queue so that only one philosopher
                                # can be added to the queue at each time (FIFO manner)
                                
waiter = threading.Semaphore(4) # indicates that only 4 philosophers can be waiter.

philosophers = [
    Philosopher(f"Philosopher {i + 1}", i + 1, forks[i % 5], forks[(i + 1) % 5], priority_queue, queue_lock, waiter)
    for i in range(5)
]


for philosopher in philosophers:
    philosopher.start()
    
for philosopher in philosophers:
    philosopher.join()